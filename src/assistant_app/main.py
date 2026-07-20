from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from assistant_app.core.config import ConfigManager
from assistant_app.core.default_commands import build_command_router
from assistant_app.services.application_service import ApplicationService
from assistant_app.services.system_service import SystemService
from assistant_app.ui.main_window import MainWindow


def main() -> None:
    config = ConfigManager()
    persona = config.load_persona("jarvis")
    system_service = SystemService()
    application_service = ApplicationService(system_service=system_service)
    command_router = build_command_router(application_service)

    app = QApplication(sys.argv)
    theme_path = config.theme_path(persona.theme)
    try:
        app.setStyleSheet(theme_path.read_text(encoding="utf-8"))
    except OSError:
        pass

    window = MainWindow(
        persona=persona,
        system_service=system_service,
        command_router=command_router,
    )
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
