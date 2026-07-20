from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from assistant_app.core.config import Persona
from assistant_app.core.state import AssistantState
from assistant_app.services.system_service import SystemService


class MainWindow(QMainWindow):
    def __init__(self, persona: Persona, system_service: SystemService) -> None:
        super().__init__()
        self.persona = persona
        self.system_service = system_service
        self.state = AssistantState.STANDBY

        self.setWindowTitle(persona.assistant_name)
        self.setMinimumSize(760, 520)

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

        self.activate_button = QPushButton("ACTIVATE")
        self.activate_button.clicked.connect(self.activate)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addWidget(self.clock_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.system_label)
        layout.addWidget(self.activate_button)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_dashboard)
        self.timer.start(1000)
        self.refresh_dashboard()
        self.set_state(AssistantState.STANDBY)

    def set_state(self, state: AssistantState, detail: str | None = None) -> None:
        self.state = state
        text = state.value if not detail else f"{state.value} — {detail}"
        self.status_label.setText(text)
        self.status_label.setProperty("assistantState", state.value.lower())
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    def refresh_dashboard(self) -> None:
        now = datetime.now()
        self.clock_label.setText(now.strftime("%H:%M:%S\n%A, %d %B %Y"))
        snapshot = self.system_service.snapshot()
        self.system_label.setText(
            f"CPU {snapshot.cpu_percent:.0f}%   |   MEMORY {snapshot.memory_percent:.0f}%"
        )

    def activate(self) -> None:
        phrase = self.persona.phrases.get("wake_response", "I'm listening.")
        self.set_state(AssistantState.LISTENING, phrase)
        QTimer.singleShot(2500, lambda: self.set_state(AssistantState.STANDBY))
