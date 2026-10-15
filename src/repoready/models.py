from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    PASS="PASS"
    FAIL="FAIL"
    WARNING="WARNING"
    UNKNOWN="UNKNOWN"

@dataclass
class CheckResult:
    name:str
    status:Status
    message:str