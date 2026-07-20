from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PERSONA_PATH = PROJECT_ROOT / "config" / "personas" / "jarvis.json"


def load_persona(path: Path = PERSONA_PATH) -> dict[str, Any]:
    """Load assistant identity without coupling the application core to one brand."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return {
            "assistant_name": "Assistant",
            "phrases": {"wake_response": "I'm listening."},
        }

    if not isinstance(data, dict):
        raise ValueError("Persona configuration must contain a JSON object.")
    return data


class MainWindow(QMainWindow):
    def __init__(self, persona: dict[str, Any]) -> None:
        super().__init__()
        self.persona = persona
        self.assistant_name = str(persona.get("assistant_name", "Assistant"))

        self.setWindowTitle(self.assistant_name)
        self.setMinimumSize(760, 520)

        self.title_label = QLabel(self.assistant_name.upper())
        self.title_label.setObjectName("assistantTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clock_label = QLabel()
        self.clock_label.setObjectName("clock")
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("STANDBY")
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.system_label = QLabel()
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

        self.setStyleSheet(
            """
            QMainWindow { background: #050a12; }
            QLabel { color: #bdefff; font-family: 'Segoe UI'; }
            QLabel#assistantTitle { font-size: 42px; font-weight: 600; letter-spacing: 8px; }
            QLabel#clock { font-size: 28px; }
            QLabel#status { font-size: 18px; color: #62d8ff; padding: 18px; }
            QPushButton {
                color: #bdefff;
                background: #0c2638;
                border: 1px solid #62d8ff;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
            }
            QPushButton:hover { background: #123b54; }
            """
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_dashboard)
        self.timer.start(1000)
        self.refresh_dashboard()

    def refresh_dashboard(self) -> None:
        now = datetime.now()
        self.clock_label.setText(now.strftime("%H:%M:%S\n%A, %d %B %Y"))
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent
        self.system_label.setText(f"CPU {cpu:.0f}%   |   MEMORY {memory:.0f}%")

    def activate(self) -> None:
        phrase_data = self.persona.get("phrases", {})
        phrase = "I'm listening."
        if isinstance(phrase_data, dict):
            phrase = str(phrase_data.get("wake_response", phrase))
        self.status_label.setText(f"LISTENING — {phrase}")
        QTimer.singleShot(2500, lambda: self.status_label.setText("STANDBY"))


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow(load_persona())
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
