# 🎯 XSS Scanner - Complete Usage Guide

## 🚀 Quick Start

### Basic Scan
```bash
python main.py
```

That's it! The scanner will guide you through an interactive setup.

---

## 📖 Step-by-Step Walkthrough

### Step 1: Enter Target URL

```
🎯 TARGET CONFIGURATION
  Enter the URL you want to test for XSS vulnerabilities

❯ Target URL: https://example.com/search?q=test&filter=all
```

**What happens:**
- Scanner validates the URL
- Extracts domain and path
- Adds `http://` if missing

**URL Examples:**
```
✓ https://example.com/search?q=test
✓ http://testsite.com/page.php?id=1&name=admin
✓ example.com/profile.php?user=123
✓ http://10.0.0.1/app/search
```

---

### Step 2: Automatic Parameter Discovery

The scanner automatically discovers injectable parameters using multiple methods:

#### Method 1: URL Query Parameters
```
🔍 PARAMETER DISCOVERY
  ✓ Found 2 parameter(s) in URL: q, filter
```

**From URL:** `https://example.com/search?q=test&filter=all`
- Automatically extracts: `q`, `filter`
- Ready to test immediately

#### Method 2: Form Discovery
If no URL parameters exist:
```
  ⚡ No URL parameters found. Analyzing page for forms...
  ✓ Found 2 form(s) on the page

  📝 Form #1 parameters:
     • username = (empty)
     • password = (empty)
     • remember = 1

  ❯ Test this form? (y/N): y
```

**Scanner will:**
- Fetch the target page
- Parse all `<form>` elements
- Extract `<input>`, `<textarea>`, `<select>` fields
- Let you choose which form to test

#### Method 3: Link Analysis
If no forms found:
```
  ✓ Discovered parameters from links: id, page, sort
```

**Scanner analyzes:**
- All `<a href="...">` links on the page
- Extracts unique parameter names
- Suggests testing these parameters

#### Method 4: Manual Entry
If auto-discovery fails:
```
  ⚠ No parameters discovered automatically
  Enter parameter names separated by commas (e.g., q,search,id,name)

❯ Parameters: query,username,email
  ✓ Added 3 parameter(s): query, username, email
```

---

### Step 3: HTTP Method Selection

```
🔧 HTTP METHOD
  [1] GET (default)
  [2] POST

❯ Select method [1-2]: 1
```

**Choose:**
- **GET**: For URL parameters, search forms, filters
- **POST**: For login forms, submission forms, APIs

---

### Step 4: Performance Configuration

```
⚡ PERFORMANCE
  How many concurrent threads to use?
  Recommended: 5-10 for normal sites, 1-3 for rate-limited sites

❯ Threads [default: 5]: 8
```

**Thread Count Guidelines:**
- **1-3**: Rate-limited sites, careful testing
- **5-10**: Standard websites (recommended)
- **10-20**: Fast internal networks, pentesting labs
- **20+**: Only for authorized testing on your own infrastructure

---

### Step 5: AI Configuration (Optional)

```
🤖 AI-POWERED PAYLOADS (Optional)
  Enable Gemini AI for advanced, context-aware payload generation

❯ Enable Gemini AI? (y/N): y
```

**If enabled:**
```
❯ Enter API key now? (y/N): y
❯ API Key: AIzaSy...your-key...

  ✓ Gemini AI enabled successfully!
  AI will generate 3 additional payloads per context
```

**Benefits of AI:**
- Context-aware payload generation
- Analyzes actual HTML structure
- Creative bypass techniques
- 3 additional payloads per context

**To skip:** Just press `N` or ENTER

---

### Step 6: Scan Summary & Confirmation

```
📋 SCAN SUMMARY
  Target URL  : https://example.com/search
  HTTP Method : GET
  Parameters  : q, filter (2 total)
  Threads     : 8
  AI Payloads : Enabled

🚀 READY TO SCAN
  ⚠ Only test applications you own or have permission to test!

❯ Start scan? (Y/n):
```

