from colorama import init
from colorama import Fore, Style
import logging


def setup_logging():
    init(autoreset=True)
    logging.basicConfig(
        level=logging.INFO,
        format=f"{Fore.BLUE}%(asctime)s - %(levelname)s - %(message)s{Style.RESET_ALL}",
        datefmt="%H:%M:%S",
    )
