from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class IntentMatch:
    command: str
    confidence: float


class IntentResolver:
    """Resolve common natural-language requests to safe canonical commands.

    The resolver is deliberately deterministic and local. It never invents actions:
    it only maps recognized wording to commands already allowlisted by the router.
    """

    _POLITE_PREFIXES = (
        "please ",
        "could you ",
        "can you ",
        "would you ",
        "will you ",
        "i want you to ",
        "i would like you to ",
    )

    def resolve(self, text: str, wake_word: str = "") -> IntentMatch | None:
        normalized = self._normalize(text)
        normalized = self._strip_wake_word(normalized, wake_word)
        normalized = self._strip_polite_prefix(normalized)

        if not normalized:
            return None

        words = set(normalized.split())

        if normalized in {
            "help",
            "commands",
            "show commands",
            "available commands",
            "what can you do",
            "what are your capabilities",
            "show me what you can do",
        }:
            return IntentMatch("help", 0.98)

        if self._contains_target(normalized, ("spotify", "music")) and words.intersection(
            {"open", "launch", "start", "play", "put"}
        ):
            return IntentMatch("open spotify", 0.95)

        if self._contains_target(normalized, ("chatgpt", "chat gpt", "openai", "open ai")) and words.intersection(
            {"open", "launch", "start"}
        ):
            return IntentMatch("open chatgpt", 0.95)

        if self._contains_target(normalized, ("windows security", "defender", "security")) and words.intersection(
            {"open", "launch", "start", "show"}
        ):
            return IntentMatch("open windows security", 0.95)

        status_terms = ("system status", "computer status", "pc status", "cpu", "memory", "ram")
        if self._contains_target(normalized, status_terms) and (
            words.intersection({"show", "check", "tell", "give", "display"})
            or normalized in status_terms
        ):
            return IntentMatch("show system status", 0.9)

        if self._contains_target(normalized, ("assistant", "jarvis", "application", "app")) and words.intersection(
            {"close", "exit", "quit", "shutdown", "stop"}
        ):
            return IntentMatch("close assistant", 0.95)

        return None

    @staticmethod
    def _contains_target(text: str, targets: tuple[str, ...]) -> bool:
        return any(target in text for target in targets)

    @classmethod
    def _strip_polite_prefix(cls, text: str) -> str:
        for prefix in cls._POLITE_PREFIXES:
            if text.startswith(prefix):
                return text[len(prefix) :].strip()
        return text

    @classmethod
    def _strip_wake_word(cls, text: str, wake_word: str) -> str:
        normalized_wake_word = cls._normalize(wake_word)
        if normalized_wake_word and text.startswith(f"{normalized_wake_word} "):
            return text[len(normalized_wake_word) :].strip()
        return text

    @staticmethod
    def _normalize(text: str) -> str:
        cleaned = re.sub(r"[^\w\s]", " ", text.casefold())
        return " ".join(cleaned.split())
