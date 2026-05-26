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

### E. WebSocket Networking Patterns
The networking is powered by high-performance **WebSockets** running over TCP.
- **Default Listening Port:** Both client and server connect/listen on WebSocket port `10000` (over unencrypted `ws://` locally, or secure `wss://` when hosted on Render).
- **Client Module:** Always configure IP and Port properties within `src/zero_hour_assault/net.py` dynamically, defaulting to `localhost` and `10000` respectively.

---

## 3. Persistent Safety Bypasses & DB Accounts

For developer convenience during local iterations:
1. **Email & Hardware Auth Bypass:** Keep the email registration and hardware ID validation code disabled in `server/zhaserver.py`. Allow new developer/tester accounts to log in instantly.
2. **Admin Character Role (`0user`):** The default testing account is named `0user`. Keep its developer flag enabled by writing/updating files in `server/chars/0user/` with `developer = True` or similar boolean options.

---

## 4. Map Management, Architecture & Editing Protocols

All maps in Zero Hour Assault are completely text-based, rendering visual, acoustic, and physical features for player navigation. Because it is an audio-game, sound design, step textures, and correct coordinate grids are vital to player orientation.

### A. File Locations
* **Map Datastore:** All maps reside in `server/maps/` as `.map` files (e.g., `lobby.map`).
* **Client-Side Parser:** Handled by [map.py](file:///e:/games/src/zero_hour_assault/src/zero_hour_assault/map.py) in the `load_map(mdata)` function.
* **Server-Side Parser:** Handled by [map.py](file:///e:/games/src/zero_hour_assault/server/map.py) and [zhaserver.py](file:///e:/games/src/zero_hour_assault/server/zhaserver.py). 

### B. Core Map Syntax & Directives
Each line in a `.map` file defines a specific asset, collider, or zone. Comments are denoted with a standard `//` prefix.

1. **Map Metadata**:
   * `mapname:<name>`: Registers the current map.
   * `maxx:<X>`, `maxy:<Y>`, `maxz:<Z>`: Defines absolute grid bounds (typically 100x100x100).

2. **Step Surfaces & Colliders (`platform`)**:
   * Format: `platform:minx:maxx:miny:maxy:minz:maxz:tiletype` (or 7-argument format `platform:minx:maxx:miny:maxy:z:tiletype`).
   * When walking on these coordinates, the player's footsteps play step sounds corresponding to `tiletype` (e.g. `hardwood`, `grass2`, `gravel2`, `ceramic2`).
   * **Walls & Collisions:** If `tiletype` starts with or contains `"wall"` (e.g., `wallbrick`, `wallbuilding3`), it registers as a blocking collider. Walking into it triggers wall-bump sounds and restricts movement.

3. **Slope Climbing (`staircase`)**:
   * Format: `staircase:minx:maxx:miny:maxy:minz:maxz:tiletype:axis:reverse`
   * Automatically moves the player vertically along the slope axis (`x` or `y`) without requiring manual climb keys. Set `reverse` to `1` or `0` to invert slope height direction.

4. **Interactive Portals & Doors (`door`)**:
   * Format: `door:minx:maxx:miny:maxy:minz:maxz:finishx:finishy:finishz:speed:open_sound.ogg:close_sound.ogg`
   * Automatically triggers when a player steps onto `(minx, miny, minz)`. It locks controls, plays the open sound, slides/teleports the player to `(finishx, finishy, finishz)` step-by-step at the specified speed, and plays the close sound.

5. **Audio Sources & Ambiences (`src` & `amb`)**:
   * **3D Audio Source (`src`):** `src:minx:maxx:miny:maxy:minz:maxz:soundfile.ogg:volume`
     Spawns a 3D audio emitter at `(minx, miny, minz)` that pans and scales in volume based on player distance.
   * **2D Ambient Loop (`amb`):** `amb:minx:maxx:miny:maxy:minz:maxz:soundfile.ogg:volume`
     Plays stationary looping background ambience when the player enters the designated boundary (e.g., `birds2.ogg`, `cafe.ogg`).

6. **Interactive Chests & Signs**:
   * **Chests (`chest`):** `chest:x:y:z`
     Renders an interactive loot chest at `(x,y,z)`. The server's chest loop automatically instantiates, manages, and spawns items in these chests on server startup.
   * **Signs (`sign`):** `sign:x:y:z:message`
     Displays/speaks `message` when the player interacts with it at `(x, y, z)`.

7. **Acoustic Environment (`reverb` & `echo`)**:
   * Renders the EAX OpenAL reverb and echo parameters inside specified coordinate boundaries to give the room an indoor hall, cave, or outdoor acoustic depth.

### C. Map Development Rules for Agents
* **Maintain Critical Coordinates:** Always preserve critical system map nodes (e.g., the Match Menu area in `lobby.map` MUST remain at `(5, 0, 0)`).
* **Asset Validation:** Ensure all tile types and sound filenames exist in the resources folders (see `tiletypes` list in client `zero_hour_assault.py` and unpacked files inside `unpacked_sounds/`).
* **Keep Teleports Safe:** Avoid placing teleports that trap the player or dump them into solid wall colliders. Always verify entry and exit coordinates.

---

## 5. Codebase Modularization & Dual-Binder System (Critical)

To prevent flat-directory clutter (where directories hold 50+ files) and avoid monolithic files over 100 KB, both the Client (`src/zero_hour_assault/`) and Server (`server/modules/`) have been organized into specialized subdirectories, using a **Dynamic Path Resolution** and a **Dual-Binder Namespace** system.

### A. Directory Restructuring
Modules are organized into functional subdirectories to make navigating the project clean and intuitive:
*   **Client Subdirectories (`src/zero_hour_assault/`)**:
    *   `core/`: Lifecycle modules, coordinate loops (`zh_client_core.py`, `zh_client_net.py`, `zh_client_gameplay.py`, `zh_client_ui.py`).
    *   `audio/`: HRTF audio engines, OpenAL, sound pools (`sound.py`, `oal.py`...).
    *   `ui/`: Menu systems, dialog inputs (`menu.py`, `dlg.py`...).
    *   `net/`: Network updaters, ping systems (`net.py`, `network.py`...).
    *   `utils/`: Shared files, map variables, inventory (`map.py`, `inventory.py`...).
*   **Server Subdirectories (`server/modules/`)**:
    *   `core/`: Core engine, persistence, auth (`zh_core.py`, `zh_persistence.py`, `zh_auth.py`...).
    *   `net/`: Network handlers, chat channels (`network.py`, `zh_net_chat.py`, `zh_net_gameplay_*`...).
    *   `entities/`: Active gameplay entities (`player.py`, `zombie.py`, `weapon.py`...).
    *   `utils/`: Shared mathematical formulas, logging handlers (`zh_utils.py`, `rotation.py`...).

### B. Dynamic Subfolder Resolution
On startup, the entry points (`zero_hour_assault.py` for client and `zhaserver.py` for server) dynamically detect all these subdirectories and register them in `sys.path`. This enables standard, flat-style imports (`import player`, `import sound`) to continue compiling perfectly across all subdirectories with **zero import refactoring required**:
```python
# Inserted at the top of zhaserver.py / zero_hour_assault.py
import sys
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
subdirs = ['core', 'net', 'entities', 'utils', 'audio', 'ui']
for subdir in subdirs:
    p = os.path.join(ROOT_DIR, subdir)
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
```

### C. The Dual-Binder Namespace System
To support massive code splitting while keeping all functions and global variables synchronized across separate modules at runtime, a **Dual-Binder namespace mapping** is executed by the entry coordinators:

1.  **Top Binder (Before local assignments)**:
    It imports all split modules and merges their internal functions/classes directly into the coordinator's module dictionary. This ensures that compiler and runtime checks in the main files successfully locate split functions without raising `NameError`.
    ```python
    import types
    import zh_client_core
    ...
    submodules = [zh_client_core, ...]
    shared_globals_top = {}
    for mod in submodules:
        for name, val in mod.__dict__.items():
            if not name.startswith('__') and not isinstance(val, types.ModuleType):
                shared_globals_top[name] = val
    sys.modules[__name__].__dict__.update(shared_globals_top)
    ```

2.  **Bottom Binder (At the end of the entry point)**:
    It extracts the final, fully-resolved global namespace of the coordinator (including all local variables, global parameters, parsed structures, and native imports) and dynamically pushes it back into the submodules' dicts.
    ```python
    shared_globals_bottom = {}
    for name, val in sys.modules[__name__].__dict__.items():
        if not name.startswith('__') and not isinstance(val, types.ModuleType):
            shared_globals_bottom[name] = val
    for mod in submodules:
        mod.__dict__.update(shared_globals_bottom)
    ```

### D. Critical Guidelines for Developer Agents
*   **Write Code Normally**: When you are editing or adding logic in submodules (e.g. `zh_client_gameplay.py` or `zh_auth.py`), you can call any coordinator global variable (`g`), external package (`pygame`, `opuslib`), or other submodule functions (`speak()`, `send_reliable()`) directly exactly as if you were in a single flat file. The Dual-Binder automatically guarantees it resolves at runtime!
*   **Do Not Manually Circular Import**: Never introduce direct circular imports (e.g., trying to do `import zero_hour_assault` inside a client submodule). Defer entirely to the Dual-Binder to sync the scopes.

---

## 🤖 Agent System Prompt Context Override

When you are invoked on this codebase, inject this instruction set into your execution model:

```text
You are an expert audio-game developer agent specializing in standard Python packaging, ctypes DLL configuration, WebSocket socket programming, and text-based coordinate map design.

Rules:
1. Always use the `uv` tool for package operations and script executions. Strictly use `uv run <script>` to execute scripts and `uv add <package>` to manage dependencies. Do NOT run raw python commands directly.
2. Keep pathing environment-agnostic using dynamic parent paths relative to __file__.
3. Always call `os.add_dll_directory` on Windows before wrapping native libraries.
4. Maintain active safety bypasses (disabled hardware/email verifications) to prevent developer lockout.
5. Track heavy binaries (like sounds.dat) using Git LFS. Never commit raw directories containing raw audio assets.
6. Before making any non-trivial modifications, verify existing server network ports (10000) and keep logging highly informative.
7. Always check coordinate integrity and OpenAL asset references when designing, editing, or validating text-based map layouts.
```
do not commit in Git every time unless the user says. After making changes, only commit if the user tells you to commit, otherwise do not do it.
