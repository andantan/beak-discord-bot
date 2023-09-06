import sys
import logging

from typing import Optional


def boot_issue(print_message: str, log_message: Optional[str], sys_exit: bool) -> None:
    if log_message: logging.fatal(msg=log_message)

    print(print_message)
    
    if sys_exit: sys.exit(-1)
