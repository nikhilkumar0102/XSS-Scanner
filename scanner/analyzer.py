"""
Advanced context analysis engine.
Detects injection contexts with high accuracy using multiple detection methods.
"""

import re
from enum import Enum
from typing import List, Set
from bs4 import BeautifulSoup


class InjectionContext(Enum):
    """Enumeration of all detectable injection contexts."""
    
    HTML_TEXT = "HTML Text Node"
    ATTR_VALUE_DOUBLE_QUOTE = "Attribute Value (Double Quote)"
    ATTR_VALUE_SINGLE_QUOTE = "Attribute Value (Single Quote)"
    ATTR_VALUE_NO_QUOTE = "Attribute Value (No Quote)"
    ATTR_NAME = "Attribute Name"
    SCRIPT_BLOCK = "Inside <script> Tag"
    SCRIPT_STRING = "JavaScript String"
    STYLE_BLOCK = "Inside <style> Tag"
    HTML_COMMENT = "HTML Comment"
    JSON_VALUE = "JSON Context"
    URL_PARAM = "URL Parameter"
    
    def __str__(self):
        return self.value


class ContextAnalyzer:
    """
    Analyzes HTML responses to determine injection contexts.
    Uses multiple detection strategies for accuracy.
    """
    
    def __init__(self, html: str, probe: str, content_type: str = ""):
        """
        Initialize analyzer with response data.
        
        Args:
            html: The HTML response content
            probe: The unique probe string injected
            content_type: Response Content-Type header
        """
        self.html = html
        self.probe = probe
        self.content_type = content_type.lower()
    
    def detect_all(self) -> List[InjectionContext]:
        """
        Detect all injection contexts where probe appears.
        
        Returns:
            List of detected InjectionContext enums
        """
        contexts: Set[InjectionContext] = set()
        
        # Quick check: probe must exist in response
        if self.probe not in self.html:
            return []
        
        # Run all detection methods
        contexts.update(self._detect_json())
        contexts.update(self._detect_script_contexts())
        contexts.update(self._detect_style_block())
        contexts.update(self._detect_html_comment())
        contexts.update(self._detect_attribute_contexts())
        contexts.update(self._detect_text_node())
        contexts.update(self._detect_url_param())
        
        return list(contexts)
    
    def _detect_json(self) -> Set[InjectionContext]:
        """Detect JSON context."""
        contexts = set()
        
        # Check Content-Type
        if "json" in self.content_type:
            contexts.add(InjectionContext.JSON_VALUE)
            return contexts
        
        # Check JSON structure
        stripped = self.html.strip()
        if (stripped.startswith(("{", "[")) and stripped.endswith(("}", "]"))):
            if self.probe in stripped:
                contexts.add(InjectionContext.JSON_VALUE)
        
        return contexts
    
    def _detect_script_contexts(self) -> Set[InjectionContext]:
        """Detect script tag and JavaScript string contexts."""
        contexts = set()
        
        # Inside <script> tags
        script_pattern = rf'<script[^>]*>.*?{re.escape(self.probe)}.*?</script>'
        if re.search(script_pattern, self.html, re.DOTALL | re.IGNORECASE):
            contexts.add(InjectionContext.SCRIPT_BLOCK)
            
            # Check if inside JS string
            for match in re.finditer(script_pattern, self.html, re.DOTALL | re.IGNORECASE):
                script_content = match.group()
                
                # Check for string contexts: "probe" or 'probe'
                if re.search(rf'["\'].*?{re.escape(self.probe)}.*?["\']', script_content):
                    contexts.add(InjectionContext.SCRIPT_STRING)
        
        return contexts
    
    def _detect_style_block(self) -> Set[InjectionContext]:
        """Detect CSS/style context."""
        contexts = set()
        
        style_pattern = rf'<style[^>]*>.*?{re.escape(self.probe)}.*?</style>'
        if re.search(style_pattern, self.html, re.DOTALL | re.IGNORECASE):
            contexts.add(InjectionContext.STYLE_BLOCK)
        
        return contexts
    
    def _detect_html_comment(self) -> Set[InjectionContext]:
        """Detect HTML comment context."""
        contexts = set()
        
        comment_pattern = rf'<!--.*?{re.escape(self.probe)}.*?-->'
        if re.search(comment_pattern, self.html, re.DOTALL):
            contexts.add(InjectionContext.HTML_COMMENT)
        
        return contexts
    
    def _detect_attribute_contexts(self) -> Set[InjectionContext]:
        """Detect various attribute value contexts."""
        contexts = set()
        
        # Double quoted attribute: attr="probe"
        if re.search(rf'="\s*[^"]*{re.escape(self.probe)}[^"]*"', self.html):
            contexts.add(InjectionContext.ATTR_VALUE_DOUBLE_QUOTE)
        
        # Single quoted attribute: attr='probe'
        if re.search(rf"='\s*[^']*{re.escape(self.probe)}[^']*'", self.html):
            contexts.add(InjectionContext.ATTR_VALUE_SINGLE_QUOTE)
        
        # Unquoted attribute: attr=probe
        if re.search(rf'=\s*{re.escape(self.probe)}(?:\s|[/>]|$)', self.html):
            contexts.add(InjectionContext.ATTR_VALUE_NO_QUOTE)
        
        # Attribute name: probe="value"
        if re.search(rf'{re.escape(self.probe)}\s*=', self.html):
            contexts.add(InjectionContext.ATTR_NAME)
        
        return contexts
    
    def _detect_text_node(self) -> Set[InjectionContext]:
        """Detect HTML text node context using BeautifulSoup."""
        contexts = set()
        
        try:
            soup = BeautifulSoup(self.html, 'html.parser')
            
            # Search for probe in text nodes
            if soup.find(string=re.compile(re.escape(self.probe))):
                contexts.add(InjectionContext.HTML_TEXT)
        except Exception:
            # Fallback: simple regex check
            # Check if probe appears outside of tags
            text_pattern = rf'>[^<]*{re.escape(self.probe)}[^<]*<'
            if re.search(text_pattern, self.html):
                contexts.add(InjectionContext.HTML_TEXT)
        
        return contexts
    
    def _detect_url_param(self) -> Set[InjectionContext]:
        """Detect URL parameter context (reflected in href, src, etc.)."""
        contexts = set()
        
        # Check if probe appears in URL attributes
        url_attrs = ['href', 'src', 'action', 'data']
        for attr in url_attrs:
            pattern = rf'{attr}\s*=\s*["\']?[^"\'>\s]*{re.escape(self.probe)}[^"\'>\s]*["\']?'
            if re.search(pattern, self.html, re.IGNORECASE):
                contexts.add(InjectionContext.URL_PARAM)
                break
        
        return contexts
