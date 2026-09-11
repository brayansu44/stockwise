from enum import Enum


class MovementType(str, Enum):
    ENTRY = "entry"
    EXIT = "exit"
    ADJUSTMENT = "adjustment"