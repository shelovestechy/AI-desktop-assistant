# AI Desktop Assistant

A privacy-first AI desktop assistant for Windows.

The first private build uses a configurable **Jarvis** persona as a personal gift. The application core must remain brand-neutral so the assistant name, wake word, voice, phrases, commands and visual theme can later be replaced without rewriting the engine.

## Product principles

- Privacy by default
- Local processing when practical
- Cloud services only when explicitly enabled
- Least-privilege integrations
- No arbitrary command or script execution
- User confirmation before state-changing or security-sensitive actions
- Clear microphone status whenever wake-word detection is enabled
- Useful notifications, minimal interruption

## Current milestone

The application now:

1. Loads assistant identity and theme from configuration.
2. Displays a PyQt6 dashboard with time, CPU and memory usage.
3. Accepts typed commands with or without the configured wake word.
4. Routes commands through an explicit allowlist.
5. Opens ChatGPT, Spotify and Windows Security.
6. Reports basic system status.
7. Rejects unknown commands instead of executing arbitrary input.
8. Runs automated command-router tests in GitHub Actions.

Current commands include:

- `Jarvis, open ChatGPT`
- `Jarvis, open Spotify`
- `Jarvis, open Windows Security`
- `Jarvis, show system status`
- `Jarvis, close assistant`

## Local development

```powershell
git clone https://github.com/shelovestechy/AI-desktop-assistant.git
cd AI-desktop-assistant

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e ".[dev]"

ai-desktop-assistant
```

Run tests with:

```powershell
pytest -q
```

## Planned modules

- Desktop HUD and settings
- Voice activation, speech-to-text and text-to-speech
- ChatGPT application handoff
- Read-only email summaries
- Weather and rain alerts
- Configurable news sources, topics and keywords
- Spotify playlists linked to user-defined modes
- Calendar and reminders
- Microsoft Defender and Windows security status
- Local preferences and approved learning

## Branding and assets

No Marvel, Iron Man, movie audio, logos, fonts or copied HUD assets are included. The gift edition may be called Jarvis privately, but all graphics, sounds and code are created independently or used under a verified compatible license.

## Status

Early development. Private repository.
