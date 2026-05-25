# AGENTS.md - Developer Agent Instructions

Welcome, Agent. You are pair-programming with the Lead Architect on the **Zero Hour Assault** codebase. This guide outlines the project structure, standard code patterns, Windows-specific DLL constraints, networking protocols, and safety bypasses you must adhere to. 

Read and strictly follow these rules to maintain codebase integrity and consistency.

---

## 1. Directory Structure & File Placement

Do not break the unified package structure of the project:
- **Client Code Package (`src/zero_hour_assault/`):** All new or modified client modules must reside in this directory. Never drop standalone python scripts into the root folder unless they are tools/scripts for asset management (e.g. `unpack_sounds.py`).
- **Server Code Package (`server/`):** All server modules, map databases, and character models reside here.
- **Dependencies Management:** All external Python dependencies must be declared in [pyproject.toml](file:///e:/games/src/zero_hour_assault/pyproject.toml). **Do not** manually copy/vendor third-party package directories into the project. Always install via the `uv` tool:
  ```powershell
  uv add <package-name>
  ```

---

## 2. Standard Coding Conventions & Patterns

### A. Dynamic Path Resolution
Because client modules reside in a nested package namespace (`src/zero_hour_assault/`), files are loaded relative to the root directory. To ensure the game can be launched from any working directory, always resolve paths dynamically:
```python
import sys
import os

# Resolve the absolute project root (two levels up from src/zero_hour_assault/...)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Register in sys.path so nested modules resolve imports successfully
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
```

### B. Windows DLL Loading Protocol (Critical)
Modern Python on Windows (Python 3.8+) does not search the current working directory for DLLs referenced by `ctypes.CDLL`. To load libraries such as `opus.dll`, `OpenAL32.dll`, or `SRAL.dll` successfully, you **must** register the DLL search directories at the entry point:
```python
if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
    # Add root directory where dlls are located
    os.add_dll_directory(ROOT_DIR)
```
Always call `os.add_dll_directory` before attempting imports or loading native binary wrappers.

### C. Media Streaming & Backends
We leverage `pafy` and `youtube-dl` for audio streaming features. Because modern YouTube parsing changes frequently, keep the internal backend active in script headers:
```python
os.environ["PAFY_BACKEND"] = "internal"
```

### D. Game Updaters Bypasses
To prevent the client from overwriting modified development source code with production compiled binaries:
- Keep the `updater.check()` and `updater.sndcheck()` calls safely commented out or bypassed inside client game loops.

### E. ENet UDP Networking Patterns
The networking is powered by `pyenet` (wrapper for the reliable ENet UDP library).
- **Default Listening Port:** Both client and server must connect/listen on UDP port `55918`. Do not change this port without explicit authorization from the Lead Architect.
- **Client Module:** Always configure IP and Port properties within `src/zero_hour_assault/net.py` dynamically, defaulting to `localhost` and `55918` respectively.

---

## 3. Persistent Safety Bypasses & DB Accounts

For developer convenience during local iterations:
1. **Email & Hardware Auth Bypass:** Keep the email registration and hardware ID validation code disabled in `server/zhaserver.py`. Allow new developer/tester accounts to log in instantly.
2. **Admin Character Role (`0user`):** The default testing account is named `0user`. Keep its developer flag enabled by writing/updating files in `server/chars/0user/` with `developer = True` or similar boolean options.

---

## 🤖 Agent System Prompt Context Override

When you are invoked on this codebase, inject this instruction set into your execution model:

```text
You are an expert audio-game developer agent specializing in standard Python packaging, ctypes DLL configuration, and ENet socket programming.

Rules:
1. Keep pathing environment-agnostic using dynamic parent paths relative to __file__.
2. Always call `os.add_dll_directory` on Windows before wrapping native libraries.
3. Manage all dependencies using the `uv` build manager and pyproject.toml.
4. Maintain active safety bypasses (disabled hardware/email verifications) to prevent developer lockout.
5. Track heavy binaries (like sounds.dat) using Git LFS. Never commit raw directories containing raw audio assets.
6. Before making any non-trivial modifications, verify existing server network ports (55918) and keep logging highly informative.
```
Do not use   wev toolevery time. Also, do not commit in Git every time unless the user says. After making changes, only commit if the user tells you to commit, otherwise do not do it.
