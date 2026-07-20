from assistant_app.core.assistant_controller import AssistantController
from assistant_app.core.command_router import CommandResult, CommandRouter
from assistant_app.core.config import Persona


def build_controller() -> AssistantController:
    persona = Persona(
        assistant_name="Jarvis",
        wake_word="jarvis",
        user_title="sir",
        theme="jarvis",
        language="en",
        phrases={"greeting": "Systems online."},
    )
    router = CommandRouter()
    router.register(["status"], lambda: CommandResult(True, "All systems nominal."))
    router.register(
        ["open spotify"],
        lambda: CommandResult(True, "Opening Spotify."),
    )
    return AssistantController(persona=persona, command_router=router)


def test_returns_configured_greeting() -> None:
    assert build_controller().greeting() == "Systems online."


def test_processes_command_through_router() -> None:
    result = build_controller().process("Jarvis, status!")

    assert result.success is True
    assert result.message == "All systems nominal."


def test_processes_natural_language_through_intent_resolver() -> None:
    result = build_controller().process("Jarvis, could you launch Spotify please?")

    assert result.success is True
    assert result.message == "Opening Spotify."


def test_rejects_empty_input() -> None:
    result = build_controller().process("   ")

    assert result.success is False
    assert result.message == "Please enter a command."
