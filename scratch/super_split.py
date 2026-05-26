import ast
import os
import shutil
import re
import types

def normalize_indent(chunk_lines, target_indent=1):
    # Find how many leading tabs are in the first non-empty line
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
    server_dir = "server"
    modules_dir = os.path.join(server_dir, "modules")
    zhaserver_path = os.path.join(server_dir, "zhaserver.py")
    zhaserver_bak_path = os.path.join(server_dir, "zhaserver.py.bak")
    
    # 1. Ensure modules directory exists
    os.makedirs(modules_dir, exist_ok=True)
    
    # 2. Move all existing python scripts from server/ to server/modules/
    # (except zhaserver.py and zhaserver.py.bak)
    for filename in os.listdir(server_dir):
        if filename.endswith(".py") and filename not in ("zhaserver.py", "zhaserver.py.bak"):
            src_path = os.path.join(server_dir, filename)
            dest_path = os.path.join(modules_dir, filename)
            shutil.move(src_path, dest_path)
            print(f"Moved {src_path} -> {dest_path}")
            
    # 3. Read the original zhaserver.py.bak
    if not os.path.exists(zhaserver_bak_path):
        print(f"Error: {zhaserver_bak_path} not found.")
        return
        
    with open(zhaserver_bak_path, "r", encoding="utf-8-sig") as f:
        source_code = f.read()
    
    lines = source_code.splitlines(keepends=True)
    tree = ast.parse(source_code)
    
    # Complete logical mappings of all 185 functions & classes
    mappings = {
        # zh_core.py (Core Framework Loops)
        "main": "zh_core",
        "gameloops": "zh_core",
        "netloop": "zh_core",
        "garbage_collect": "zh_core",
        "exit": "zh_core",
        "backup": "zh_core",
        "itemdo": "zh_core",
        "iositemdo": "zh_core",

        # zh_auth.py (Auth, login, registration, banning, computers)
        "login": "zh_auth",
        "create": "zh_auth",
        "add_compid": "zh_auth",
        "load_compids": "zh_auth",
        "compid_handlercheck": "zh_auth",
        "is_compbanned": "zh_auth",
        "remove_from_server": "zh_auth",
        "getplayer_by_peer": "zh_auth",
        "get_player_index": "zh_auth",
        "get_player_index_from": "zh_auth",
        "get_player_index_fromnpc": "zh_auth",
        "getpc": "zh_auth",

        # zh_persistence.py (File I/O, Char & State Serialization)
        "charwrite": "zh_persistence",
        "charwriteb": "zh_persistence",
        "save_char": "zh_persistence",
        "save_all_chars": "zh_persistence",
        "file_get_contents": "zh_persistence",
        "save_matches": "zh_persistence",
        "load_matches": "zh_persistence",
        "save_chests": "zh_persistence",
        "load_chests": "zh_persistence",
        "save_electrics": "zh_persistence",
        "load_electrics": "zh_persistence",
        "save_corpses": "zh_persistence",
        "load_corpses": "zh_persistence",
        "save_tickets": "zh_persistence",
        "save_votes": "zh_persistence",
        "save_rain": "zh_persistence",
        "save_ladders": "zh_persistence",
        "save_barricades": "zh_persistence",
        "load_rain": "zh_persistence",
        "load_ladders": "zh_persistence",
        "load_barricades": "zh_persistence",
        "load_tickets": "zh_persistence",
        "load_votes": "zh_persistence",
        "save_timebombs": "zh_persistence",
        "load_timebombs": "zh_persistence",
        "save_zks": "zh_persistence",
        "load_zks": "zh_persistence",
        "save_mines": "zh_persistence",
        "load_mines": "zh_persistence",
        "save_bikes": "zh_persistence",
        "load_bikes": "zh_persistence",
        "save_motors": "zh_persistence",
        "load_motors": "zh_persistence",
        "save_npcs": "zh_persistence",
        "load_npcs": "zh_persistence",
        "save_zombies": "zh_persistence",
        "load_zombies": "zh_persistence",
        "save_timeditems": "zh_persistence",
        "load_timeditems": "zh_persistence",
        "save_groups": "zh_persistence",
        "load_groups": "zh_persistence",
        "save_communitys": "zh_persistence",
        "load_communitys": "zh_persistence",
        "save_group_bases": "zh_persistence",
        "load_group_bases": "zh_persistence",
        "save_items": "zh_persistence",
        "load_items": "zh_persistence",
        "save_flags": "zh_persistence",
        "load_flags": "zh_persistence",
        "load_mailbans": "zh_persistence",
        "save_mailbans": "zh_persistence",
        "is_mailbanned": "zh_persistence",
        "ban_mail": "zh_persistence",

        # zh_gameplay.py (Gameplay variables, maps, combat, movement, entity queries)
        "climb_bus_ladder": "zh_gameplay",
        "play": "zh_gameplay",
        "play2": "zh_gameplay",
        "play_delay": "zh_gameplay",
        "move_player": "zh_gameplay",
        "move_player2": "zh_gameplay",
        "update_map": "zh_gameplay",
        "get_map_data": "zh_gameplay",
        "get_nearest_player": "zh_gameplay",
        "get_nearest_zombie": "zh_gameplay",
        "get_nearest_npc": "zh_gameplay",
        "get_nearest_npc2": "zh_gameplay",
        "setupserver": "zh_gameplay",
        "requires_ammo": "zh_gameplay",
        "get_max_ammo": "zh_gameplay",
        "get_ammotype": "zh_gameplay",
        "get_reloadtime": "zh_gameplay",
        "get_chest_at_player": "zh_gameplay",
        "chestadd": "zh_gameplay",
        "get_corpse_at_player": "zh_gameplay",
        "get_corpse_at_player_length": "zh_gameplay",
        "corpseadd": "zh_gameplay",
        "get_match_name": "zh_gameplay",
        "get_max_values": "zh_gameplay",
        "get_zero_token_amount": "zh_gameplay",
        "match_exists": "zh_gameplay",
        "chest_at": "zh_gameplay",
        "ladder_at": "zh_gameplay",
        "barricade_at": "zh_gameplay",
        "mine_at": "zh_gameplay",
        "get_chest_at": "zh_gameplay",
        "corpse_at": "zh_gameplay",
        "get_corpse_at": "zh_gameplay",
        "get_player_count_in_freedom": "zh_gameplay",
        "get_current_base": "zh_gameplay",
        "get_base_count": "zh_gameplay",
        "update_char_counter": "zh_gameplay",
        "get_match_info": "zh_gameplay",
        "get_drawtime": "zh_gameplay",
        "vote": "zh_gameplay",
        "votecheck": "zh_gameplay",
        "get_task_name": "zh_gameplay",
        "get_task_description": "zh_gameplay",
        "select_random_player_from_freedom_fight_map": "zh_gameplay",
        "get_task_end_time": "zh_gameplay",
        "get_task_max_point": "zh_gameplay",
        "get_task_complete_need": "zh_gameplay",
        "get_corpse_amount_in_map": "zh_gameplay",
        "playmoving": "zh_gameplay",
        "playmoving2": "zh_gameplay",

        # zh_utils.py (Messaging, parsing, notifications, logging, timing)
        "server_menu": "zh_utils",
        "find_directories": "zh_utils",
        "send_menu": "zh_utils",
        "remove_duplicate_mapwalls": "zh_utils",
        "bilet_cevapla": "zh_utils",
        "adminsend": "zh_utils",
        "adminsend2": "zh_utils",
        "adminsendsound": "zh_utils",
        "get_date": "zh_utils",
        "get_time": "zh_utils",
        "developersend": "zh_utils",
        "stn": "zh_utils",
        "send_reliable": "zh_utils",
        "send_plus": "zh_utils",
        "send_plus2": "zh_utils",
        "my_list": "zh_utils",
        "sort_descending": "zh_utils",
        "convert_to_list": "zh_utils",
        "convert_to_list2": "zh_utils",
        "send_serverbox": "zh_utils",
        "get_leader_hit_player": "zh_utils",
        "load_store_data": "zh_utils",
        "load_event_store_data": "zh_utils",
        "get_friend_count": "zh_utils",
        "find_ticket_by_title": "zh_utils",
        "find_ticket_by_id": "zh_utils",
        "get_datetime_difference": "zh_utils",
        "convert_minutes_to_datetime_object": "zh_utils",
        "send_yesno_question": "zh_utils",
        "strtobool": "zh_utils",
        "removefriendadd": "zh_utils",
        "offlinepm": "zh_utils",
        "offlinestaff": "zh_utils",
        "url_encode": "zh_utils",
        "url_decode": "zh_utils",
        "url_get": "zh_utils",
        "make_request": "zh_utils",
        "notify_admins": "zh_utils",
        "make_request2": "zh_utils",
        "notify_admins2": "zh_utils",
        "send_mail": "zh_utils",
        "load_tempmail_domains": "zh_utils",
        "is_tempmail": "zh_utils",
        "ms_to_readable_time": "zh_utils",
        "ms_to_readable_time2": "zh_utils",
        "plural": "zh_utils",
        "get_group": "zh_utils",
        "get_community": "zh_utils",
        "randomstring": "zh_utils",
        "time_difference_exceeds_24_hours": "zh_utils",
        "time_difference_exceeds_1_week": "zh_utils",
        "time_difference_exceeds_2_hours": "zh_utils",
        "url_post2": "zh_utils",
        "minutes_to_timestamp": "zh_utils",
        "ticketcheck": "zh_utils",
        "is_enabled_ticket_mail": "zh_utils",
        "get_current_date": "zh_utils",
        "get_long_name_for_size_unit": "zh_utils",
        "get_file_size": "zh_utils",
        "get_file_size_b": "zh_utils",
        "get_file_size_bit": "zh_utils",
        "convert_size": "zh_utils",
        "convert_size_bit": "zh_utils",
        "get_language_used_count": "zh_utils",
        "get_open_ticket_count": "zh_utils",
        "get_closed_ticket_count": "zh_utils",
        "get_pending_ticket_count": "zh_utils",
    }
    
    extracted = {
        "zh_utils": [],
        "zh_auth": [],
        "zh_persistence": [],
        "zh_gameplay": [],
        "zh_core": []
    }
    
    omit_lines = [False] * len(lines)
    
    # 4. Extract standard modular functions (excluding zhaserver netloop logic)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            dest = mappings.get(name)
            if dest and name != "netloop":  # We handle netloop with highly custom split below
                start_line = node.lineno
                end_line = node.end_lineno
                
                # capture developer comments
                start_idx = start_line - 1
                while start_idx > 0 and lines[start_idx - 1].strip().startswith("#"):
                    start_idx -= 1
                
                node_lines = lines[start_idx : end_line]
                node_source = "".join(node_lines)
                
                extracted[dest].append(node_source)
                
                for idx in range(start_idx, end_line):
                    omit_lines[idx] = True
                    
    # Find netloop line bounds in zhaserver.py.bak
    netloop_start = -1
    netloop_end = -1
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "netloop":
            netloop_start = node.lineno
            netloop_end = node.end_lineno
            break
            
    if netloop_start == -1 or netloop_end == -1:
        print("Error: Could not locate netloop function bounds.")
        return
        
    for idx in range(netloop_start - 1, netloop_end):
        omit_lines[idx] = True
        
    # Standard header for submodules
    header = (
        "import globals as g\n"
        "import os\n"
        "import time\n"
        "import pickle\n"
        "import json\n"
        "import datetime\n"
        "import urllib.parse\n"
        "import requests\n"
        "from threading import Thread\n"
        "from timer import timer\n\n"
    )
    
    # 5. SPLIT THE Monolithic 11,700-line netloop()!
    # - Chat / Admin commands (e.channel == 1)
    # - Gameplay packets (e.channel == 0) -> Split into 6 clean submodules under 80 KB each!
    # - Other channels (2, 5, 6)
    
    # Extract channel 1 lines (approx 921 to 2458)
    chan1_lines = lines[920:2458]
    # Normalize indentation of extracted body to 2 tabs (since nested under if index > -1:)
    chan1_lines_norm = normalize_indent(chan1_lines, target_indent=2)
    
    # Wrap in function with pure tab indentation
    chan1_code = (
        "def handle_channel_1(e):\n"
        "\tglobal languages\n"
        "\tindex = g.get_player_index(e.peer_id)\n"
        "\tif index > -1:\n"
        + "".join(chan1_lines_norm) + "\n"
    )
    with open(os.path.join(modules_dir, "zh_net_chat.py"), "w", encoding="utf-8") as out:
        out.write(header + chan1_code)
        
    # Extract channel 2, 5, 6 lines (approx 2459 to 2709)
    chan_others_lines = lines[2458:2709]
    chan_others_lines_norm = normalize_indent(chan_others_lines, target_indent=1)
    
    chan_others_code = (
        "def handle_channel_others(e):\n"
        "\tglobal languages\n"
        + "".join(chan_others_lines_norm) + "\n"
    )
    with open(os.path.join(modules_dir, "zh_net_others.py"), "w", encoding="utf-8") as out:
        out.write(header + chan_others_code)
        
    # Extract channel 0 gameplay commands (approx 2710 to 12615)
    gameplay_lines = lines[2709:12615]
    
    # Global search of all 89 top-level candidate elif statement indices inside gameplay block
    candidates = []
    for idx, line in enumerate(gameplay_lines):
        line_str = line.rstrip()
        # Regex to match exact top-level elif indentation inside gameplay block (2 or 3 tabs)
        if re.match(r'^\t{2,3}elif\s', line_str):
            candidates.append(idx)
            
    # We split gameplay_lines into 6 parts using the best closest global candidate splits!
    chunk_size = len(gameplay_lines) // 6
    boundaries = [0]
    
    for i in range(1, 6):
        target = i * chunk_size
        # Select the candidate closest to target
        best_candidate = min(candidates, key=lambda x: abs(x - target))
        boundaries.append(best_candidate)
    boundaries.append(len(gameplay_lines))
    
    for i in range(6):
        start_idx = boundaries[i]
        end_idx = boundaries[i+1]
        chunk_lines = gameplay_lines[start_idx:end_idx]
        
        # Scan chunk_lines for parsed[0] command values to build fast-path index lookup!
        cmds = set()
        subs = set()
        for line in chunk_lines:
            line_str = line.strip()
            # Extract parsed[0]=="cmd"
            match = re.search(r'parsed\[0\]\s*==\s*["\']([^"\']+)["\']', line_str)
            if match:
                cmds.add(match.group(1))
            # Extract string_contains(e.message, "sub")
            match_sub = re.search(r'string_contains\([a-zA-Z0-9_\.]+\s*,\s*["\']([^"\']+)["\']', line_str)
            if match_sub:
                subs.add(match_sub.group(1))
                
        # Format chunk to start with standalone 'if' instead of 'elif'
        first_line = chunk_lines[0]
        # Replace the leading 'elif' with 'if' in the first statement
        if "elif" in first_line:
            first_line = first_line.replace("elif", "if", 1)
        chunk_lines[0] = first_line
        
        # Normalize indentation of extracted body to 1 tab (since directly in handle_gameplay_N)
        chunk_lines_norm = normalize_indent(chunk_lines, target_indent=1)
        
        func_name = f"handle_gameplay_{i+1}"
        cmd_set_str = ", ".join(f'"{c}"' for c in cmds)
        sub_set_str = ", ".join(f'"{s}"' for s in subs)
        
        chunk_code = (
            f"def {func_name}(e, parsed, index):\n"
            f"\tglobal languages\n"
            f"\tcmds = {{{cmd_set_str}}}\n"
            f"\tsubs = {{{sub_set_str}}}\n"
            f"\tmatched = False\n"
            f"\tif len(parsed) > 0 and parsed[0] in cmds:\n"
            f"\t\tmatched = True\n"
            f"\telse:\n"
            f"\t\tfor s in subs:\n"
            f"\t\t\tif s in e.message:\n"
            f"\t\t\t\tmatched = True\n"
            f"\t\t\t\tbreak\n"
            f"\tif not matched:\n"
            f"\t\treturn False\n\n"
            + "".join(chunk_lines_norm) + "\n"
            f"\treturn True\n"
        )
        
        mod_path = os.path.join(modules_dir, f"zh_net_gameplay_{i+1}.py")
        with open(mod_path, "w", encoding="utf-8") as out:
            out.write(header + chunk_code)
        print(f"Created gameplay submodule: {mod_path} ({len(chunk_lines)} lines)")
        
    # 6. Write modular delegated netloop() inside zh_core.py
    netloop_delegated = (
        "def netloop():\n"
        "    global languages, e\n"
        "    try:\n"
        "        e = g.n.request()\n"
        "    except:\n"
        "        return\n"
        "    if e.type == event_disconnect:\n"
        "        px = g.get_player_index(e.peer_id)\n"
        "        if px > -1:\n"
        "            remove_from_server(px)\n"
        "    if e.type == event_receive:\n"
        "        if e.channel == 1:\n"
        "            import zh_net_chat\n"
        "            zh_net_chat.handle_channel_1(e)\n"
        "        elif e.channel == 0:\n"
        "            import zh_net_gameplay_1, zh_net_gameplay_2, zh_net_gameplay_3, zh_net_gameplay_4, zh_net_gameplay_5, zh_net_gameplay_6\n"
        "            parsed = g.string_split(e.message, ' ', True)\n"
        "            index = g.get_player_index(e.peer_id)\n"
        "            if index > -1:\n"
        "                if zh_net_gameplay_1.handle_gameplay_1(e, parsed, index): return\n"
        "                if zh_net_gameplay_2.handle_gameplay_2(e, parsed, index): return\n"
        "                if zh_net_gameplay_3.handle_gameplay_3(e, parsed, index): return\n"
        "                if zh_net_gameplay_4.handle_gameplay_4(e, parsed, index): return\n"
        "                if zh_net_gameplay_5.handle_gameplay_5(e, parsed, index): return\n"
        "                if zh_net_gameplay_6.handle_gameplay_6(e, parsed, index): return\n"
        "        elif e.channel in (2, 5, 6):\n"
        "            import zh_net_others\n"
        "            zh_net_others.handle_channel_others(e)\n"
    )
    extracted["zh_core"].append(netloop_delegated)
    
    # Write the submodules
    for mod_name, code_blocks in extracted.items():
        mod_path = os.path.join(modules_dir, f"{mod_name}.py")
        content = header + "\n\n".join(code_blocks) + "\n"
        with open(mod_path, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"Created {mod_path} with {len(code_blocks)} code blocks.")
        
    # Write coordinator zhaserver.py
    new_zhaserver_lines = []
    for idx, line in enumerate(lines):
        if not omit_lines[idx]:
            new_zhaserver_lines.append(line)
            
    top_binder = (
        "# --- AUTOMATIC PATH RESOLUTION AND MODULE REGISTRATION ---\n"
        "import sys\n"
        "import os\n"
        "MODULES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))\n"
        "if MODULES_DIR not in sys.path:\n"
        "    sys.path.insert(0, MODULES_DIR)\n\n"
        "# --- AUTOMATIC TOP MODULE BINDER ---\n"
        "import types\n"
        "import zh_utils\n"
        "import zh_auth\n"
        "import zh_persistence\n"
        "import zh_gameplay\n"
        "import zh_core\n"
        "import zh_net_chat\n"
        "import zh_net_others\n"
        "import zh_net_gameplay_1\n"
        "import zh_net_gameplay_2\n"
        "import zh_net_gameplay_3\n"
        "import zh_net_gameplay_4\n"
        "import zh_net_gameplay_5\n"
        "import zh_net_gameplay_6\n\n"
        "submodules = [\n"
        "    zh_utils, zh_auth, zh_persistence, zh_gameplay, zh_core,\n"
        "    zh_net_chat, zh_net_others,\n"
        "    zh_net_gameplay_1, zh_net_gameplay_2, zh_net_gameplay_3,\n"
        "    zh_net_gameplay_4, zh_net_gameplay_5, zh_net_gameplay_6\n"
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
    
    new_zhaserver_content = top_binder + "".join(new_zhaserver_lines) + bottom_binder
    
    with open(zhaserver_path, "w", encoding="utf-8") as out:
        out.write(new_zhaserver_content)
        
    print(f"Modularized {zhaserver_path} successfully!")

if __name__ == '__main__':
    main()
