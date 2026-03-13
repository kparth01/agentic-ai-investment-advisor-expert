
from colorama import Fore, Style, init

init(autoreset=True)

class Custom_printer():

    def cout_cyan(self, message: str):
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

    def cout_yellow(self, message: str):
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def cout_green(self, message: str):
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def cout_red(self, message: str):
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")

    def cout_magenta(self, message: str):
        print(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")