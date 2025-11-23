# 🛡️ XSS Scanner v2.0

**Professional Context-Aware Cross-Site Scripting Detection Framework**

A senior-level, production-ready XSS vulnerability scanner with intelligent context detection, automatic parameter discovery, smart payload generation, and stunning visual reporting.

---

## ✨ Features

### 🎯 **Intelligent Parameter Discovery**
- Automatic extraction from URL query strings
- Form field detection and analysis
- Link-based parameter discovery
- Manual parameter specification support

### 🔍 **Advanced Context Detection**
- HTML Text Nodes
- Attribute Values (Double/Single/Unquoted)
- JavaScript Contexts (Script blocks & strings)
- HTML Comments
- JSON Responses
- CSS/Style Blocks
- URL Parameters

### 🚀 **Smart Capabilities**
- **Context-Aware Payloads**: Generates targeted exploits based on injection context
- **Multi-threaded Scanning**: Concurrent testing for faster results
- **Intelligent Reflection Detection**: Unique probe strings with accurate tracking
- **AI-Powered Payloads**: Optional Gemini AI integration for advanced exploitation
- **Modern Bypasses**: Includes polyglot payloads and creative techniques

### 📊 **Beautiful Reporting**
- **Stunning HTML Reports**: Dark/light mode toggle
- **Auto-Named Reports**: `xss-report_YYYY-MM-DD_HH-MM-SS_{domain}.html`
- **Responsive Design**: Works perfectly on mobile devices
- **Clickable Exploits**: Test vulnerabilities directly from the report
- **Syntax Highlighting**: Professional code display
- **Real-time Statistics**: Comprehensive scan metrics

### 🎨 **Professional UI**
- Eye-catching ASCII banner
- Rich color scheme with semantic meanings
- Real-time progress indicators
- Clean, organized terminal output
- Interactive guided setup

---

## 🚀 Quick Start

### Installation

```bash
# Clone or create the project directory
mkdir xss-scanner && cd xss-scanner

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the scanner
python main.py

# Follow the interactive prompts:
# 1. Enter target URL
# 2. Scanner auto-discovers parameters
# 3. Choose HTTP method (GET/POST)
# 4. Set thread count
# 5. Optional: Enable AI payloads
# 6. Confirm and start scan
# 7. Review auto-generated report
```

### Example Session

```
❯ python main.py

🎯 TARGET CONFIGURATION
❯ Target URL: https://example.com/search?q=test

🔍 PARAMETER DISCOVERY
  ✓ Found 1 parameter(s) in URL: q

🔧 HTTP METHOD
❯ Select method [1-2]: 1

⚡ PERFORMANCE
❯ Threads [default: 5]: 5

🤖 AI-POWERED PAYLOADS (Optional)
❯ Enable Gemini AI? (y/N): n

📋 SCAN SUMMARY
  Target URL  : https://example.com/search
  Parameters  : q (1 total)
  Threads     : 5

❯ Start scan? (Y/n): y

[Scan completes, report auto-opens]
```

---

## 📁 Project Structure

```
xss-scanner/
├── main.py                      # Interactive entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── USAGE_GUIDE.md              # Detailed usage instructions
├── GEMINI_SETUP.md             # AI integration guide
├── scanner/                     # Core scanning engine
│   ├── __init__.py
│   ├── engine.py               # Main XSS scanning logic
│   ├── analyzer.py             # Context detection engine
│   ├── payloads.py             # Smart payload generation
│   └── reporter.py             # HTML report generation
├── utils/                       # Utility functions
│   ├── __init__.py
│   └── colors.py               # Beautiful terminal UI
└── reports/                     # Generated HTML reports (auto-created)
```

---

## 🎯 How It Works

### 1. **URL Analysis & Parameter Discovery**
User enters target URL:
```
https://example.com/search?q=test&filter=all
```

Scanner automatically:
- Extracts parameters: `q`, `filter`
- Parses domain: `example.com`
- Identifies injection points

If no URL parameters, scanner:
- Fetches the page
- Analyzes HTML forms
- Discovers parameters from links
- Allows manual entry

### 2. **Probe Injection**
Injects unique probe strings to detect reflection points:
```
XSS_PROBE_A7K9M2Q8P1L5
```

Tests each parameter individually to identify where input appears in the response.

### 3. **Context Analysis**
Analyzes WHERE the probe appears in the response:
- Inside HTML tags? → HTML Text context
- Inside attributes? → Attribute context (checks quotes)
- Inside `<script>`? → JavaScript context
- Inside comments? → Comment context
- Inside JSON? → JSON context

### 4. **Smart Payload Generation**
Generates context-specific payloads:

**HTML Text Context:**
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
```

**Double-Quoted Attribute:**
```html
"><script>alert(1)</script>
" onload="alert(1)" x="
```

**JavaScript Context:**
```javascript
';alert(1)//
</script><script>alert(1)</script>
```

**With AI (Optional):**
- Analyzes actual HTML structure
- Generates creative bypasses
- Adapts to visible filters

### 5. **Verification**
Tests each payload and confirms successful injection by checking for trigger functions in the response.

### 6. **Reporting**
Generates a beautiful HTML report:
```
reports/xss-report_2024-01-15_14-30-45_example.com.html
```

Contains:
- All discovered vulnerabilities
- Injection contexts
- Working payloads
- Clickable exploit URLs
- Scan statistics

---

## 🤖 AI-Powered Payloads (Optional)

### Setup Gemini AI

```bash
# Get free API key from: https://makersuite.google.com/app/apikey

