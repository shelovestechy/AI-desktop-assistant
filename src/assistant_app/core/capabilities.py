from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    name: str
    example: str
    description: str


CAPABILITIES: tuple[Capability, ...] = (
    Capability("ChatGPT", "open ChatGPT", "Open ChatGPT in the default browser."),
    Capability("Spotify", "open Spotify", "Launch Spotify or open Spotify Web."),
    Capability(
        "Windows Security",
        "open Windows Security",
        "Open the Windows Security application.",
    ),
    Capability(
        "System status",
        "show system status",
        "Report current CPU and memory usage.",
    ),
    Capability("Help", "help", "Show the commands currently available."),
    Capability("Exit", "close assistant", "Close the assistant safely."),
)


def format_capabilities() -> str:
    lines = ["Here is what I can do right now:"]
    lines.extend(
        f"• {capability.name}: {capability.example} — {capability.description}"
        for capability in CAPABILITIES
    )
    return "\n".join(lines)


def compact_capability_examples() -> str:
    return "  |  ".join(capability.example for capability in CAPABILITIES)
