from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Persona:
    assistant_name: str
    wake_word: str
    user_title: str
    theme: str
    language: str
    phrases: dict[str, str]

    @classmethod
    def fallback(cls) -> "Persona":
        return cls(
            assistant_name="Assistant",
            wake_word="assistant",
            user_title="",
            theme="default",
            language="en",
            phrases={"wake_response": "I'm listening."},
        )


class ConfigManager:
    """Load user-facing identity and theme settings without hard-coding a brand."""

    def __init__(self, project_root: Path = PROJECT_ROOT) -> None:
        self.project_root = project_root

    def load_persona(self, persona_name: str = "jarvis") -> Persona:
        path = self.project_root / "config" / "personas" / f"{persona_name}.json"
        try:
            raw: Any = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return Persona.fallback()

        if not isinstance(raw, dict):
            return Persona.fallback()

        fallback = Persona.fallback()
        phrases_raw = raw.get("phrases", {})
        phrases = (
            {str(key): str(value) for key, value in phrases_raw.items()}
            if isinstance(phrases_raw, dict)
            else fallback.phrases
        )

        return Persona(
            assistant_name=str(raw.get("assistant_name", fallback.assistant_name)),
            wake_word=str(raw.get("wake_word", fallback.wake_word)),
            user_title=str(raw.get("user_title", fallback.user_title)),
            theme=str(raw.get("theme", fallback.theme)),
            language=str(raw.get("language", fallback.language)),
            phrases=phrases,
        )

    def theme_path(self, theme_name: str) -> Path:
        requested = self.project_root / "themes" / theme_name / "theme.qss"
        if requested.is_file():
            return requested
        return self.project_root / "themes" / "default" / "theme.qss"
