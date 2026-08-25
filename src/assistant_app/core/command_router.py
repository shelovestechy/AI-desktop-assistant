from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    success: bool
    message: str
    should_close: bool = False


CommandHandler = Callable[[], CommandResult]


class CommandRouter:
    """Resolve normalized user phrases to explicitly registered safe handlers."""

    def __init__(self) -> None:
        self._commands: dict[str, CommandHandler] = {}

    def register(self, phrases: list[str], handler: CommandHandler) -> None:
        for phrase in phrases:
            normalized = self.normalize(phrase)
            if not normalized:
                raise ValueError("Command phrase cannot be empty.")
            if normalized in self._commands:
                raise ValueError(f"Command phrase already registered: {phrase}")
            self._commands[normalized] = handler

    def dispatch(self, text: str, wake_word: str = "") -> CommandResult:
        normalized = self.normalize(text)
        normalized_wake_word = self.normalize(wake_word)

        if normalized_wake_word and normalized.startswith(f"{normalized_wake_word} "):
            normalized = normalized[len(normalized_wake_word) :].strip()
        elif normalized == normalized_wake_word:
            return CommandResult(success=True, message="I'm listening.")

        handler = self._commands.get(normalized)
        if handler is None:
            return CommandResult(
                success=False,
                message="I don't recognize that command yet.",
            )

        try:
            return handler()
        except Exception:  # noqa: BLE001 - handlers end at this safety boundary.
            return CommandResult(
                success=False,
                message="I was unable to complete that request safely.",
            )

    @staticmethod
    def normalize(text: str) -> str:
        normalized = text.casefold().strip()
        normalized = re.sub(r"[^\w\s-]", " ", normalized)
        return " ".join(normalized.split())
