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

## First milestone

Create a Windows desktop application that:

1. Loads assistant identity and theme from configuration.
2. Displays a PyQt6 dashboard with time and system status.
3. Supports activation by keyboard shortcut.
4. Optionally supports a locally detected wake word.
5. Routes a small allowlisted set of commands.
6. Opens ChatGPT, Spotify and Windows Security.
7. Keeps an audit trail without storing message or email contents.

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
