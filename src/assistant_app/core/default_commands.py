from __future__ import annotations

from assistant_app.core.command_router import CommandRouter
from assistant_app.services.application_service import ApplicationService


def build_command_router(application_service: ApplicationService) -> CommandRouter:
    router = CommandRouter()

    router.register(
        ["open chatgpt", "open chat gpt", "open ai"],
        application_service.open_chatgpt,
    )
    router.register(
        ["open spotify", "start spotify", "play music"],
        application_service.open_spotify,
    )
    router.register(
        ["open windows security", "open defender", "show security"],
        application_service.open_windows_security,
    )
    router.register(
        ["show system status", "system status", "computer status"],
        application_service.show_system_status,
    )
    router.register(
        ["close assistant", "close jarvis", "shut down assistant"],
        application_service.close_assistant,
    )

    return router
