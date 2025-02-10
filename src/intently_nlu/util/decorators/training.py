"""Utilities for training and fitting models"""

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from intently_nlu.exceptions import NoSuchSetting, NotTrained
from intently_nlu.util.intently_logging import get_logger, log_error

T = TypeVar("T")


def fitted_required(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that marks that a class must be fitted before calling a method"""

    @wraps(func)
    def func_wrapper(self: Any, *args: Any, **kwargs: Any):
        if not self.fitted:
            e = NotTrained(
                f"{self.__name__} must be fitted before calling {func.__name__}."
            )
            raise log_error(
                get_logger(__name__), e, "Action with fitted required"
            ) from e
        return func(self, *args, **kwargs)

    return func_wrapper


def update_settings(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that updates the settings of a class"""

    @wraps(func)
    def func_wrapper(self: Any, *args: Any, **kwargs: Any):
        settings = kwargs.get("settings")
        if settings is not None:
            for key in settings:
                if key in self.settings:
                    self.settings[key] = settings[key]
                else:
                    e = NoSuchSetting(
                        f"{self.__name__} has no overridable parameter '{key}'."
                    )
                    raise log_error(
                        get_logger(__name__), e, "Update class settings"
                    ) from e
        return func(self, *args, **kwargs)

    return func_wrapper
