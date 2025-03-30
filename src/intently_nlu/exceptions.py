"""Custom exceptions for the IntentlyNLU library"""


class IntentlyNLUError(Exception):
    """Base class for exceptions raised in the  IntentlyNLU library"""


class NotTrained(IntentlyNLUError):
    """Raised if an engine component is used while not fitted"""


class NoSuchSetting(IntentlyNLUError):
    """Raised if an engine component has no parameter with this name"""


class DatasetNotValid(IntentlyNLUError):
    """Raised if a Dataset is not valid"""


class DatasetError(IntentlyNLUError):
    """Raised if an issue related to the training data occurs at runtime"""


class RuntimeMLError(IntentlyNLUError):
    """Raised if an issue related to machine learning occurs at runtime"""


class ResourceError(IntentlyNLUError):
    """Raised if an issue related to local resources occurs."""


class ModelVersionError(IntentlyNLUError):
    """Raised if a loaded engine has an incompatible version."""