# Set environment variable
export GEMINI_API_KEY="your-api-key-here"

# Run scanner
python main.py

# Enable when prompted
❯ Enable Gemini AI? (y/N): y
```

### Benefits

- **Context-Aware**: Analyzes actual injection point
- **Creative**: Generates novel bypass techniques
- **Adaptive**: Learns from HTML structure
- **Enhanced Coverage**: 3 additional payloads per context

See [GEMINI_SETUP.md](GEMINI_SETUP.md) for detailed AI configuration.

---

## 💡 Usage Examples

### Example 1: Simple Search Page
```bash
python main.py
❯ Target URL: https://shop.com/search?q=laptop
# Scanner auto-finds 'q' parameter and tests it
```

### Example 2: Multiple Parameters
```bash
python main.py
❯ Target URL: https://site.com/page?id=1&name=test&sort=asc
# Scanner tests: id, name, sort
```

### Example 3: Form-Based
```bash
python main.py
❯ Target URL: https://app.com/contact
# Scanner discovers form fields: name, email, message
# User selects which form to test
```

### Example 4: Manual Parameters
```bash
python main.py
❯ Target URL: https://api.com/endpoint
❯ Parameters: userId,action,data
# Manually specify parameters when auto-discovery fails
```

---

## 📊 Report Features

### Automatic Naming
```
xss-report_2024-01-15_14-30-45_example.com.html
          └─ Date ─┘ └─ Time ─┘ └─ Domain ─┘
```

### Report Contents

1. **Executive Summary**
   - Total vulnerabilities found
   - Scan duration
   - Risk assessment
   - Target information

2. **Vulnerability Cards**
   - Parameter name
   - Injection context
   - Working payload (syntax-highlighted)
   - Full exploit URL (clickable)
   - Timestamp

3. **Interactive Features**
   - 🌓 Dark/light mode toggle
   - 📱 Mobile-responsive
   - 🔗 One-click exploit testing
   - 💻 Professional design

---

## 🛡️ Security & Ethics

### ⚠️ IMPORTANT

**Only test applications you own or have explicit written permission to test.**

Unauthorized testing is illegal and unethical. This tool is for:

- **Security Research**: Authorized testing
- **Penetration Testing**: With proper contracts
- **Bug Bounty Programs**: Within scope
- **Education**: On practice environments

### Legal Use Cases

✅ Your own websites/applications  
✅ Client sites with written authorization  
✅ Bug bounty programs (within scope)  
✅ Practice labs (DVWA, XSS Game, etc.)  
✅ Local development environments  

❌ Sites without permission  
❌ Production systems without authorization  
❌ Third-party applications  

---

## 🔧 Advanced Configuration

### Adjust Thread Count

```bash
# Conservative (rate-limited sites)
❯ Threads: 1-3

# Standard (most sites)
❯ Threads: 5-10

# Aggressive (authorized pentests only)
❯ Threads: 10-20
```

### Custom Headers

Edit `scanner/engine.py`:
```python
session.headers.update({
    'User-Agent': 'CustomBot/1.0',
    'Cookie': 'session=abc123',
    'Authorization': 'Bearer token'
})
```

### Timeout Settings

```python
# In scanner/engine.py
response = self.session.get(url, timeout=30)  # Increase timeout
```

---

## 🐛 Troubleshooting

### No Parameters Discovered

**Solution:** Manually specify parameters:
```bash
❯ Parameters: q,search,id,name
```

### Connection Issues

**Check:**
1. Internet connection
2. Target is accessible
3. No VPN/proxy blocking
4. Firewall settings

### WAF Blocks

**Symptoms:** 403/406 responses  
**Solution:**
- Reduce threads to 1-2
- Test during off-peak hours
- Use AI for evasion
- Verify authorization

---

## 📚 Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage instructions
- **[GEMINI_SETUP.md](GEMINI_SETUP.md)** - AI integration guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation & setup

---

## 🎓 Learning Resources

### Practice Targets

- **Google XSS Game**: https://xss-game.appspot.com
- **DVWA**: http://www.dvwa.co.uk
- **PortSwigger Labs**: https://portswigger.net/web-security/cross-site-scripting

### Understanding XSS

- [OWASP XSS Guide](https://owasp.org/www-community/attacks/xss/)
- [PortSwigger Academy](https://portswigger.net/web-security/cross-site-scripting)

---

## 🤝 Contributing

Contributions welcome! Please maintain:
- Code quality and architecture
- Visual consistency
- Comprehensive testing
- Clear documentation

---

## 📄 License

This tool is provided for educational and authorized testing purposes only.

---

## 🌟 Credits

**XSS Scanner v2.0**  
Professional Context-Aware XSS Detection Framework  

Built for security researchers, penetration testers, and bug bounty hunters.

---

**Built with ❤️ for the security community**

*Remember: With great power comes great responsibility. Always get authorization!*
