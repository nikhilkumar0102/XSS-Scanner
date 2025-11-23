#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    CONTEXT-AWARE XSS SCANNER v2.0                         ║
║                     Professional Security Assessment Tool                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

Entry point for the XSS Scanner application.
"""

import sys
import os
import webbrowser
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode
import requests

from scanner.engine import XSSEngine
from scanner.reporter import HTMLReporter
from scanner.payloads import PayloadGenerator
from utils.colors import Colors, Banner


def discover_parameters(url: str) -> dict:
    """
    Automatically discover injectable parameters from a URL.
    
    Args:
        url: Target URL to analyze
        
    Returns:
        Dictionary of discovered parameters
    """
    params = {}
    
    try:
        parsed = urlparse(url)
        
        # 1. Extract query parameters from URL
        query_params = parse_qs(parsed.query)
        for key in query_params.keys():
            params[key] = query_params[key][0] if query_params[key] else ''
        
        if params:
            Colors.print_success(f"  ✓ Found {len(params)} parameter(s) in URL: {', '.join(params.keys())}")
            return params
        
        # 2. Try to discover parameters by fetching the page
        Colors.print_info("  ⚡ No URL parameters found. Analyzing page for forms...")
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            
            # Parse HTML for forms
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all input fields in forms
            forms = soup.find_all('form')
            if forms:
                Colors.print_success(f"  ✓ Found {len(forms)} form(s) on the page")
                
                for idx, form in enumerate(forms, 1):
                    form_params = {}
                    inputs = form.find_all(['input', 'textarea', 'select'])
                    
                    for inp in inputs:
                        name = inp.get('name')
                        if name and inp.get('type') != 'submit':
                            form_params[name] = inp.get('value', '')
                    
                    if form_params:
                        Colors.print_info(f"\n  📝 Form #{idx} parameters:")
                        for key, val in form_params.items():
                            Colors.print_dim(f"     • {key} = {val if val else '(empty)'}")
                        
                        use_form = input(f"\n{Colors.CYAN}  ❯ Test this form? (y/N): {Colors.RESET}").strip().lower()
                        if use_form == 'y':
                            # Get form action URL
                            action = form.get('action', '')
                            if action:
                                if not action.startswith('http'):
                                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                                    action = base_url + action if action.startswith('/') else base_url + '/' + action
                                Colors.print_success(f"  ✓ Using form action URL: {action}")
                                return form_params
                            return form_params
            
            # 3. Look for common parameter patterns in links
            links = soup.find_all('a', href=True)
            discovered_params = set()
            
            for link in links:
                href = link['href']
                if '?' in href:
                    link_params = parse_qs(urlparse(href).query)
                    discovered_params.update(link_params.keys())
            
            if discovered_params:
                Colors.print_success(f"  ✓ Discovered parameters from links: {', '.join(discovered_params)}")
                params = {key: '' for key in discovered_params}
                return params
                
        except Exception as e:
            Colors.print_warning(f"  ⚠ Could not analyze page: {str(e)[:50]}")
        
    except Exception as e:
        Colors.print_error(f"  ✗ Error parsing URL: {e}")
    
    return params


def get_target_from_user():
    """
    Interactive prompt to get target URL and discover parameters.
    
    Returns:
        Dictionary with target configuration
    """
    Colors.print_header("\n🎯 TARGET CONFIGURATION")
    Colors.print_info("  Enter the URL you want to test for XSS vulnerabilities")
    Colors.print_dim("  Examples:")
    Colors.print_dim("    • https://example.com/search?q=test")
    Colors.print_dim("    • http://testsite.com/page.php?id=1&name=admin")
    Colors.print_dim("    • https://vulnerable-app.com/profile")
    
    url = input(f"\n{Colors.CYAN}❯ Target URL: {Colors.RESET}").strip()
    
    if not url:
        Colors.print_error("URL cannot be empty!")
        return None
    
    # Add http:// if no scheme provided
    if not url.startswith(('http://', 'https://')):
        Colors.print_warning("  No scheme provided, assuming http://")
        url = 'http://' + url
    
    # Validate URL
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            Colors.print_error("Invalid URL format!")
            return None
    except Exception:
        Colors.print_error("Invalid URL!")
        return None
    
    Colors.print_header("\n🔍 PARAMETER DISCOVERY")
    
    # Automatically discover parameters
    params = discover_parameters(url)
    
    # If no parameters found, allow manual entry
    if not params:
        Colors.print_warning("\n  ⚠ No parameters discovered automatically")
        Colors.print_info("  You can manually specify parameters to test")
        Colors.print_dim("  Enter parameter names separated by commas (e.g., q,search,id,name)")
        Colors.print_dim("  Or press ENTER to skip")
        
        param_input = input(f"\n{Colors.CYAN}❯ Parameters: {Colors.RESET}").strip()
        
        if param_input:
            params = {p.strip(): '' for p in param_input.split(',') if p.strip()}
            Colors.print_success(f"  ✓ Added {len(params)} parameter(s): {', '.join(params.keys())}")
        else:
            Colors.print_error("  No parameters to test. Cannot proceed.")
            return None
    
    # Get HTTP method
    Colors.print_header("\n🔧 HTTP METHOD")
    Colors.print_info("  [1] GET (default)")
    Colors.print_info("  [2] POST")
    
    method_choice = input(f"\n{Colors.CYAN}❯ Select method [1-2]: {Colors.RESET}").strip()
    method = 'POST' if method_choice == '2' else 'GET'
    
    # Get thread count
    Colors.print_header("\n⚡ PERFORMANCE")
    Colors.print_info("  How many concurrent threads to use?")
    Colors.print_dim("  Recommended: 5-10 for normal sites, 1-3 for rate-limited sites")
    
    thread_input = input(f"\n{Colors.CYAN}❯ Threads [default: 5]: {Colors.RESET}").strip()
    threads = int(thread_input) if thread_input.isdigit() else 5
    
    # Extract base URL (without query parameters)
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    return {
        'name': 'Custom Target Scan',
        'url': base_url,
        'method': method,
        'params': params,
        'threads': threads
    }


def configure_gemini():
    """Configure Gemini AI for advanced payload generation."""
    Colors.print_header("\n🤖 AI-POWERED PAYLOADS (Optional)")
    Colors.print_info("  Enable Gemini 2.0 Flash for intelligent XSS payload generation")
    Colors.print_dim("  • Analyzes parameter names and injection contexts")
    Colors.print_dim("  • Generates context-aware, filter-evading payloads")
    Colors.print_dim("  • Free tier available at: https://makersuite.google.com/app/apikey")
    
    choice = input(f"\n{Colors.CYAN}❯ Enable Gemini AI? (y/N): {Colors.RESET}").strip().lower()
    
    if choice == 'y':
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            Colors.print_warning("\n  GEMINI_API_KEY not found in environment variables")
            Colors.print_info("  You can either:")
            Colors.print_dim("    1. Export it: export GEMINI_API_KEY='your-key'")
            Colors.print_dim("    2. Enter it now (less secure)")
            
            choice2 = input(f"\n{Colors.CYAN}❯ Enter API key now? (y/N): {Colors.RESET}").strip().lower()
            
            if choice2 == 'y':
                api_key = input(f"{Colors.CYAN}❯ API Key: {Colors.RESET}").strip()
        
        if api_key:
            Colors.print_info("\n  Initializing Gemini 2.0 Flash model...")
            success = PayloadGenerator.initialize_gemini(api_key)
            if success:
                Colors.print_success("  ✓ Gemini AI enabled successfully!")
                Colors.print_success("  ✓ Using model: gemini-2.0-flash-exp")
                Colors.print_dim("  AI will analyze parameters and generate 5 custom payloads per context")
                return True
            else:
                Colors.print_error("  ✗ Failed to initialize Gemini AI")
                Colors.print_dim("  Check your API key and internet connection")
                Colors.print_dim("  Continuing with traditional payloads only...")
        else:
            Colors.print_warning("  No API key provided. Using traditional payloads.")
    else:
        Colors.print_dim("  Skipping AI configuration. Using traditional payloads only.")
    
    return False


def main():
    """Main entry point with streamlined user experience."""
    
    # Display stunning banner
    Banner.show()
    
    # Get target configuration from user
    target = get_target_from_user()
    
    if not target:
        Colors.print_error("\n❌ Failed to configure target. Exiting.")
        sys.exit(1)
    
    # Optional: Configure Gemini AI
    configure_gemini()
    
    # Display configuration summary
    Colors.print_header("\n📋 SCAN SUMMARY")
    Colors.print_success(f"  Target URL  : {target['url']}")
    Colors.print_success(f"  HTTP Method : {target['method']}")
    Colors.print_success(f"  Parameters  : {', '.join(target['params'].keys())} ({len(target['params'])} total)")
    Colors.print_success(f"  Threads     : {target['threads']}")
    Colors.print_success(f"  AI Payloads : {'Enabled' if PayloadGenerator.gemini_enabled else 'Disabled'}")
    
    # Initialize components
    Path("reports").mkdir(exist_ok=True)
    
    reporter = HTMLReporter(target_url=target['url'])
    engine = XSSEngine(
        url=target['url'],
        method=target['method'],
        reporter=reporter
    )
    
    # Confirmation before starting
    Colors.print_header("\n🚀 READY TO SCAN")
    Colors.print_warning("  ⚠ Only test applications you own or have permission to test!")
    
    confirm = input(f"\n{Colors.CYAN}❯ Start scan? (Y/n): {Colors.RESET}").strip().lower()
    
    if confirm == 'n':
        Colors.print_warning("\n⚠️  Scan cancelled by user")
        sys.exit(0)
    
    print()  # Blank line for spacing
    
    # Run the scan
    Colors.print_header("🔥 SCAN IN PROGRESS")
    engine.run(
        params=target['params'],
        threads=target['threads']
    )
    
    # Generate report
    Colors.print_header("\n📊 GENERATING REPORT")
    
    # Ensure reports directory exists before saving
    Path("reports").mkdir(exist_ok=True)
    
    report_path = reporter.save()
    
    # Final summary
    Colors.print_header("\n✨ SCAN COMPLETED")
    Colors.print_success(f"  Report File       : {report_path}")
    Colors.print_info(f"  Vulnerabilities   : {len(reporter.findings)}")
    
    if reporter.findings:
        Colors.print_error(f"  ⚠ SECURITY ALERT  : {len(reporter.findings)} XSS vulnerability(ies) found!")
        Colors.print_dim("  Review the HTML report for detailed information")
    else:
        Colors.print_success("  ✓ No XSS vulnerabilities detected")
    
    # Auto-open report
    try:
        Colors.print_dim("\n  Opening report in browser...")
        webbrowser.open(f"file://{Path(report_path).absolute()}")
    except Exception:
        Colors.print_dim("  Could not auto-open browser. Please open the report manually.")
    
    Colors.print_dim(f"\n{'─' * 75}\n")
    Colors.print_info("  Thank you for using XSS Scanner v2.0!")
    Colors.print_dim("  Report issues at: https://github.com/your-repo/xss-scanner\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Colors.print_warning("\n\n⚠️  Scan interrupted by user")
        Colors.print_dim("  Partial results may be available in the reports directory\n")
        sys.exit(0)
    except Exception as e:
        Colors.print_error(f"\n❌ Fatal error: {e}")
        Colors.print_dim("  Please report this issue with the full error message\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
