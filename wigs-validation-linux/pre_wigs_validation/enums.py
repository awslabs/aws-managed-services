from enum import Enum


class ValidationResult(str, Enum):
    PASS = "Pass"
    FAIL = "Fail"
    NOT_RUN = "Not Run"
    ERROR = "Error"


class ValidationConfig(str, Enum):
    CUSTOM = "Custom"
    DEFAULT = "Default"


class ValidationEnforcement(str, Enum):
    REQUIRED = "Required"
    RECOMMENDED = "Recommended"


class Colors(str, Enum):
    HEADER = "\033[95m"
    NOT_RUN = "\033[94m"
    PASS = "\033[92m"
    ERROR = "\033[35m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
