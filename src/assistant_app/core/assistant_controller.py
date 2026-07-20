from __future__ import annotations

from dataclasses import dataclass

from assistant_app.core.command_router import CommandRouter
from assistant_app.core.config import Persona
from assistant_app.core.intent_resolver import IntentResolver


@dataclass(frozen=True)
class AssistantReply:
    message: str
    success: bool
    should_close: bool = False


class AssistantController:
    """Coordinate user requests without coupling command logic to the UI."""

    def __init__(
        self,
        persona: Persona,
        command_router: CommandRouter,
        intent_resolver: IntentResolver | None = None,
    ) -> None:
        self.persona = persona
        self.command_router = command_router
        self.intent_resolver = intent_resolver or IntentResolver()

    def greeting(self) -> str:
        return self.persona.phrases.get(
            "greeting",
            f"{self.persona.assistant_name} online. How may I help?",
        )

    def process(self, text: str) -> AssistantReply:
        command = text.strip()
        if not command:
            return AssistantReply("Please enter a command.", success=False)

        intent = self.intent_resolver.resolve(command, wake_word=self.persona.wake_word)
        if intent is not None:
            result = self.command_router.dispatch(intent.command)
        else:
            result = self.command_router.dispatch(
                command,
                wake_word=self.persona.wake_word,
            )

        return AssistantReply(
            message=result.message,
            success=result.success,
            should_close=result.should_close,
        )
