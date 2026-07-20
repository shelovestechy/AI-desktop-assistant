from assistant_app.core.intent_resolver import IntentResolver


def test_resolves_polite_spotify_request() -> None:
    result = IntentResolver().resolve(
        "Jarvis, could you launch Spotify please?",
        wake_word="jarvis",
    )

    assert result is not None
    assert result.command == "open spotify"


def test_resolves_natural_system_status_request() -> None:
    result = IntentResolver().resolve(
        "Can you show me the computer status?",
        wake_word="jarvis",
    )

    assert result is not None
    assert result.command == "show system status"


def test_resolves_windows_security_request() -> None:
    result = IntentResolver().resolve("Please open Defender")

    assert result is not None
    assert result.command == "open windows security"


def test_does_not_guess_unknown_action() -> None:
    result = IntentResolver().resolve("Delete all my files")

    assert result is None
