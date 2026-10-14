from enum import Enum


class AuditResult(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"