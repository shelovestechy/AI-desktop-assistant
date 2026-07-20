from __future__ import annotations

import os
import subprocess
import webbrowser
from dataclasses import dataclass

from assistant_app.core.command_router import CommandResult
from assistant_app.services.system_service import SystemService


@dataclass(frozen=True)
class ApplicationService:
    """Open only explicitly approved destinations. Never execute arbitrary user input."""

    system_service: SystemService

    def open_chatgpt(self) -> CommandResult:
        opened = webbrowser.open("https://chatgpt.com", new=2)
        return CommandResult(opened, "Opening ChatGPT." if opened else "ChatGPT could not be opened.")

    def open_spotify(self) -> CommandResult:
        if os.name == "nt":
            try:
                os.startfile("spotify:")  # type: ignore[attr-defined]
                return CommandResult(True, "Opening Spotify.")
            except OSError:
                pass

        opened = webbrowser.open("https://open.spotify.com", new=2)
        return CommandResult(opened, "Opening Spotify." if opened else "Spotify could not be opened.")

    def open_windows_security(self) -> CommandResult:
        if os.name != "nt":
            return CommandResult(False, "Windows Security is available only on Windows.")

        try:
            subprocess.Popen(
                ["explorer.exe", "windowsdefender:"],
                shell=False,
                close_fds=True,
            )
        except OSError:
            return CommandResult(False, "Windows Security could not be opened.")
        return CommandResult(True, "Opening Windows Security.")

    def show_system_status(self) -> CommandResult:
        snapshot = self.system_service.snapshot()
        return CommandResult(
            True,
            f"CPU usage is {snapshot.cpu_percent:.0f} percent and memory usage is "
            f"{snapshot.memory_percent:.0f} percent.",
        )

    def close_assistant(self) -> CommandResult:
        return CommandResult(True, "Shutting down.", should_close=True)
