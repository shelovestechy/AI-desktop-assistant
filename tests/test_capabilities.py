from assistant_app.core.capabilities import CAPABILITIES, format_capabilities


def test_capability_catalog_includes_help_and_exit() -> None:
    names = {capability.name for capability in CAPABILITIES}

    assert "Help" in names
    assert "Exit" in names


def test_formats_capabilities_for_conversation() -> None:
    message = format_capabilities()

    assert message.startswith("Here is what I can do right now:")
    assert "open Spotify" in message
    assert "show system status" in message
    assert "close assistant" in message
