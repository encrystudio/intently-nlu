"""Utilities for measuring timings"""

from collections.abc import Callable
from functools import wraps
from time import time
from typing import Any, TypeVar

from intently_nlu.util.intently_logging import get_logger

T = TypeVar("T")


def elapsed_time(
    message: str = "Function took", warn_if_more_than: float = -1.0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to print the elapsed time for running the decorated function

    Args:
        message (str, optional): Optional custom message to print with the elapsed time. Defaults to "Function took".
        warn_if_more_than (float, optional): Print a warning when the function takes more time. Defaults to -1.0.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            elapsed = end_time - start_time
            get_logger(__name__).info("%s %s seconds.", message, f"{elapsed:.4f}")
            if 0 <= warn_if_more_than < elapsed:
                get_logger(__name__).warning(
                    "%s %s seconds. This is longer than %s!",
                    message,
                    f"~{elapsed:.4f}",
                    warn_if_more_than,
                )
            return result

        return wrapper

    return decorator
