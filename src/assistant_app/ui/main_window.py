from __future__ import annotations

from datetime import datetime
from html import escape

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from assistant_app.core.assistant_controller import AssistantController
from assistant_app.core.config import Persona
from assistant_app.core.state import AssistantState
from assistant_app.services.system_service import SystemService


class MainWindow(QMainWindow):
    def __init__(
        self,
        persona: Persona,
        system_service: SystemService,
        controller: AssistantController,
    ) -> None:
        super().__init__()
        self.persona = persona
        self.system_service = system_service
        self.controller = controller
        self.state = AssistantState.STANDBY

        self.setWindowTitle(persona.assistant_name)
        self.setMinimumSize(820, 680)

        self.title_label = QLabel(persona.assistant_name.upper())
        self.title_label.setObjectName("assistantTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clock_label = QLabel()
        self.clock_label.setObjectName("clock")
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel()
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.system_label = QLabel()
        self.system_label.setObjectName("systemStatus")
        self.system_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conversation = QTextBrowser()
        self.conversation.setObjectName("conversation")
        self.conversation.setOpenExternalLinks(False)

        self.command_input = QLineEdit()
        self.command_input.setObjectName("commandInput")
        self.command_input.setPlaceholderText(
            f'Type a command, for example: "{persona.wake_word}, open Spotify"'
        )
        self.command_input.setClearButtonEnabled(True)
        self.command_input.returnPressed.connect(self.submit_command)

        self.command_button = QPushButton("SEND")
        self.command_button.clicked.connect(self.submit_command)

        self.activate_button = QPushButton("ACTIVATE")
        self.activate_button.clicked.connect(self.activate)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.addWidget(self.command_input, 1)
        input_layout.addWidget(self.command_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(self.clock_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.system_label)
        layout.addWidget(self.conversation, 1)
        layout.addLayout(input_layout)
        layout.addWidget(self.activate_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_dashboard)
        self.timer.start(1000)
        self.refresh_dashboard()
        self.set_state(AssistantState.STANDBY)
        self.append_assistant_message(self.controller.greeting())
        self.command_input.setFocus()

    def set_state(self, state: AssistantState, detail: str | None = None) -> None:
        self.state = state
        text = state.value if not detail else f"{state.value} — {detail}"
        self.status_label.setText(text)
        self.status_label.setProperty("assistantState", state.value.lower())
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    def refresh_dashboard(self) -> None:
        now = datetime.now()
        self.clock_label.setText(now.strftime("%H:%M:%S   |   %A, %d %B %Y"))
        snapshot = self.system_service.snapshot()
        self.system_label.setText(
            f"CPU {snapshot.cpu_percent:.0f}%   |   MEMORY {snapshot.memory_percent:.0f}%"
        )

    def activate(self) -> None:
        phrase = self.persona.phrases.get("wake_response", "I'm listening.")
        self.set_state(AssistantState.LISTENING, phrase)
        self.append_assistant_message(phrase)
        self.command_input.setFocus()
        QTimer.singleShot(2500, self._return_to_standby_if_listening)

    def submit_command(self) -> None:
        command = self.command_input.text().strip()
        if not command:
            self.set_state(AssistantState.LISTENING, "Please enter a command.")
            self.command_input.setFocus()
            return

        self.command_input.clear()
        self.append_user_message(command)
        self.set_state(AssistantState.PROCESSING)
        result = self.controller.process(command)
        self.append_assistant_message(result.message, is_error=not result.success)

        if result.success:
            self.set_state(AssistantState.SPEAKING, result.message)
        else:
            self.set_state(AssistantState.ERROR, result.message)

        if result.should_close:
            QTimer.singleShot(900, self._quit_application)
        else:
            QTimer.singleShot(2200, lambda: self.set_state(AssistantState.STANDBY))
            self.command_input.setFocus()

    def append_user_message(self, message: str) -> None:
        self._append_message("YOU", message, "userMessage")

    def append_assistant_message(self, message: str, is_error: bool = False) -> None:
        css_class = "errorMessage" if is_error else "assistantMessage"
        self._append_message(self.persona.assistant_name.upper(), message, css_class)

    def _append_message(self, sender: str, message: str, css_class: str) -> None:
        self.conversation.append(
            f'<div class="message {css_class}">'
            f'<span class="sender">{escape(sender)}</span><br>'
            f'<span>{escape(message)}</span></div><br>'
        )
        scrollbar = self.conversation.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _return_to_standby_if_listening(self) -> None:
        if self.state is AssistantState.LISTENING:
            self.set_state(AssistantState.STANDBY)

    @staticmethod
    def _quit_application() -> None:
        application = QApplication.instance()
        if application is not None:
            application.quit()