Press ENTER or `Y` to start scanning.

---

### Step 7: Scanning Process

```
🔥 SCAN IN PROGRESS

─────────────────────────────────────────────────────────────────────────────
🔍 Testing parameter: q
  ⚡ Injecting probe...
  ✓ Reflected in 2 context(s):
    • HTML Text Node
    • Attribute Value (Double Quote)

🎯 XSS DISCOVERED → q
  Parameter : q
  Context   : HTML Text Node
  Payload   : <script>alert(1)</script>
  🔗 URL: https://example.com/search?q=%3Cscript%3Ealert%281%29%3C%2Fscript%3E

─────────────────────────────────────────────────────────────────────────────
🔍 Testing parameter: filter
  ⚡ Injecting probe...
  ⊗ Not reflected or no contexts detected

  Progress: [██████████████████████████████████████████████████] 100%
```

**What you'll see:**
- Real-time parameter testing
- Context detection results
- XSS discoveries with payloads
- Progress bar
- Color-coded output

---

### Step 8: Report Generation

```
📊 GENERATING REPORT

✨ SCAN COMPLETED
  Report File       : reports/xss-report_2024-01-15_14-30-45_example.com.html
  Vulnerabilities   : 1
  ⚠ SECURITY ALERT  : 1 XSS vulnerability(ies) found!
  Review the HTML report for detailed information

  Opening report in browser...
```

**Report automatically:**
- Opens in your default browser
- Named with timestamp and domain
- Contains full vulnerability details

---

## 💡 Real-World Examples

### Example 1: Testing a Search Form

```bash
$ python main.py

❯ Target URL: https://shop.example.com/search?q=laptop

# Scanner finds: q parameter
# Tests: HTML, attributes, JavaScript contexts
# Discovers: XSS in search results page
```

### Example 2: Login Form

```bash
$ python main.py

❯ Target URL: https://app.example.com/login
# No URL parameters

# Scanner discovers form:
📝 Form #1 parameters:
   • username
   • password
   • csrf_token

❯ Test this form? (y/N): y

# Method: POST
# Tests: username field for XSS
# Result: Found XSS in error messages
```

### Example 3: Profile Page

```bash
$ python main.py

❯ Target URL: https://social.example.com/profile?user=john&tab=posts

# Scanner finds: user, tab parameters
# Tests: Both parameters
# Discovers: XSS in user parameter (reflected in page title)
```

### Example 4: API Endpoint

```bash
$ python main.py

❯ Target URL: https://api.example.com/v1/search?query=test&format=json

# Scanner finds: query, format parameters
# Tests: JSON context detection
# Discovers: XSS in JSON response
```

---

## 🎯 Advanced Techniques

### Custom Parameter Testing

If you know the parameters but they're not in the URL:

```
❯ Target URL: https://example.com/app

  ⚠ No parameters discovered automatically
❯ Parameters: userId,action,data

# Manually specify parameters
# Scanner will test: userId, action, data
```

### Testing POST Forms

```
❯ Target URL: https://example.com/contact

# If form found:
❯ Test this form? (y/N): y

# Select method:
❯ Select method [1-2]: 2  # Choose POST

# Scanner will:
# - Send POST requests
# - Test form fields
# - Check response for reflections
```

### Rate-Limited Targets

```
❯ Threads [default: 5]: 1

# Use single thread for:
# - Rate-limited APIs
# - Sensitive production systems
# - Sites with aggressive WAFs
```

---

## 📊 Understanding Results

### Terminal Output

**Colors Guide:**
- 🟢 **Green**: Success, found reflection
- 🔴 **Red**: XSS discovered
- 🟡 **Yellow**: Warnings
- 🔵 **Cyan**: Information
- ⚪ **White/Dim**: Details

