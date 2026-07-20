from assistant_app.core.command_router import CommandResult, CommandRouter


def test_dispatches_registered_command() -> None:
    router = CommandRouter()
    router.register(["open dashboard"], lambda: CommandResult(True, "Opened."))

    result = router.dispatch("Jarvis, open dashboard!", wake_word="jarvis")

    assert result.success is True
    assert result.message == "Opened."


def test_normalizes_whitespace_and_case() -> None:
    router = CommandRouter()
    router.register(["system status"], lambda: CommandResult(True, "Ready."))

    result = router.dispatch("  SYSTEM   STATUS  ")

    assert result.success is True


def test_unknown_command_is_rejected() -> None:
    router = CommandRouter()

    result = router.dispatch("delete everything")

    assert result.success is False
    assert "recognize" in result.message


def test_handler_failure_does_not_escape_router() -> None:
    router = CommandRouter()

    def failing_handler() -> CommandResult:
        raise RuntimeError("failure")

    router.register(["fail safely"], failing_handler)
    result = router.dispatch("fail safely")

    assert result.success is False
    assert "safely" in result.message


def test_duplicate_phrase_is_rejected() -> None:
    router = CommandRouter()
    router.register(["open app"], lambda: CommandResult(True, "Opened."))

    try:
        router.register(["OPEN APP"], lambda: CommandResult(True, "Opened again."))
    except ValueError as error:
        assert "already registered" in str(error)
    else:
        raise AssertionError("Duplicate command phrase should raise ValueError")
