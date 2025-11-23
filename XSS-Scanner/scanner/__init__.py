"""
XSS Scanner Package
Professional context-aware cross-site scripting detection engine.
"""

from .engine import XSSEngine
from .analyzer import ContextAnalyzer, InjectionContext
from .payloads import PayloadGenerator, PolyglotPayloads
from .reporter import HTMLReporter

__all__ = [
    'XSSEngine',
    'ContextAnalyzer',
    'InjectionContext',
    'PayloadGenerator',
    'PolyglotPayloads',
    'HTMLReporter',
]

__version__ = '2.0.0'
__author__ = 'Security Research Team'
