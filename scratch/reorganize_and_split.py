import ast
import os
import shutil
import re

def normalize_indent(chunk_lines, target_indent=1):
    # Find how many leading tabs or spaces are in the first non-empty line
    leading_tabs = 0
    for line in chunk_lines:
        if line.strip():
            leading_tabs = len(line) - len(line.lstrip('\t'))
            break
            
    strip_count = leading_tabs - target_indent
    if strip_count <= 0:
        return chunk_lines
        
    normalized_lines = []
    for line in chunk_lines:
        if line.startswith('\t' * strip_count):
            normalized_lines.append(line[strip_count:])
        else:
            normalized_lines.append(line.lstrip('\t'))
    return normalized_lines

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    client_dir = os.path.join(root_dir, "src", "zero_hour_assault")
    server_dir = os.path.join(root_dir, "server")
    server_modules_dir = os.path.join(server_dir, "modules")
    
    print(f"[*] Root Directory: {root_dir}")
    print(f"[*] Client Directory: {client_dir}")
    print(f"[*] Server Directory: {server_dir}")
    print(f"[*] Server Modules: {server_modules_dir}")
    
    # ----------------- 1. BACKUP & PREPARATION -----------------
    client_bak_path = os.path.join(client_dir, "zero_hour_assault.py.bak")
    if not os.path.exists(client_bak_path):
        print(f"[!] Warning: zero_hour_assault.py.bak not found, copying from original...")
        shutil.copy2(os.path.join(client_dir, "zero_hour_assault.py"), client_bak_path)
        
    with open(client_bak_path, "r", encoding="utf-8-sig") as f:
        source_code = f.read()
        
    lines = source_code.splitlines(keepends=True)
    tree = ast.parse(source_code)
    
    # ----------------- 2. CLIENT SPLITTING CONFIG -----------------
    target_mapping = {
        # zh_client_core
        "main": "zh_client_core",
        "mainloop": "zh_client_core",
        "game": "zh_client_core",
        "exitfunction": "zh_client_core",
        "readprefs": "zh_client_core",
        "writeprefs": "zh_client_core",
        "handle_exception": "zh_client_core",
        "check_if_already_running": "zh_client_core",

        # zh_client_net
        "netloop": "zh_client_net",
        "play_voice_pcm": "zh_client_net",
        "init_voicechat_player": "zh_client_net",
        "play_for_voicechat": "zh_client_net",
        "play_for_voicechat2": "zh_client_net",
        "handle_voicechat_data": "zh_client_net",
        "handle_voicechat_data2": "zh_client_net",
        "reinit_voicechat": "zh_client_net",
        "change_voicechat_volume": "zh_client_net",
        "record_voice": "zh_client_net",
        "record_voice2": "zh_client_net",

        # zh_client_gameplay
        "zeroloop": "zh_client_gameplay",
        "positions": "zh_client_gameplay",
        "checkloc": "zh_client_gameplay",
        "doorcheck": "zh_client_gameplay",
        "dloop": "zh_client_gameplay",
        "dropen": "zh_client_gameplay",
        "drclose": "zh_client_gameplay",
        "drmoving": "zh_client_gameplay",
        "walking": "zh_client_gameplay",
        "fallloop": "zh_client_gameplay",
        "fallcheck": "zh_client_gameplay",
        "fallingloop": "zh_client_gameplay",
        "death": "zh_client_gameplay",
        "reset": "zh_client_gameplay",
        "alt_is_down": "zh_client_gameplay",
        "shift_is_down": "zh_client_gameplay",
        "altdown": "zh_client_gameplay",
        "control_is_down": "zh_client_gameplay",
        "left_control_is_down": "zh_client_gameplay",
        "right_control_is_down": "zh_client_gameplay",
        "joystick_button_pressed": "zh_client_gameplay",
        "joystick_button_down": "zh_client_gameplay",
        "joystick_button_released": "zh_client_gameplay",
        "joystick_button_up": "zh_client_gameplay",
        "waitjoyhat": "zh_client_gameplay",
        "is_cheater": "zh_client_gameplay",
        "file_get_hash_sha256": "zh_client_gameplay",
        "is_vm": "zh_client_gameplay",
        "Detector": "zh_client_gameplay",
        "VPDError": "zh_client_gameplay",

        # zh_client_ui
        "binput": "zh_client_ui",
        "builder_input": "zh_client_ui",
        "delinear": "zh_client_ui",
        "serverside_menu": "zh_client_ui",
        "plattypemenu": "zh_client_ui",
        "plattypemenuw": "zh_client_ui",
        "list_ambiences": "zh_client_ui",
        "addplattypes": "zh_client_ui",
        "addplattypesw": "zh_client_ui",
        "plm": "zh_client_ui",
        "dummy": "zh_client_ui",
        "matchteammenu": "zh_client_ui",
        "zonemenu": "zh_client_ui",
        "invmenu": "zh_client_ui",
        "invclb": "zh_client_ui",
        "friendpm": "zh_client_ui",
        "youtubesearch": "zh_client_ui",
        "serverbox": "zh_client_ui",
        "getmotd": "zh_client_ui",
        "jawscheck": "zh_client_ui",
        "get_installed_jaws_versions": "zh_client_ui",
        "get_user_languages": "zh_client_ui",
        "install_language": "zh_client_ui",
        "stn": "zh_client_ui",
        "calculate_distance": "zh_client_ui",
        "is_sound_number": "zh_client_ui",
        "mouse_update": "zh_client_ui",
        "mouse_down": "zh_client_ui",
        "mouse_pressed": "zh_client_ui",
        "autotracktoggle": "zh_client_ui",
        "get_aim_str": "zh_client_ui",
        "notifycb": "zh_client_ui",
        "get_max_aim": "zh_client_ui",
        "get_firetime": "zh_client_ui",
        "get_firetime2": "zh_client_ui",
        "amplify_audio_data": "zh_client_ui",
        "get_rain_sound": "zh_client_ui",
        "get_rain_sound_camera": "zh_client_ui",
        "play_audio": "zh_client_ui",
        "play_audio2": "zh_client_ui",
        "strtobool": "zh_client_ui",
    }
    
    extracted = {
        "zh_client_core": [],
        "zh_client_net": [],
        "zh_client_gameplay": [],
        "zh_client_ui": []
    }
    
    omit_lines = [False] * len(lines)
    
    # ----------------- 3. PARSE AND EXTRACT CLIENT SUBMODULES -----------------
    print("[*] Extracting client functions and classes...")
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            dest = target_mapping.get(name)
            if dest:
                start_line = node.lineno
                end_line = node.end_lineno
                
                # Capture any developer comments right above the node
                start_idx = start_line - 1
                while start_idx > 0 and lines[start_idx - 1].strip().startswith("#"):
                    start_idx -= 1
                    
                node_lines = lines[start_idx : end_line]
                node_source = "".join(node_lines)
                
                extracted[dest].append(node_source)
                
                # Mark as omitted in coordinator
                for idx in range(start_idx, end_line):
                    omit_lines[idx] = True
                    
    # Write client split submodules temporarily inside client_dir
    for mod_name, code_blocks in extracted.items():
        mod_path = os.path.join(client_dir, f"{mod_name}.py")
        content = "import globals as g\nimport os\nimport time\nimport sys\nimport math\n\n" + "\n\n".join(code_blocks) + "\n"
        with open(mod_path, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"[OK] Extracted submodule: {mod_path} ({len(code_blocks)} blocks)")

    # ----------------- 4. RECREATE CLIENT COORDINATOR -----------------
    coordinator_lines = []
    for idx, line in enumerate(lines):
        if not omit_lines[idx]:
            coordinator_lines.append(line)
            
    top_binder = (
        "# --- AUTOMATIC PATH RESOLUTION AND MODULE REGISTRATION ---\n"
        "import sys\n"
        "import os\n"
        "CLIENT_DIR = os.path.dirname(os.path.abspath(__file__))\n"
        "subdirs = ['core', 'audio', 'ui', 'net', 'utils']\n"
        "for subdir in subdirs:\n"
        "    p = os.path.join(CLIENT_DIR, subdir)\n"
        "    if os.path.isdir(p) and p not in sys.path:\n"
        "        sys.path.insert(0, p)\n\n"
        "# --- AUTOMATIC TOP MODULE BINDER ---\n"
        "import types\n"
        "import zh_client_core\n"
        "import zh_client_net\n"
        "import zh_client_gameplay\n"
        "import zh_client_ui\n\n"
        "submodules = [\n"
        "    zh_client_core, zh_client_net, zh_client_gameplay, zh_client_ui\n"
        "]\n"
        "shared_globals_top = {}\n"
        "for mod in submodules:\n"
        "    for name, val in mod.__dict__.items():\n"
        "        if not name.startswith('__') and not isinstance(val, types.ModuleType):\n"
        "            shared_globals_top[name] = val\n"
        "sys.modules[__name__].__dict__.update(shared_globals_top)\n\n"
    )
    
    bottom_binder = (
        "\n\n# --- AUTOMATIC BOTTOM MODULE BINDER ---\n"
        "shared_globals_bottom = {}\n"
        "for name, val in sys.modules[__name__].__dict__.items():\n"
        "    if not name.startswith('__') and not isinstance(val, types.ModuleType):\n"
        "        shared_globals_bottom[name] = val\n"
        "for mod in submodules:\n"
        "    mod.__dict__.update(shared_globals_bottom)\n"
    )
    
    new_coordinator_content = top_binder + "".join(coordinator_lines) + bottom_binder
    coordinator_path = os.path.join(client_dir, "zero_hour_assault.py")
    with open(coordinator_path, "w", encoding="utf-8") as out:
        out.write(new_coordinator_content)
    print(f"[OK] Re-created client coordinator: {coordinator_path}")

    # ----------------- 5. REORGANIZE CLIENT DIRECTORY -----------------
    print("[*] Reorganizing client subdirectories...")
    client_mapping = {
        "core": [
            "zero_hour_assault.py", "zh_client_core.py", "zh_client_net.py",
            "zh_client_gameplay.py", "zh_client_ui.py", "globals.py", "constants.py",
            "events.py", "main.py"
        ],
        "audio": [
            "sound.py", "sound_pool.py", "sound_positioning.py", "source.py", "speech.py",
            "audio.py", "fmod_audio.py", "oal.py", "phonon_test.py", "sound_len_checker.py"
        ],
        "ui": [
            "menu.py", "menu_system.py", "dlg.py", "dlgplay.py", "ticket_dialogs.py",
            "input.py", "joystick.py", "key_hold.py"
        ],
        "net": [
            "net.py", "network.py", "enet_ping.py", "ipfind.py", "telegram_ticket.py", "updater.py"
        ],
        "utils": [
            "Miscellaneous.py", "buffer.py", "cid.py", "door.py", "downloader.py",
            "file_directories.py", "getfiles.py", "inventory.py", "map.py", "player.py",
            "rotation.py", "savedata.py", "security.py", "sign.py", "timer.py",
            "translation.py", "variable_management.py", "vector.py", "virtualizer.py",
            "moving_sound_client_handler.py", "pack_creator.py", "pack_extracter.py",
            "pack_file.py", "pack_lister.py", "internet.py"
        ]
    }
    
    # Create client folders
    for sub in client_mapping.keys():
        os.makedirs(os.path.join(client_dir, sub), exist_ok=True)
        
    # Move files, except zero_hour_assault.py itself which MUST stay at client root!
    for sub, files in client_mapping.items():
        for filename in files:
            src_file = os.path.join(client_dir, filename)
            if os.path.exists(src_file):
                if filename == "zero_hour_assault.py":
                    # Keep at package root
                    continue
                dest_file = os.path.join(client_dir, sub, filename)
                shutil.move(src_file, dest_file)
                print(f"  Moved client: {filename} -> {sub}/")
                
    # ----------------- 6. REORGANIZE SERVER MODULES -----------------
    print("[*] Reorganizing server modules subdirectories...")
    server_mapping = {
        "core": [
            "zh_core.py", "zh_auth.py", "zh_persistence.py", "zh_gameplay.py",
            "base.py", "group.py", "community.py", "compban.py", "compid_handler.py"
        ],
        "net": [
            "network.py", "transit.py", "zh_net_chat.py", "zh_net_others.py",
            "zh_net_gameplay_1.py", "zh_net_gameplay_2.py", "zh_net_gameplay_3.py",
            "zh_net_gameplay_4.py", "zh_net_gameplay_5.py", "zh_net_gameplay_6.py",
            "moving_sound_serverside_handler.py"
        ],
        "entities": [
            "player.py", "zombie.py", "npc.py", "weapon.py", "grenade.py",
            "bike.py", "motor.py", "timebomb.py", "mine.py", "zk.py",
            "loot.py", "flag.py", "item.py", "timeditem.py", "bodyfall.py"
        ],
        "utils": [
            "zh_utils.py", "globals.py", "timer.py", "variable_management.py",
            "file_directories.py", "vector.py", "rotation.py", "pathfinder.py",
            "performance_monitor.py", "packchecker.py", "getfiles.py", "guns.py",
            "internet.py", "map.py", "match.py"
        ]
    }
    
    # Create server subfolders inside server/modules/
    for sub in server_mapping.keys():
        os.makedirs(os.path.join(server_modules_dir, sub), exist_ok=True)
        
    # Move server files
    for sub, files in server_mapping.items():
        for filename in files:
            src_file = os.path.join(server_modules_dir, filename)
            if os.path.exists(src_file):
                dest_file = os.path.join(server_modules_dir, sub, filename)
                shutil.move(src_file, dest_file)
                print(f"  Moved server: {filename} -> {sub}/")
                
    # ----------------- 7. UPDATE SERVER RESOLVER IN zhaserver.py -----------------
    zhaserver_path = os.path.join(server_dir, "zhaserver.py")
    with open(zhaserver_path, "r", encoding="utf-8") as f:
        zha_content = f.read()
        
    # Inject subdirectory registration in zhaserver.py pathing header
    old_header = """MODULES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)"""

    new_header = """MODULES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))
subdirs = ['core', 'net', 'entities', 'utils']
for subdir in subdirs:
    p = os.path.join(MODULES_DIR, subdir)
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)"""

    if old_header in zha_content:
        zha_content = zha_content.replace(old_header, new_header)
        with open(zhaserver_path, "w", encoding="utf-8") as out:
            out.write(zha_content)
        print("[OK] Updated zhaserver.py Dynamic Resolver successfully!")
    else:
        print("[!] zhaserver.py custom pathing header not matched, inserting manually...")
        # Fallback regex replace
        zha_content = re.sub(
            r"MODULES_DIR\s*=\s*os\.path\.abspath.*sys\.path\.insert\(0,\s*MODULES_DIR\)",
            new_header,
            zha_content,
            flags=re.DOTALL
        )
        with open(zhaserver_path, "w", encoding="utf-8") as out:
            out.write(zha_content)
            
    print("\n[SUCCESS] Automated split and reorganization completed successfully!")

if __name__ == '__main__':
    main()