**Symbols:**
- ✓ Success
- ✗ Error
- ⚠ Warning
- 🔍 Testing
- 🎯 Discovery
- ⚡ Action

### HTML Report

The report includes:

1. **Summary Cards**
   - Total vulnerabilities
   - Scan duration
   - Risk level

2. **Vulnerability Details**
   - Parameter name
   - Injection context
   - Working payload
   - Full exploit URL

3. **Interactive Features**
   - Dark/light mode toggle
   - Clickable exploit links
   - Syntax-highlighted code
   - Mobile-responsive design

---

## 🛡️ Best Practices

### 1. Authorization

```
⚠ ONLY TEST SITES YOU OWN OR HAVE PERMISSION TO TEST
```

**Required:**
- Written authorization
- Defined scope
- Clear testing window
- Incident response plan

### 2. Start Conservatively

```bash
# First scan: Low threads, no AI
❯ Threads: 5
❯ Enable AI: n

# If needed: Increase threads
❯ Threads: 10
❯ Enable AI: y
```

### 3. Test in Stages

**Stage 1: Discovery**
- Test with 1-2 threads
- Identify reflection points
- Map attack surface

**Stage 2: Exploitation**
- Increase threads
- Enable AI payloads
- Test all contexts

**Stage 3: Verification**
- Review all findings
- Test manually
- Document results

### 4. Monitor Responses

Watch for:
- WAF blocks (403/406 responses)
- Rate limiting (429 responses)
- Account lockouts
- Service disruptions

---

## 🚨 Troubleshooting

### Issue: "No parameters discovered"

**Solutions:**
1. Add parameters manually
2. Check if page requires authentication
3. Verify URL is correct
4. Try accessing page in browser first

### Issue: "Connection timeout"

**Solutions:**
1. Check internet connection
2. Verify target is accessible
3. Reduce thread count
4. Increase timeout in `scanner/engine.py`

### Issue: "No vulnerabilities found"

**Possible reasons:**
1. Site is properly secured ✅
2. Parameters not injectable
3. Strong input validation
4. WAF blocking payloads

**Try:**
- Enable AI payloads
- Test different parameters
- Check report for reflection points
- Review scanner output carefully

### Issue: WAF Detection

Signs of WAF:
```
🔍 Testing parameter: q
  ⚡ Injecting probe...
  ❌ Request failed: 403 Forbidden
```

**Solutions:**
- Reduce thread count to 1-2
- Add delays between requests
- Use AI for evasion payloads
- Consider if testing is appropriate

---

## 📈 Workflow Examples

### Quick Security Check
```bash
python main.py
# Enter URL with parameters
# Use defaults
# Review report
# Duration: 1-2 minutes
```

### Thorough Assessment
```bash
python main.py
# Enter URL
# Enable AI
# Use 10 threads
# Test all discovered parameters
# Duration: 5-10 minutes
```

### Production Testing
```bash
python main.py
# Enter URL
# Disable AI (consistent results)
# Use 1-3 threads (careful)
# Review each finding manually
# Duration: 10-20 minutes
```

---

## 🎓 Tips for Success

1. **Start Simple**: Test known-vulnerable labs first
2. **Read Output**: Scanner provides detailed context information
3. **Verify Findings**: Click exploit URLs in report to confirm
4. **Document Everything**: Save reports with timestamps
5. **Learn Contexts**: Understand why each payload works
6. **Be Patient**: Thorough scanning takes time
7. **Stay Legal**: Only test authorized systems

---

## 🔗 Quick Reference

**Start Scanner:**
```bash
python main.py
```

**Set Gemini API Key:**
```bash
export GEMINI_API_KEY="your-key-here"
```

**View Report:**
```bash
# Reports are in: reports/xss-report_*.html
# Auto-opens in browser
```

**Cancel Scan:**
```
Press Ctrl+C anytime
```

---

**Happy (Authorized) Bug Hunting! 🎯**
