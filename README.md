# AI Desktop Assistant

A small Windows desktop assistant I am building while learning Python, application structure and security-minded automation.

The name says AI, but the current version does not use a language model yet. It uses local and deterministic intent matching. In other words, it only does things I have explicitly allowed it to do. This is less magical, but also less likely to decide that `delete everything` sounds like a reasonable afternoon task.

## What works now

- PyQt6 desktop interface
- typed commands with an optional wake word
- local matching for a few natural-language requests
- an explicit allowlist of available actions
- links to ChatGPT and Spotify
- Windows Security launcher
- read-only CPU and memory status
- configurable assistant name and visual theme
- automated tests on Windows with GitHub Actions

The application rejects unknown commands. It does not pass user input to PowerShell, Command Prompt or another shell.

## Why I am building this

I am interested in what happens when a helpful tool is also allowed to interact with a computer. (Also I am huge Marvel fan and who doesn't want their own little J.A.R.V.I.S. ?)

The interesting part is not only making a button work. I also want to understand:

- which actions should be allowed
- where user confirmation is needed
- how to keep the user interface separate from command logic
- what should stay local
- how failures should be handled without running something unexpected

This is not a finished assistant. It is a working learning project with a deliberately small set of features.

## Safety rules in the current build

1. Commands must be registered before they can run.
2. Natural-language matching can only return an existing registered command.
3. Unknown requests are rejected.
4. System information is read-only.
5. External programs are opened through fixed destinations, not arbitrary user input.
6. Cloud integrations are not enabled by default.

More detail is available in [SECURITY.md](./SECURITY.md).

## Project structure

```text
src/assistant_app/
├── core/       command routing, intent matching and configuration
├── services/   approved application and system actions
└── ui/         PyQt6 desktop interface

config/personas/  public example persona
themes/           visual theme
tests/            command, intent and controller tests
```

## Run locally

The project requires Windows and Python 3.12 or newer.

```powershell
git clone https://github.com/shelovestechy/AI-desktop-assistant.git
cd AI-desktop-assistant

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"

ai-desktop-assistant
```

Run the checks:

```powershell
pytest -q
ruff check .
mypy src
```

## Current limitations

- commands are typed; voice input is not implemented
- intent matching is rule-based and intentionally small
- there is no email, calendar or account integration
- there is no installer yet
- the interface is still an early desktop prototype

## Next things I want to learn

- confirmation before any future state-changing action
- a small local audit log without storing unnecessary personal data
- clearer permission settings for integrations
- voice input with a visible microphone state
- packaging the application for Windows

I would rather add these slowly than build a very impressive security incident generator.
