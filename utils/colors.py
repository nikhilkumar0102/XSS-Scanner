"""
Beautiful terminal colors and UI components.
Provides consistent, eye-catching visual styling throughout the application.
"""

from colorama import Fore, Back, Style, init
from datetime import datetime

init(autoreset=True)


class Colors:
    """Centralized color scheme for consistent UI."""
    
    # Primary colors
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    
    # Semantic colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    
    # Background colors
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    
    # Styled combinations
    SUCCESS = f"{Style.BRIGHT}{Fore.GREEN}"
    ERROR = f"{Style.BRIGHT}{Fore.RED}"
    WARNING = f"{Style.BRIGHT}{Fore.YELLOW}"
    INFO = f"{Fore.CYAN}"
    HEADER = f"{Style.BRIGHT}{Fore.MAGENTA}"
    
    @staticmethod
    def print_success(msg: str):
        """Print success message in bright green."""
        print(f"{Colors.SUCCESS}✓{Colors.RESET} {msg}")
    
    @staticmethod
    def print_error(msg: str):
        """Print error message in bright red."""
        print(f"{Colors.ERROR}✗{Colors.RESET} {msg}")
    
    @staticmethod
    def print_warning(msg: str):
        """Print warning message in bright yellow."""
        print(f"{Colors.WARNING}⚠{Colors.RESET} {msg}")
    
    @staticmethod
    def print_info(msg: str):
        """Print info message in cyan."""
        print(f"{Colors.INFO}{msg}{Colors.RESET}")
    
    @staticmethod
    def print_header(msg: str):
        """Print section header in bright magenta."""
        print(f"{Colors.HEADER}{msg}{Colors.RESET}")
    
    @staticmethod
    def print_dim(msg: str):
        """Print dimmed text."""
        print(f"{Colors.DIM}{msg}{Colors.RESET}")
    
    @staticmethod
    def print_finding(param: str, context: str, payload: str):
        """Print XSS finding with special formatting."""
        print(f"\n{Colors.BG_RED}{Colors.WHITE} 🎯 XSS DISCOVERED {Colors.RESET}")
        print(f"{Colors.YELLOW}  Parameter : {Colors.WHITE}{param}{Colors.RESET}")
        print(f"{Colors.YELLOW}  Context   : {Colors.WHITE}{context}{Colors.RESET}")
        print(f"{Colors.YELLOW}  Payload   : {Colors.GREEN}{payload}{Colors.RESET}")


class Banner:
    """Stunning ASCII banner for application startup."""
    
    @staticmethod
    def show():
        """Display beautiful startup banner."""
        banner = f"""
{Colors.MAGENTA}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     ██╗  ██╗███████╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗        ║
║     ╚██╗██╔╝██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║        ║
║      ╚███╔╝ ███████╗███████╗    ███████╗██║     ███████║██╔██╗ ██║        ║
║      ██╔██╗ ╚════██║╚════██║    ╚════██║██║     ██╔══██║██║╚██╗██║        ║
║     ██╔╝ ██╗███████║███████║    ███████║╚██████╗██║  ██║██║ ╚████║        ║
║     ╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝        ║
║                                                                           ║
║ {Colors.CYAN}             Context-Aware XSS Detection Framework v2.0{Colors.MAGENTA}                   ║
║ {Colors.WHITE}                 Professional Security Assessment{Colors.MAGENTA}                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}  Author: Security Research Team
  Date: {datetime.now().strftime("%B %d, %Y")}
  Description: Advanced XSS scanner with context-aware payload generation
{Colors.RESET}
{Colors.YELLOW}{'─' * 75}{Colors.RESET}
"""
        print(banner)


class ProgressBar:
    """Simple progress indicator for scans."""
    
    def __init__(self, total: int, width: int = 50):
        self.total = total
        self.current = 0
        self.width = width
    
    def update(self, current: int):
        """Update progress bar."""
        self.current = current
        percent = int((current / self.total) * 100)
        filled = int((current / self.total) * self.width)
        bar = '█' * filled + '░' * (self.width - filled)
        
        print(f"\r{Colors.CYAN}  Progress: [{bar}] {percent}%{Colors.RESET}", end='', flush=True)
        
        if current >= self.total:
            print()  # New line when complete
                                              