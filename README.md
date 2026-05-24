# Zero Hour Assault

Welcome to the public source release of **Zero Hour Assault**, a high-fidelity Python-based audio game!

This repository has been fully restructured, cleaned, and migrated to the **`uv`** project manager. You can now bootstrap and run both the client and the server with zero configuration.

---

## Quick Start

### Prerequisites
Make sure you have **`uv`** installed. If not, install it using:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Running the Game

### 1. Launching the Game Client
To automatically set up the virtual environment, install all required dependencies (including native audio wrappers), and launch the game client:
```bash
uv run python src/zero_hour_assault/main.py
```

### 2. Launching the Game Server
To boot up the reliable UDP server network loop:
```bash
uv run python server/zhaserver.py
```

---

## Key Features of This Release
- **Standardized UV Integration:** Python 3.12 target ensures pre-compiled binary compatibility for Windows without requiring any local C++ compiling tools.
- **Pristine Project Structure:** Clean separation of client source code (`src/zero_hour_assault/`), assets, native DLLs, and server-side code (`server/`).
- **Painless Dependencies:** All third-party libraries (`pygame`, `wxpython`, `PyAudio`, `pyenet`, `soundfile`, `python-vlc`, etc.) are managed dynamically and safely through the standard PyPI pipeline.
- **Bypassed Updater Logic:** Automatic internet version checks and file overwrites are commented out so the source tree remains completely under your control.
