from __future__ import annotations

from enum import StrEnum


class AssistantState(StrEnum):
    STANDBY = "STANDBY"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    SPEAKING = "SPEAKING"
    NOTIFYING = "NOTIFYING"
    PRIVACY = "PRIVACY"
    ERROR = "ERROR"
