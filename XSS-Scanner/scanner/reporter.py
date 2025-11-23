"""
Beautiful, modern HTML report generation.
Creates responsive, interactive reports with dark/light mode toggle.
"""

from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse
import html
import re


class HTMLReporter:
    """
    Generates stunning, professional HTML security reports.
    Features: Dark/light mode, syntax highlighting, clickable exploits, responsive design.
    """
    
    # AFTER (Correct order):
    def __init__(self, filename: str = "xss_report.html", target_url: str = ""):

        # Store all instance variables FIRST
        self.target_url = target_url
        self.findings: List[Dict[str, str]] = []
        self.scan_start = datetime.now()

        # THEN use them
        if target_url:
            generated_name = self._generate_filename(target_url)
            self.filename = f"reports/{generated_name}"
        else:
            if not filename.startswith('reports/'):
                self.filename = f"reports/{filename}"
            else:
                self.filename = filename
    
    def _generate_filename(self, url: str) -> str:
        """
        Generate formatted filename: xss-report_YYYY-MM-DD_HH-MM-SS_{sanitized-domain}.html
        
        Args:
            url: Target URL
            
        Returns:
            Formatted filename
        """
        try:
            # Parse domain from URL
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            
            # Sanitize domain (remove invalid filename characters)
            sanitized = re.sub(r'[^\w\-.]', '_', domain)
            sanitized = sanitized.strip('_')
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Construct filename
            filename = f"xss-report_{timestamp}_{sanitized}.html"
            
            return filename
        except Exception:
            # Fallback to simple timestamp
            return f"xss-report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
    
    def add_finding(self, param: str, payload: str, context: str, url: str):
        """
        Add a vulnerability finding to the report.
        
        Args:
            param: Parameter name
            payload: XSS payload used
            context: Injection context
            url: Full exploit URL
        """
        self.findings.append({
            'param': param,
            'payload': payload,
            'context': context,
            'url': url,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
    
    def save(self):
        from pathlib import Path

        # Ensure reports directory exists
        Path("reports").mkdir(exist_ok=True)
    
        scan_duration = (datetime.now() - self.scan_start).total_seconds()
        html_content = self._generate_html(scan_duration)
    
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
        return self.filename

    def _generate_html(self, duration: float) -> str:
        """Generate complete HTML report content."""
        
        findings_html = self._generate_findings_html()
        summary_html = self._generate_summary_html(duration)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XSS Security Report - {datetime.now().strftime("%Y-%m-%d %H:%M")}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --border: #475569;
            --shadow: rgba(0, 0, 0, 0.3);
        }}
        
        [data-theme="light"] {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-card: #f1f5f9;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --border: #e2e8f0;
            --shadow: rgba(0, 0, 0, 0.1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background 0.3s, color 0.3s;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        /* Header */
        header {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            padding: 3rem 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px var(--shadow);
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .subtitle {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
            font-weight: 300;
        }}
        
        /* Theme Toggle */
        .theme-toggle {{
            position: fixed;
            top: 2rem;
            right: 2rem;
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 50px;
            padding: 0.5rem 1.5rem;
            cursor: pointer;
            font-weight: 500;
            color: var(--text-primary);
            transition: all 0.3s;
            z-index: 1000;
            box-shadow: 0 4px 12px var(--shadow);
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--shadow);
        }}
        
        /* Summary Cards */
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 12px var(--shadow);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px var(--shadow);
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent-primary);
        }}
        
        .stat-value.danger {{
            color: var(--danger);
        }}
        
        .stat-value.success {{
            color: var(--success);
        }}
        
        /* Findings Section */
        .section-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 3rem 0 1.5rem 0;
        }}
        
        .section-header h2 {{
            font-size: 1.75rem;
            font-weight: 600;
        }}
        
        .badge {{
            background: var(--danger);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
        }}
        
        /* Vulnerability Cards */
        .vulnerability {{
            background: var(--bg-card);
            border-left: 4px solid var(--danger);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px var(--shadow);
            transition: all 0.3s;
        }}
        
        .vulnerability:hover {{
            transform: translateX(4px);
            box-shadow: 0 8px 24px var(--shadow);
        }}
        
        .vuln-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .param-name {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .timestamp {{
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
        
        .info-grid {{
            display: grid;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .info-item {{
            display: flex;
            gap: 0.75rem;
        }}
        
        .info-label {{
            color: var(--text-secondary);
            font-weight: 600;
            min-width: 100px;
        }}
        
        .info-value {{
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }}
        
        .context-tag {{
            display: inline-block;
            background: var(--accent-primary);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        /* Code Block */
        .code-block {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            overflow-x: auto;
        }}
        
        .code-header {{
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.75rem;
            font-weight: 600;
        }}
        
        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--accent-primary);
            word-break: break-all;
        }}
        
        /* Exploit Link */
        .exploit-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, var(--danger), #dc2626);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }}
        
        .exploit-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
        }}
        
        .exploit-link::before {{
            content: "🔗";
        }}
        
        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            background: var(--bg-card);
            border-radius: 12px;
            border: 2px dashed var(--border);
        }}
        
        .empty-state-icon {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        
        .empty-state-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--success);
        }}
        
        .empty-state-text {{
            color: var(--text-secondary);
        }}
        
        /* Footer */
        footer {{
            margin-top: 4rem;
            padding: 2rem;
            text-align: center;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            h1 {{
                font-size: 1.75rem;
            }}
            
            .theme-toggle {{
                top: 1rem;
                right: 1rem;
                padding: 0.5rem 1rem;
                font-size: 0.875rem;
            }}
            
            .summary {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Toggle Theme</button>
    
    <div class="container">
        <header>
            <h1>🛡️ XSS Security Report</h1>
            <div class="subtitle">Context-Aware Vulnerability Assessment</div>
            {f'<div class="subtitle" style="margin-top: 0.5rem; font-size: 0.95rem;">Target: {html.escape(self.target_url)}</div>' if self.target_url else ''}
        </header>
        
        {summary_html}
        
        <div class="section-header">
            <h2>🎯 Vulnerability Findings</h2>
            {f'<span class="badge">{len(self.findings)} Found</span>' if self.findings else ''}
        </div>
        
        {findings_html}
    </div>
    
    <footer>
        <p>Generated by XSS Scanner v2.0 | {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}</p>
        <p style="margin-top: 0.5rem; font-size: 0.875rem;">Professional Security Assessment Tool</p>
    </footer>
    
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }}
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
</body>
</html>"""
    
    def _generate_summary_html(self, duration: float) -> str:
        """Generate summary statistics section."""
        return f"""
        <div class="summary">
            <div class="stat-card">
                <div class="stat-label">Vulnerabilities</div>
                <div class="stat-value {'danger' if self.findings else 'success'}">{len(self.findings)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Scan Duration</div>
                <div class="stat-value">{duration:.1f}s</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Completion Time</div>
                <div class="stat-value" style="font-size: 1.5rem;">{datetime.now().strftime("%H:%M")}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Risk Level</div>
                <div class="stat-value {'danger' if self.findings else 'success'}">
                    {'HIGH' if self.findings else 'LOW'}
                </div>
            </div>
        </div>
        """
    
    def _generate_findings_html(self) -> str:
        """Generate vulnerability findings section."""
        if not self.findings:
            return """
            <div class="empty-state">
                <div class="empty-state-icon">✅</div>
                <div class="empty-state-title">No Vulnerabilities Found</div>
                <div class="empty-state-text">The target application appears secure against XSS attacks in the tested parameters.</div>
            </div>
            """
        
        findings_html = ""
        for finding in self.findings:
            findings_html += f"""
            <div class="vulnerability">
                <div class="vuln-header">
                    <div class="param-name">{html.escape(finding['param'])}</div>
                    <div class="timestamp">⏰ {finding['timestamp']}</div>
                </div>
                
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">Context:</span>
                        <span class="context-tag">{html.escape(finding['context'])}</span>
                    </div>
                </div>
                
                <div class="code-block">
                    <div class="code-header">💉 Payload</div>
                    <code>{html.escape(finding['payload'])}</code>
                </div>
                
                <a href="{html.escape(finding['url'])}" target="_blank" class="exploit-link">
                    Test Exploit
                </a>
            </div>
            """
        
        return findings_html
