"""
Core XSS scanning engine.
Orchestrates probing, context detection, payload testing, and result reporting.
"""

import requests
import random
import string
import threading
from typing import Dict, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from .analyzer import ContextAnalyzer, InjectionContext
from .payloads import PayloadGenerator, PolyglotPayloads
from .reporter import HTMLReporter
from utils.colors import Colors, ProgressBar


class XSSEngine:
    """
    Main scanning engine that orchestrates the XSS detection workflow.
    Thread-safe, context-aware, and designed for production use.
    """
    
    def __init__(self, url: str, method: str = "GET", reporter: Optional[HTMLReporter] = None):
        """
        Initialize the XSS scanner engine.
        
        Args:
            url: Target URL to scan
            method: HTTP method (GET or POST)
            reporter: HTMLReporter instance for results
        """
        self.url = url.rstrip("/")
        self.method = method.upper()
        self.reporter = reporter
        self.session = self._create_session()
        self.print_lock = threading.Lock()
        self.findings_count = 0
    
    def _create_session(self) -> requests.Session:
        """Create configured requests session."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        return session
    
    def _log(self, message: str, color_func=None):
        """Thread-safe logging."""
        with self.print_lock:
            if color_func:
                color_func(message)
            else:
                print(message)
    
    def _generate_probe(self) -> str:
        """Generate unique probe string."""
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        return f"XSS_PROBE_{random_part}"
    
    def _extract_snippet(self, html: str, probe: str, context_chars: int = 200) -> str:
        """
        Extract HTML snippet around the probe for AI analysis.
        
        Args:
            html: Full HTML response
            probe: The probe string
            context_chars: Characters to extract before/after probe
            
        Returns:
            HTML snippet containing the probe
        """
        try:
            probe_index = html.find(probe)
            if probe_index == -1:
                return ""
            
            start = max(0, probe_index - context_chars)
            end = min(len(html), probe_index + len(probe) + context_chars)
            
            return html[start:end]
        except Exception:
            return ""
    
    def _extract_broader_context(self, html: str, probe: str, context_chars: int = 500) -> str:
        """
        Extract broader HTML context for comprehensive AI analysis.
        
        Args:
            html: Full HTML response
            probe: The probe string
            context_chars: Characters to extract before/after probe
            
        Returns:
            Broader HTML context containing the probe
        """
        try:
            probe_index = html.find(probe)
            if probe_index == -1:
                return ""
            
            start = max(0, probe_index - context_chars)
            end = min(len(html), probe_index + len(probe) + context_chars)
            
            return html[start:end]
        except Exception:
            return ""
    
    def _send_request(self, params: Dict[str, str]) -> Optional[requests.Response]:
        """
        Send HTTP request with error handling.
        
        Args:
            params: Request parameters
            
        Returns:
            Response object or None on failure
        """
        try:
            if self.method == "GET":
                response = self.session.get(
                    self.url,
                    params=params,
                    timeout=15,
                    allow_redirects=True
                )
            else:
                response = self.session.post(
                    self.url,
                    data=params,
                    timeout=15,
                    allow_redirects=True
                )
            return response
        except requests.exceptions.Timeout:
            self._log(f"  ⏱️  Timeout for request", Colors.print_warning)
        except requests.exceptions.RequestException as e:
            self._log(f"  ❌ Request failed: {str(e)[:50]}", Colors.print_error)
        return None
    
    def _test_reflection(self, param: str, base_params: Dict[str, str]) -> Optional[tuple]:
        """
        Test if parameter reflects in response.
        
        Returns:
            Tuple of (probe, response, contexts, html_snippet, response_snippet) or None
        """
        probe = self._generate_probe()
        test_params = base_params.copy()
        test_params[param] = probe
        
        response = self._send_request(test_params)
        if not response:
            return None
        
        # Check if probe reflected
        if probe not in response.text:
            return None
        
        # Analyze contexts
        analyzer = ContextAnalyzer(
            response.text,
            probe,
            response.headers.get('Content-Type', '')
        )
        contexts = analyzer.detect_all()
        
        if not contexts:
            return None
        
        # Extract HTML snippet around probe for AI analysis
        html_snippet = self._extract_snippet(response.text, probe)
        
        # Extract broader context for comprehensive AI analysis
        response_snippet = self._extract_broader_context(response.text, probe)
        
        return (probe, response, contexts, html_snippet, response_snippet)
    
    def _test_payload(self, param: str, payload: str, base_params: Dict[str, str]) -> Optional[str]:
        """
        Test a specific payload.
        
        Returns:
            Exploit URL if successful, None otherwise
        """
        test_params = base_params.copy()
        test_params[param] = payload
        
        response = self._send_request(test_params)
        if not response:
            return None
        
        # Check for successful execution indicators
        triggers = [
            'alert(', 'alert`', 'confirm(', 'prompt(', 'print(',
            'onerror=', 'onload=', 'onfocus=', 'onclick='
        ]
        
        response_lower = response.text.lower()
        if any(trigger.lower() in response_lower for trigger in triggers):
            # Additional check: ensure payload wasn't HTML encoded
            if payload in response.text or payload.replace('"', '&quot;') not in response.text:
                return response.url
        
        return None
    
    def scan_parameter(self, param: str, base_params: Dict[str, str]) -> int:
        """
        Scan a single parameter for XSS vulnerabilities.
        
        Args:
            param: Parameter name to test
            base_params: Base parameters dictionary
            
        Returns:
            Number of vulnerabilities found
        """
        self._log(f"\n{Colors.CYAN}{'─' * 75}")
        self._log(f"🔍 Testing parameter: {Colors.BOLD}{param}{Colors.RESET}", Colors.print_info)
        
        # Step 1: Test reflection
        self._log("  ⚡ Injecting probe...", Colors.print_dim)
        reflection_result = self._test_reflection(param, base_params)
        
        if not reflection_result:
            self._log(f"  ⊗ Not reflected or no contexts detected", Colors.print_dim)
            return 0
        
        probe, response, contexts, html_snippet, response_snippet = reflection_result
        
        # Step 2: Report contexts
        context_names = [ctx.value for ctx in contexts]
        self._log(f"  ✓ Reflected in {len(contexts)} context(s):", Colors.print_success)
        for ctx in context_names:
            self._log(f"    • {ctx}", Colors.print_dim)
        
        # Show AI analysis status
        if PayloadGenerator.gemini_enabled:
            self._log(f"  🤖 AI analyzing parameter and generating custom payloads...", Colors.print_info)
        
        # Step 3: Test payloads for each context
        vulnerabilities = 0
        
        for context in contexts:
            # Generate payloads with AI analysis (parameter name, context, HTML snippets)
            payloads = PayloadGenerator.generate(
                context=context,
                param_name=param,
                html_snippet=html_snippet,
                response_snippet=response_snippet
            )
            
            # Show payload count
            if PayloadGenerator.gemini_enabled:
                traditional_count = 7  # Approximate
                ai_count = len(payloads) - traditional_count
                if ai_count > 0:
                    self._log(f"  🎯 Testing {len(payloads)} payloads ({traditional_count} traditional + {ai_count} AI-generated)", Colors.print_dim)
            
            for payload in payloads:
                exploit_url = self._test_payload(param, payload, base_params)
                
                if exploit_url:
                    vulnerabilities += 1
                    self.findings_count += 1
                    
                    # Report finding
                    Colors.print_finding(param, context.value, payload)
                    self._log(f"  🔗 URL: {exploit_url}\n", Colors.print_dim)
                    
                    # Add to reporter
                    if self.reporter:
                        self.reporter.add_finding(
                            param=param,
                            payload=payload,
                            context=context.value,
                            url=exploit_url
                        )
                    
                    # Stop testing this context after first success
                    break
        
        if vulnerabilities == 0:
            self._log(f"  ⊗ No working payloads found", Colors.print_dim)
        
        return vulnerabilities
    
    def run(self, params: Dict[str, str], threads: int = 10):
        """
        Run the XSS scan on all parameters.
        
        Args:
            params: Dictionary of parameters to test
            threads: Number of concurrent threads
        """
        param_names = list(params.keys())
        total_params = len(param_names)
        
        self._log(f"\n{Colors.HEADER}🎯 Scanning {total_params} parameter(s) with {threads} thread(s){Colors.RESET}\n")
        
        # Scan parameters concurrently
        completed = 0
        progress = ProgressBar(total_params)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            # Submit all tasks
            future_to_param = {
                executor.submit(self.scan_parameter, param, params): param
                for param in param_names
            }
            
            # Process results as they complete
            for future in as_completed(future_to_param):
                param = future_to_param[future]
                try:
                    future.result()
                except Exception as e:
                    self._log(f"  ❌ Error scanning {param}: {e}", Colors.print_error)
                
                completed += 1
                progress.update(completed)
        
        # Summary
        self._log(f"\n{Colors.CYAN}{'─' * 75}{Colors.RESET}")
        self._log(f"\n{Colors.HEADER}📊 SCAN SUMMARY{Colors.RESET}")
        self._log(f"{Colors.SUCCESS}  ✓ Parameters tested: {total_params}{Colors.RESET}")
        self._log(f"{Colors.ERROR if self.findings_count > 0 else Colors.SUCCESS}  ⚠ Vulnerabilities found: {self.findings_count}{Colors.RESET}\n")
