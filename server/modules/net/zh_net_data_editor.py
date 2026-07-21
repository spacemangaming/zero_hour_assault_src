import globals as g
import json
import os
import sys
import time
import datetime
import data_loader

# Lazy import — zh_bot_spawner is in modules/core/, which is in sys.path
# by the time any handler is called (after the binder runs).
def _bs():
    import zh_bot_spawner as _m
    return _m

# ── Sound Scanner & Player Giver Helpers ────────────────────────────────────
_cached_sounds = None

def _get_sounds_list():
    global _cached_sounds
    if _cached_sounds is not None:
        return _cached_sounds
    
    dat_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "sounds.dat")
    )
    if not os.path.exists(dat_path):
        return []
        
    try:
        src_utils_dir = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src", "zero_hour_assault", "utils")
        )
        if src_utils_dir not in sys.path:
            sys.path.insert(0, src_utils_dir)
        from pack_file import pack_file
        
        p = pack_file()
        p.open(dat_path)
        files = [f.decode(errors="ignore") for f in p.list_files()]
        p.close()
        files.sort()
        _cached_sounds = files
        return _cached_sounds
    except Exception as ex:
        print(f"Error reading sounds.dat: {ex}")
        return []

def _get_all_items():
    items = set(data_loader.get_inventory_limits().keys())
    legacy_items = (
        "vitality_potion revival_nectar small_potion "
        "hand_grenade molotov_cocktail snowflake_shard timebomb tm62 zk91 "
        "parachute binoculars base_life_amplifier metal_shield ladder "
        "fire_suppressant barricade invisibility_shield steel_helmet silencer "
        "7.62x51mm 5.56x45mm dragunov_psl_ammo_cartrigges gsg5_ammo_cartrigges "
        "357_magnum 9mm 45_ACP 12_gauge 40S&W 22_LR_Long_Rifle m4_ammo_cartrigges "
        "colt1911_ammo_cartrigges fnhfnp40_ammo_cartrigges 7.62x54mmR"
    ).split()
    items.update(legacy_items)
    return sorted(list(items))

def _apply_give(admin_idx, target_idx):
    ctx = _player_ctx(admin_idx)
    cat = ctx.get("give_category", "")
    item = ctx.get("give_item", "")
    admin_pid = g.players[admin_idx].peer_id
    admin_name = g.players[admin_idx].name
    target = g.players[target_idx]
    
    if not cat or not item:
        g.n.send_reliable(admin_pid, "Give transaction lost context.", 0)
        _send_main_menu(admin_idx)
        return
        
    if cat == "weapon":
        target.give(item, 1)
        import pickle
        data = pickle.dumps(target.inv)
        target.cachedinv = data
        g.n.send_reliable(target.peer_id, data, 19)
        
        _log_edit(admin_name, "give", target.name, cat, item)
        g.n.send_reliable(admin_pid, f"Successfully gave weapon '{item}' to {target.name}.", 0)
        g.n.send_reliable(target.peer_id, f"An admin gave you weapon '{item}'.", 0)
        _send_give_player_list(admin_idx)
        
    elif cat == "character":
        if item not in target.bought_chars:
            target.bought_chars.append(item)
        
        _log_edit(admin_name, "give", target.name, cat, item)
        g.n.send_reliable(admin_pid, f"Successfully unlocked character '{item}' for {target.name}.", 0)
        g.n.send_reliable(target.peer_id, f"An admin unlocked character '{item}' for you.", 0)
        _send_give_player_list(admin_idx)
        
    elif cat == "item":
        ctx["give_target_idx"] = target_idx
        ctx["field_key"] = "_give_amount"
        ctx["awaiting_input"] = True
        _deinput(admin_pid, "_give_amount", f"Enter amount of '{item}' to give (default: 1):")

    elif cat == "paid_account":
        if item == "Custom Duration":
            ctx["give_target_idx"] = target_idx
            ctx["field_key"] = "_give_custom_paid"
            ctx["awaiting_input"] = True
            _deinput(admin_pid, "_give_custom_paid", "Enter subscription duration in months (e.g. 5):")
            return
        import time as tm
        durations = {
            "1 Month": 30 * 24 * 3600,
            "3 Months": 90 * 24 * 3600,
            "6 Months": 180 * 24 * 3600,
            "1 Year": 12 * 30 * 24 * 3600
        }
        seconds = durations.get(item, 30 * 24 * 3600)
        target.paid = True
        target.paidtime = int(tm.time())
        target.paidmonths = seconds
        
        from file_directories import file_put_contents
        file_put_contents("chars/" + target.name + "/paid.usr", "True")
        file_put_contents("chars/" + target.name + "/paidtime.usr", str(target.paidtime))
        file_put_contents("chars/" + target.name + "/paidmonths.usr", str(target.paidmonths))
        
        _log_edit(admin_name, "give", target.name, cat, item)
        g.n.send_reliable(admin_pid, f"Successfully gave {item} paid subscription to {target.name}.", 0)
        g.n.send_reliable(target.peer_id, f"An admin activated a {item} paid subscription for you.", 0)
        _send_give_player_list(admin_idx)

    elif cat == "token_pack":
        if item == "Custom Amount":
            ctx["give_target_idx"] = target_idx
            ctx["field_key"] = "_give_custom_tokens"
            ctx["awaiting_input"] = True
            _deinput(admin_pid, "_give_custom_tokens", "Enter amount of tokens to give:")
            return
        
        fn = "ioszitemdata.txt" if getattr(target, "ios", False) else "zitemdata.txt"
        try:
            with open(fn, "a") as f:
                f.write(f"{target.name}={item}=1\n")
            _log_edit(admin_name, "give", target.name, cat, f"{item} via /givepack")
            g.n.send_reliable(admin_pid, f"Successfully queued pack '{item}' for {target.name} via /givepack.", 0)
        except Exception as ex:
            g.n.send_reliable(admin_pid, f"Error writing givepack data: {ex}", 0)
        _send_give_player_list(admin_idx)

def _send_sound_search_menu(index):
    m = server_menu()
    m.initial_packet = "de_sounds_main"
    m.intro = "Sound Scanner - choose an option"
    m.add("Search sounds by name", "search", True)
    m.add("List all sounds (first 150)", "all", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _send_sounds_list(index):
    ctx = _player_ctx(index)
    query = ctx.get("sound_query", "")
    sounds = _get_sounds_list()
    
    if query:
        matches = [s for s in sounds if query.lower() in s.lower()]
        intro = f"Sound matches for '{query}'"
    else:
        matches = sounds
        intro = "All sounds (showing first 150)"
        
    m = server_menu()
    m.initial_packet = "de_sounds_list"
    m.intro = f"{intro} - choose to copy"
    
    limit = 150
    for s in matches[:limit]:
        m.add(s, s, True)
        
    if len(matches) > limit:
        m.add(f"-- Showing {limit} of {len(matches)} matches. Refine query. --", "__sep__", True)
        
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _send_give_cat_menu(index):
    m = server_menu()
    m.initial_packet = "de_give_cat"
    m.intro = "Give to player - select category"
    m.add("Weapon", "weapon", True)
    m.add("Item", "item", True)
    m.add("Character", "character", True)
    m.add("Paid Account", "paid_account", True)
    m.add("Token Pack", "token_pack", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _send_give_items_list(index):
    ctx = _player_ctx(index)
    cat = ctx.get("give_category", "")
    
    m = server_menu()
    m.initial_packet = "de_give_item"
    m.intro = f"Give {cat} - select item to give"
    
    if cat == "weapon":
        items = sorted(list(data_loader.get_all_weapons().keys()))
    elif cat == "character":
        items = sorted(list(data_loader.get_all_characters().keys()))
    elif cat == "item":
        items = _get_all_items()
    elif cat == "paid_account":
        items = ["1 Month", "3 Months", "6 Months", "1 Year", "Custom Duration"]
    elif cat == "token_pack":
        items = list(data_loader._token_packs.keys()) + ["Custom Amount"]
    else:
        items = []
        
    for item in items:
        m.add(item, item, True)
        
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _send_give_player_list(index):
    ctx = _player_ctx(index)
    item = ctx.get("give_item", "")
    cat = ctx.get("give_category", "")
    
    m = server_menu()
    m.initial_packet = "de_give_player"
    m.intro = f"Give {cat} '{item}' - select target player"
    
    online_players = [p for p in g.players if p is not None and getattr(p, "name", None)]
    for p in online_players:
        m.add(p.name, p.name, True)
        
    m.add("-- Enter name manually --", "__manual__", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

# ---------------------------------------------------------------------------
# In-Game Staff Data Editor
# ---------------------------------------------------------------------------
# Menu command namespace: all packets start with "de_"
# Entry point: parsed[0] == "de_main"
#
# Navigation per-player stored in g.players[index]._de_ctx:
#   category      : str  (weapons/characters/zombie/chest/loot/ranks)
#   item_key      : str  (weapon key, char key, rank index, or == category for single-file)
#   field_key     : str  (field name, "pool.item", "drop.N", or "_new*" creation keys)
#   _pending_score: int  (rank creation: score stored between the two prompts)
# ---------------------------------------------------------------------------

DATA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
)
ANN_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "announcements")
)



# Scalar-only skip: dict/list fields we handle specially below instead of skipping
_ALWAYS_SKIP = {"thrown"}   # null/complex, never useful to edit directly

# Default templates for new entries
_DEFAULT_WEAPON = {
    "bullet": True, "fire_interval": 1000, "auto": False, "range": 20,
    "min_damage": 20, "max_damage": 50, "spread": 3, "mag_size": 30,
    "ammo_type": "rifle", "reload_time": 3000, "npc_priority": 2,
    "bulletfall_min": 5, "bulletfall_max": 10, "thrown": None
}
_DEFAULT_CHARACTER = {
    "walk_time": 200, "max_walk_time": 120, "health": 150,
    "plus_damage": 10, "jump_time": 100, "purchasable": False
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _data_path(rel):
    return os.path.join(DATA_DIR, rel)

def _load_json(rel):
    try:
        with open(_data_path(rel)) as f:
            return json.load(f)
    except Exception:
        return None

def _save_json(rel, obj):
    path = _data_path(rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def _player_ctx(index):
    if not hasattr(g.players[index], "_de_ctx"):
        g.players[index]._de_ctx = {}
    return g.players[index]._de_ctx

def _require_admin(index):
    if not (g.players[index].admin or g.players[index].dev):
        g.n.send_reliable(g.players[index].peer_id,
            "You don't have permission to use the data editor.", 0)
        return True
    return False

def _reload(index):
    pid = g.players[index].peer_id
    try:
        data_loader.reload_all()
    except Exception as ex:
        g.n.send_reliable(pid, f"Reload error: {ex}", 0)

def _log_edit(admin_name, category, item_key, field_key, new_value):
    line = f"[DATA_EDIT] {admin_name} set {category}/{item_key}.{field_key} = {new_value}"
    try:
        import datetime
        file_put_contents("data_edits.log", f"{datetime.datetime.now().isoformat()}  {line}\n", "a")
    except Exception:
        pass
    for p in g.players:
        if p.admin or p.dev:
            g.n.send_reliable(p.peer_id, line, 0)

def _coerce(value_str, old_value):
    if isinstance(old_value, bool):
        return value_str.lower() in ("true", "1", "yes")
    if isinstance(old_value, int):
        try: return int(value_str)
        except ValueError: return value_str
    if isinstance(old_value, float):
        try: return float(value_str)
        except ValueError: return value_str
    return value_str

# ---------------------------------------------------------------------------
# Data accessors
# ---------------------------------------------------------------------------

def _get_data(category, item_key):
    if category == "weapons":
        return data_loader._weapons.get(item_key, {})
    if category == "characters":
        return data_loader._characters.get(item_key, {})
    if category == "zombie":
        return data_loader.get_zombie_stats()
    if category == "chest":
        return data_loader.get_chest_config()
    if category == "loot":
        return data_loader.get_loot_table()
    if category == "ranks":
        try: return data_loader._ranks[int(item_key)]
        except Exception: return {}
    if category == "match_modes":
        return data_loader.get_match_mode(item_key)
    return {}

# ---------------------------------------------------------------------------
# Menu builders
# ---------------------------------------------------------------------------

def _send_main_menu(index):
    m = server_menu()
    m.initial_packet = "de_main"
    m.intro = "Data Editor - choose a category"
    m.add(f"Weapons ({len(data_loader._weapons)} entries)", "weapons", True)
    m.add(f"Characters ({len(data_loader._characters)} entries)", "characters", True)
    m.add(f"Match Modes ({len(data_loader.get_all_match_modes())} entries)", "match_modes", True)
    m.add("Zombie stats", "zombie", True)
    m.add("Chest pool & config", "chest", True)
    m.add("Loot table", "loot", True)
    m.add(f"Ranks ({len(data_loader._ranks)} entries)", "ranks", True)
    m.add("Manage Announcements", "announcements", True)
    m.add("Bot Spawners", "bot_spawners", True)
    m.add("Scan sounds.dat", "scan_sounds", True)
    m.add("Give weapon/item/character to player", "give_player", True)
    m.add("Reload all configs from disk", "reload", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)


# ── Announcements Manager Helpers ───────────────────────────────────────────

def _get_all_announcements():
    os.makedirs(ANN_DIR, exist_ok=True)
    list_ann = []
    for f in os.listdir(ANN_DIR):
        if f.endswith(".announcement"):
            path = os.path.join(ANN_DIR, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    list_ann.append(data)
            except Exception:
                pass
    list_ann.sort(key=lambda x: x.get("id", ""), reverse=True)
    return list_ann

def _send_announcements_main_menu(index):
    m = server_menu()
    m.initial_packet = "de_ann_main"
    m.intro = "Announcements Manager"
    m.add("List Announcements", "list", True)
    m.add("Create New Announcement", "create", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _send_announcements_list(index):
    m = server_menu()
    m.initial_packet = "de_ann_list"
    m.intro = "Announcements List - select to edit"
    anns = _get_all_announcements()
    if not anns:
        m.add("-- No announcements --", "__none__", True)
    for ann in anns:
        pinned_str = "[PINNED] " if ann.get("pinned") else ""
        title = ann.get("title", "No Title")
        author = ann.get("author", "Unknown")
        label = f"{pinned_str}{title} (by {author})"
        m.add(label, ann.get("id"), True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _send_announcement_fields(index, ann_id):
    path = os.path.join(ANN_DIR, f"{ann_id}.announcement")
    if not os.path.exists(path):
        g.n.send_reliable(g.players[index].peer_id, "Announcement not found.", 0)
        _send_announcements_list(index)
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        g.n.send_reliable(g.players[index].peer_id, f"Error loading announcement: {ex}", 0)
        _send_announcements_list(index)
        return

    m = server_menu()
    m.initial_packet = "de_ann_fields"
    m.intro = f"Edit Announcement: {data.get('title')}"
    m.add(f"Title: {data.get('title')}", f"title:{ann_id}", True)
    content_preview = data.get("content", "")
    if len(content_preview) > 30:
        content_preview = content_preview[:27] + "..."
    m.add(f"Content: {content_preview}", f"content:{ann_id}", True)
    m.add(f"Pinned: {data.get('pinned', False)}", f"pinned:{ann_id}", True)
    m.add("── Delete Announcement ──", f"delete:{ann_id}", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)

def _prompt_announcement_create_title(index):
    ctx = _player_ctx(index)
    ctx["field_key"] = "ann_create_title"
    ctx["awaiting_input"] = True
    _deinput(g.players[index].peer_id, "ann_create_title", "Enter announcement title:")

def _prompt_announcement_create_content(index):
    ctx = _player_ctx(index)
    ctx["field_key"] = "ann_create_content"
    ctx["awaiting_input"] = True
    _deinput(g.players[index].peer_id, "ann_create_content", "Enter announcement content:")




def _send_item_list(index, category):
    m = server_menu()
    m.initial_packet = "de_itemlist"
    if category == "weapons":
        m.intro = "Weapons - select one to edit, or add new"
        for key in sorted(data_loader._weapons.keys()):
            m.add(key, key, True)
        m.add("-- Add new weapon --", "__add__", True)
    elif category == "characters":
        m.intro = "Characters - select one to edit, or add new"
        for key in sorted(data_loader._characters.keys()):
            m.add(key, key, True)
        m.add("-- Add new character --", "__add__", True)
    elif category == "match_modes":
        m.intro = "Match Modes - select one to edit, or add new"
        for key in sorted(data_loader.get_all_match_modes().keys()):
            m.add(key, key, True)
        m.add("-- Add new match mode --", "__add__", True)
    elif category == "ranks":
        m.intro = "Ranks - select one to edit, or add new"
        for i, r in enumerate(data_loader._ranks):
            m.add(f"{r['name']} (score {r['score']})", str(i), True)
        m.add("-- Add new rank --", "__add__", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)


def _send_field_list(index, category, item_key):
    m = server_menu()
    m.initial_packet = "de_fieldlist"
    m.intro = f"Edit {item_key} - choose a field"
    data = _get_data(category, item_key)

    # Scalar fields first
    for field, val in data.items():
        if field in _ALWAYS_SKIP:
            continue
        if isinstance(val, (dict, list)):
            continue   # handled below as special sections
        m.add(f"{field}: {val}", field, True)

    # ── Chest: pool entries ──────────────────────────────────────────────────
    if category == "chest":
        pool = data.get("pool", {})
        if pool:
            m.add("── Pool items ──", "__sep_pool__", True)
            for item_name, weight in sorted(pool.items()):
                m.add(f"  {item_name}: weight {weight}", f"pool.{item_name}", True)
        m.add("-- Add pool item --", "__add_pool__", True)

    # ── Loot: drop entries ───────────────────────────────────────────────────
    elif category == "loot":
        drops = data.get("drops", [])
        if drops:
            m.add("── Loot drops ──", "__sep_drops__", True)
            for i, drop in enumerate(drops):
                label = f"  {drop['item']}: min={drop['min']} max={drop['max']}"
                m.add(label, f"drop.{i}", True)
        m.add("-- Add loot drop --", "__add_drop__", True)

    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)


def _deinput(pid, field_key, prompt):
    """Send a deinput packet — client shows get_input() and auto-sends de_setval back."""
    g.n.send_reliable(pid, f"deinput {field_key} {prompt}", 0)


def _send_value_prompt(index, category, item_key, field_key):
    pid = g.players[index].peer_id
    ctx = _player_ctx(index)
    ctx["field_key"] = field_key
    ctx["awaiting_input"] = True

    if field_key.startswith("pool.") and category == "chest":
        item_name = field_key[5:]
        pool = data_loader.get_chest_config().get("pool", {})
        current = pool.get(item_name, "?")
        _deinput(pid, field_key, f"Chest pool weight for {item_name} (current: {current})")
        return

    if field_key.startswith("drop.") and category == "loot":
        try:
            idx = int(field_key[5:])
            drop = data_loader.get_loot_table()["drops"][idx]
            current = f"{drop['item']},{drop['min']},{drop['max']}"
        except Exception:
            current = "item,min,max"
        _deinput(pid, field_key, f"Edit loot drop (current: {current}) — enter item,min,max")
        return

    data = _get_data(category, item_key)
    current = data.get(field_key, "?")
    _deinput(pid, field_key, f"{item_key}.{field_key} (current: {current})")


# ---------------------------------------------------------------------------
# Creation flow prompts
# ---------------------------------------------------------------------------

def _prompt_new_key(index, cat):
    ctx = _player_ctx(index)
    ctx["field_key"] = "_newkey"
    ctx["awaiting_input"] = True
    label = "weapon" if cat == "weapons" else ("character" if cat == "characters" else "match mode")
    _deinput(g.players[index].peer_id, "_newkey", f"Enter key name for new {label} (no spaces)")

def _prompt_new_rank_score(index):
    ctx = _player_ctx(index)
    ctx["field_key"] = "_newscore"
    ctx["awaiting_input"] = True
    _deinput(g.players[index].peer_id, "_newscore", "Enter score required for new rank")

def _prompt_new_rank_name(index):
    score = _player_ctx(index).get("_pending_score", "?")
    ctx = _player_ctx(index)
    ctx["field_key"] = "_newname"
    ctx["awaiting_input"] = True
    _deinput(g.players[index].peer_id, "_newname", f"Enter display name for new rank (score: {score})")

def _prompt_new_pool_item(index):
    ctx = _player_ctx(index)
    ctx["field_key"] = "_newpool"
    ctx["awaiting_input"] = True
    _deinput(g.players[index].peer_id, "_newpool", "Add chest pool item — enter item_name,weight (e.g. m4,1)")

def _prompt_new_drop(index):
    ctx = _player_ctx(index)
    ctx["field_key"] = "_newdrop"
    ctx["awaiting_input"] = True
    _deinput(g.players[index].peer_id, "_newdrop", "Add loot drop — enter item,min,max (e.g. m4,1,1)")


# ---------------------------------------------------------------------------
# Apply edit — normal fields AND creation flow
# ---------------------------------------------------------------------------

def _apply_edit(index, new_value_str):
    ctx = _player_ctx(index)
    category  = ctx.get("category")
    item_key  = ctx.get("item_key")
    field_key = ctx.get("field_key")
    pid = g.players[index].peer_id
    admin = g.players[index].name

    # ── Bot Spawner: new map name prompt ──────────────────────────────────
    if field_key == "_spawner_newmap":
        map_name = new_value_str.strip()
        ctx["field_key"] = None; ctx["awaiting_input"] = False
        if not map_name:
            g.n.send_reliable(pid, "Map name cannot be empty.", 0)
            _spawner_main_menu(index); return
        cfg = _bs().get_spawners_cache()
        if map_name not in cfg:
            cfg[map_name] = []
            _bs().save_spawners()
            _bs().load_spawners()
        ctx["spawner_map"] = map_name
        _spawner_list_for_map(index, map_name); return

    # ── Bot Spawner: new spawner type prompt (type/npc/zombie) ────────────
    if field_key == "_spawner_newtype":
        bot_type = new_value_str.strip().lower()
        ctx["field_key"] = None; ctx["awaiting_input"] = False
        if bot_type not in ("npc", "zombie"):
            g.n.send_reliable(pid, "Type must be 'npc' or 'zombie'.", 0)
            map_name = ctx.get("spawner_map", "")
            _spawner_list_for_map(index, map_name); return
        import time as _t
        map_name = ctx.get("spawner_map", "")
        new_sid = f"sp_{int(_t.time())}"
        new_sp = {
            "id": new_sid, "type": bot_type, "enabled": False,
            "max_count": 5, "schedule_ms": 30000,
            "minx": 0, "maxx": 200, "miny": 0, "maxy": 200, "z": 0,
            "mind": 30, "maxd": 50, "health": 100, "hitrange": 30,
            "walktime": 150, "shoottime": 10, "voicesound": "botbeacon"
        }
        cfg = _bs().get_spawners_cache()
        cfg.setdefault(map_name, []).append(new_sp)
        _bs().save_spawners()
        _bs().load_spawners()
        g.n.send_reliable(pid, f"Created spawner '{new_sid}' on '{map_name}'.", 0)
        ctx["spawner_id"] = new_sid
        _spawner_fields_menu(index, map_name, new_sid); return

    # ── Announcements creation / editing ──────────────────────────────────
    if field_key == "ann_create_title":
        ctx["ann_temp_title"] = new_value_str.strip()
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        _prompt_announcement_create_content(index)
        return

    if field_key == "ann_create_content":
        title = ctx.get("ann_temp_title", "Untitled")
        content = new_value_str.strip()
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        ctx.pop("ann_temp_title", None)
        
        ann_id = str(int(time.time()))
        import datetime as dt_mod
        dt_class = dt_mod.datetime if hasattr(dt_mod, "datetime") else dt_mod
        data = {
            "id": ann_id,
            "title": title,
            "content": content,
            "author": admin,
            "timestamp": dt_class.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pinned": False
        }
        os.makedirs(ANN_DIR, exist_ok=True)
        path = os.path.join(ANN_DIR, f"{ann_id}.announcement")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            g.n.send_reliable(pid, "Announcement created successfully.", 0)
            
            # Broadcast to all players that a new announcement is posted
            try:
                g.n.broadcast("play_s important.ogg", 0)
                g.n.broadcast(f"New Announcement: {title}\nOpen game menu to read details.", 2)
            except Exception:
                pass
                
            _send_announcement_fields(index, ann_id)
        except Exception as ex:
            g.n.send_reliable(pid, f"Error creating announcement: {ex}", 0)
            _send_announcements_main_menu(index)
        return

    if field_key and field_key.startswith("ann_edit_title:"):
        ann_id = field_key.split(":")[1]
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        
        path = os.path.join(ANN_DIR, f"{ann_id}.announcement")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["title"] = new_value_str.strip()
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                g.n.send_reliable(pid, "Announcement title updated.", 0)
            except Exception as ex:
                g.n.send_reliable(pid, f"Error updating announcement: {ex}", 0)
        _send_announcement_fields(index, ann_id)
        return

    if field_key and field_key.startswith("ann_edit_content:"):
        ann_id = field_key.split(":")[1]
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        
        path = os.path.join(ANN_DIR, f"{ann_id}.announcement")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["content"] = new_value_str.strip()
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                g.n.send_reliable(pid, "Announcement content updated.", 0)
            except Exception as ex:
                g.n.send_reliable(pid, f"Error updating announcement: {ex}", 0)
        _send_announcement_fields(index, ann_id)
        return

    if field_key == "_soundquery":
        ctx["sound_query"] = new_value_str.strip()
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        _send_sounds_list(index)
        return

    if field_key == "_give_manual_player":
        target_name = new_value_str.strip()
        target_idx = g.get_player_index_from(target_name)
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        if target_idx == -1 or g.players[target_idx] is None:
            g.n.send_reliable(pid, "Player not found or offline.", 0)
            _send_give_player_list(index)
            return
        _apply_give(index, target_idx)
        return

    if field_key == "_give_amount":
        target_idx = ctx.get("give_target_idx")
        item = ctx.get("give_item")
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        ctx.pop("give_target_idx", None)
        
        if target_idx is None or g.players[target_idx] is None:
            g.n.send_reliable(pid, "Target player no longer online.", 0)
            _send_main_menu(index)
            return
            
        try:
            amount = int(new_value_str.strip())
        except ValueError:
            amount = 1
            
        if amount <= 0:
            amount = 1
            
        target = g.players[target_idx]
        target.give(item, amount)
        import pickle
        data = pickle.dumps(target.inv)
        target.cachedinv = data
        g.n.send_reliable(target.peer_id, data, 19)
        
        _log_edit(admin, "give", target.name, "item", f"{item} (qty: {amount})")
        g.n.send_reliable(pid, f"Successfully gave {amount}x '{item}' to {target.name}.", 0)
        g.n.send_reliable(target.peer_id, f"An admin gave you {amount}x '{item}'.", 0)
        _send_give_player_list(index)
        return

    if field_key == "_give_custom_paid":
        target_idx = ctx.get("give_target_idx")
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        ctx.pop("give_target_idx", None)
        
        if target_idx is None or g.players[target_idx] is None:
            g.n.send_reliable(pid, "Target player no longer online.", 0)
            _send_main_menu(index)
            return
            
        try:
            months = int(new_value_str.strip())
        except ValueError:
            months = 1
            
        if months <= 0:
            months = 1
            
        seconds = months * 30 * 24 * 3600
        target = g.players[target_idx]
        import time as tm
        target.paid = True
        target.paidtime = int(tm.time())
        target.paidmonths = seconds
        
        from file_directories import file_put_contents
        file_put_contents("chars/" + target.name + "/paid.usr", "True")
        file_put_contents("chars/" + target.name + "/paidtime.usr", str(target.paidtime))
        file_put_contents("chars/" + target.name + "/paidmonths.usr", str(target.paidmonths))
        
        _log_edit(admin, "give", target.name, "paid_account", f"{months} Months")
        g.n.send_reliable(pid, f"Successfully gave {months} Months paid subscription to {target.name}.", 0)
        g.n.send_reliable(target.peer_id, f"An admin activated a {months} Months paid subscription for you.", 0)
        _send_give_player_list(index)
        return

    if field_key == "_give_custom_tokens":
        target_idx = ctx.get("give_target_idx")
        ctx["field_key"] = None
        ctx["awaiting_input"] = False
        ctx.pop("give_target_idx", None)
        
        if target_idx is None or g.players[target_idx] is None:
            g.n.send_reliable(pid, "Target player no longer online.", 0)
            _send_main_menu(index)
            return
            
        try:
            amt = int(new_value_str.strip())
        except ValueError:
            amt = 100
            
        if amt <= 0:
            amt = 100
            
        target = g.players[target_idx]
        target.zhtoken += amt
        
        from zh_persistence import save_char
        save_char(target_idx)
        
        _log_edit(admin, "give", target.name, "token_pack", f"{amt} Tokens")
        g.n.send_reliable(pid, f"Successfully gave {amt} tokens to {target.name}.", 0)
        g.n.send_reliable(target.peer_id, f"An admin gave you {amt} tokens.", 0)
        _send_give_player_list(index)
        return

    if not category or not field_key:
        g.n.send_reliable(pid, "No pending edit.", 0)
        return

    # ── New weapon / character ───────────────────────────────────────────────
    if field_key == "_newkey":
        key = new_value_str.strip().replace(" ", "_")
        if not key:
            g.n.send_reliable(pid, "Key cannot be empty.", 0); _prompt_new_key(index, category); return
        if category == "weapons":
            rel = f"weapons/{key}.json"
            if os.path.exists(_data_path(rel)):
                g.n.send_reliable(pid, f"Weapon '{key}' already exists.", 0); _send_item_list(index, category); return
            _save_json(rel, dict(_DEFAULT_WEAPON))
        elif category == "characters":
            rel = f"characters/{key}.json"
            if os.path.exists(_data_path(rel)):
                g.n.send_reliable(pid, f"Character '{key}' already exists.", 0); _send_item_list(index, category); return
            _save_json(rel, dict(_DEFAULT_CHARACTER))
        elif category == "match_modes":
            rel = "match_modes.json"
            obj = _load_json(rel)
            if obj is None:
                g.n.send_reliable(pid, "Error loading match_modes.json", 0); return
            if key in obj:
                g.n.send_reliable(pid, f"Match mode '{key}' already exists.", 0); _send_item_list(index, category); return
            obj[key] = {
                "display_name": key.replace("_", " "),
                "map": "main",
                "team_based": True,
                "allow_bots": True,
                "use_helicopter": False,
                "min_size": 1,
                "max_size": 5
            }
            _save_json(rel, obj)
        _reload(index); _log_edit(admin, category, key, "(created)", "new")
        g.n.send_reliable(pid, f"Created '{key}' with default values.", 0)
        ctx["item_key"] = key; ctx["field_key"] = None; ctx["awaiting_input"] = False
        _send_field_list(index, category, key)
        return

    # ── New rank step 1: score ───────────────────────────────────────────────
    if field_key == "_newscore":
        try: score = int(new_value_str.strip())
        except ValueError:
            g.n.send_reliable(pid, "Score must be a whole number.", 0)
            _prompt_new_rank_score(index); return
        ctx["_pending_score"] = score; ctx["awaiting_input"] = False
        _prompt_new_rank_name(index); return

    # ── New rank step 2: name ────────────────────────────────────────────────
    if field_key == "_newname":
        name = new_value_str.strip()
        if not name:
            g.n.send_reliable(pid, "Name cannot be empty.", 0)
            _prompt_new_rank_name(index); return
        score = ctx.get("_pending_score", 0)
        rel = "ranks/ranks.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error: could not load ranks.json", 0); return
        new_rank = {"score": score, "name": name}
        inserted_at = len(obj)
        for i, r in enumerate(obj):
            if score < r.get("score", 0):
                obj.insert(i, new_rank); inserted_at = i; break
        else:
            obj.append(new_rank)
        _save_json(rel, obj); _reload(index)
        _log_edit(admin, "ranks", str(inserted_at), "(created)", f"{name}/{score}")
        g.n.send_reliable(pid, f"Created rank '{name}' at score {score} (index {inserted_at}).", 0)
        ctx["item_key"] = str(inserted_at); ctx["field_key"] = None
        ctx["awaiting_input"] = False; ctx.pop("_pending_score", None)
        _send_field_list(index, "ranks", str(inserted_at)); return

    # ── New chest pool item ──────────────────────────────────────────────────
    if field_key == "_newpool":
        parts = [p.strip() for p in new_value_str.split(",")]
        if len(parts) != 2:
            g.n.send_reliable(pid, "Format: item_name,weight  (e.g. m4,1)", 0)
            _prompt_new_pool_item(index); return
        item_name, weight_str = parts[0], parts[1]
        try: weight = int(weight_str)
        except ValueError:
            g.n.send_reliable(pid, "Weight must be a whole number.", 0)
            _prompt_new_pool_item(index); return
        rel = "chest/chest_items.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error: could not load chest_items.json", 0); return
        obj.setdefault("pool", {})[item_name] = weight
        _save_json(rel, obj); _reload(index)
        _log_edit(admin, "chest", "pool", item_name, str(weight))
        g.n.send_reliable(pid, f"Added '{item_name}' to chest pool with weight {weight}.", 0)
        ctx["field_key"] = None; ctx["awaiting_input"] = False
        _send_field_list(index, "chest", "chest"); return

    # ── New loot drop ────────────────────────────────────────────────────────
    if field_key == "_newdrop":
        parts = [p.strip() for p in new_value_str.split(",")]
        if len(parts) != 3:
            g.n.send_reliable(pid, "Format: item,min,max  (e.g. m4,1,1)", 0)
            _prompt_new_drop(index); return
        try: min_v, max_v = int(parts[1]), int(parts[2])
        except ValueError:
            g.n.send_reliable(pid, "min and max must be whole numbers.", 0)
            _prompt_new_drop(index); return
        new_drop = {"item": parts[0], "min": min_v, "max": max_v}
        rel = "items/loot_table.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error: could not load loot_table.json", 0); return
        obj.setdefault("drops", []).append(new_drop)
        _save_json(rel, obj); _reload(index)
        _log_edit(admin, "loot", "drops", parts[0], f"{min_v}-{max_v}")
        g.n.send_reliable(pid, f"Added loot drop: {parts[0]} (min={min_v} max={max_v}).", 0)
        ctx["field_key"] = None; ctx["awaiting_input"] = False
        _send_field_list(index, "loot", "loot"); return

    # ── Edit existing pool weight ────────────────────────────────────────────
    if field_key.startswith("pool.") and category == "chest":
        item_name = field_key[5:]
        try: weight = int(new_value_str.strip())
        except ValueError:
            g.n.send_reliable(pid, "Weight must be a whole number.", 0)
            _send_value_prompt(index, category, item_key, field_key); return
        rel = "chest/chest_items.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading chest_items.json", 0); return
        obj.setdefault("pool", {})[item_name] = weight
        _save_json(rel, obj); _reload(index)
        _log_edit(admin, "chest", "pool", item_name, str(weight))
        g.n.send_reliable(pid, f"Set chest pool '{item_name}' weight to {weight}.", 0)
        ctx["field_key"] = None; ctx["awaiting_input"] = False
        _send_field_list(index, "chest", "chest"); return

    # ── Edit existing loot drop ──────────────────────────────────────────────
    if field_key.startswith("drop.") and category == "loot":
        parts = [p.strip() for p in new_value_str.split(",")]
        if len(parts) != 3:
            g.n.send_reliable(pid, "Format: item,min,max", 0)
            _send_value_prompt(index, category, item_key, field_key); return
        try: min_v, max_v = int(parts[1]), int(parts[2])
        except ValueError:
            g.n.send_reliable(pid, "min and max must be whole numbers.", 0)
            _send_value_prompt(index, category, item_key, field_key); return
        try: idx = int(field_key[5:])
        except ValueError:
            g.n.send_reliable(pid, "Bad drop index.", 0); return
        rel = "items/loot_table.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading loot_table.json", 0); return
        obj["drops"][idx] = {"item": parts[0], "min": min_v, "max": max_v}
        _save_json(rel, obj); _reload(index)
        _log_edit(admin, "loot", "drops", str(idx), f"{parts[0]},{min_v},{max_v}")
        g.n.send_reliable(pid, f"Updated drop {idx}: {parts[0]} min={min_v} max={max_v}.", 0)
        ctx["field_key"] = None; ctx["awaiting_input"] = False
        _send_field_list(index, "loot", "loot"); return

    # ── Normal scalar field edit ─────────────────────────────────────────────
    if category == "weapons":
        rel = f"weapons/{item_key.replace('&','_')}.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, f"Error loading {rel}", 0); return
        obj[field_key] = _coerce(new_value_str, obj.get(field_key)); _save_json(rel, obj)

    elif category == "characters":
        rel = f"characters/{item_key}.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, f"Error loading {rel}", 0); return
        obj[field_key] = _coerce(new_value_str, obj.get(field_key)); _save_json(rel, obj)

    elif category == "match_modes":
        rel = "match_modes.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading match_modes.json", 0); return
        if item_key not in obj:
            g.n.send_reliable(pid, f"Unknown match mode: {item_key}", 0); return
        obj[item_key][field_key] = _coerce(new_value_str, obj[item_key].get(field_key))
        _save_json(rel, obj)

    elif category == "zombie":
        rel = "zombies/zombie.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading zombie.json", 0); return
        obj[field_key] = _coerce(new_value_str, obj.get(field_key)); _save_json(rel, obj)

    elif category == "chest":
        rel = "chest/chest_items.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading chest_items.json", 0); return
        obj[field_key] = _coerce(new_value_str, obj.get(field_key)); _save_json(rel, obj)

    elif category == "loot":
        rel = "items/loot_table.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading loot_table.json", 0); return
        obj[field_key] = _coerce(new_value_str, obj.get(field_key)); _save_json(rel, obj)

    elif category == "ranks":
        rel = "ranks/ranks.json"
        obj = _load_json(rel)
        if obj is None:
            g.n.send_reliable(pid, "Error loading ranks.json", 0); return
        try:
            rank_idx = int(item_key)
            obj[rank_idx][field_key] = _coerce(new_value_str, obj[rank_idx].get(field_key))
        except Exception as ex:
            g.n.send_reliable(pid, f"Error updating rank: {ex}", 0); return
        _save_json(rel, obj)

    else:
        g.n.send_reliable(pid, f"Unknown category: {category}", 0); return

    _reload(index)
    g.n.send_reliable(pid, f"Saved: {category}/{item_key}.{field_key} = {new_value_str}", 0)
    _log_edit(admin, category, item_key, field_key, new_value_str)
    ctx["awaiting_input"] = False; ctx["field_key"] = None


# ---------------------------------------------------------------------------
# Bot Spawner UI helpers
# ---------------------------------------------------------------------------

def _spawner_main_menu(index):
    """Top-level spawner screen: list maps that have spawners + add."""
    cfg = _bs().get_spawners_cache()
    m = server_menu()
    m.initial_packet = "de_spawner_maps"
    m.intro = "Bot Spawners - select a map"
    if cfg:
        for map_name, spawners in cfg.items():
            active = sum(1 for s in spawners if s.get("enabled"))
            m.add(f"{map_name} ({len(spawners)} spawners, {active} active)", map_name, True)
    m.add("-- Add spawner for a new map --", "__newmap__", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)


def _spawner_list_for_map(index, map_name):
    """List all spawners configured for map_name."""
    cfg = _bs().get_spawners_cache()
    spawners = cfg.get(map_name, [])
    m = server_menu()
    m.initial_packet = "de_spawner_list"
    m.intro = f"Spawners on '{map_name}'"
    for sp in spawners:
        sid = sp.get("id", "?")
        bot_type = sp.get("type", "npc")
        enabled = "ON" if sp.get("enabled") else "OFF"
        interval = sp.get("schedule_ms", 0)
        sched = f"every {interval}ms" if interval > 0 else "manual"
        label = f"[{enabled}] {sid} ({bot_type}, {sched}, max={sp.get('max_count',5)})"
        m.add(label, sid, True)
    m.add("-- Add new spawner --", "__add__", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)


def _spawner_fields_menu(index, map_name, spawner_id):
    """Edit/action screen for a single spawner."""
    cfg = _bs().get_spawners_cache()
    sp = next((s for s in cfg.get(map_name, []) if s.get("id") == spawner_id), None)
    if sp is None:
        g.n.send_reliable(g.players[index].peer_id, f"Spawner '{spawner_id}' not found.", 0)
        _spawner_list_for_map(index, map_name)
        return
    m = server_menu()
    m.initial_packet = "de_spawner_fields"
    enabled_label = "Disable" if sp.get("enabled") else "Enable"
    m.intro = f"Spawner '{spawner_id}' on '{map_name}'"
    # Actions
    m.add(f"{enabled_label} spawner", "toggle_enabled", True)
    m.add("Spawn one bot now (manual)", "spawn_now", True)
    m.add("Kill all bots from this spawner", "kill_bots", True)
    m.add("Delete this spawner", "delete", True)
    # Editable fields
    fields_npc = ["type", "max_count", "schedule_ms", "minx", "maxx", "miny", "maxy", "z",
                  "mind", "maxd", "health", "hitrange", "walktime", "shoottime", "voicesound"]
    fields_zombie = ["type", "max_count", "schedule_ms", "minx", "maxx", "miny", "maxy", "z"]
    fields = fields_npc if sp.get("type", "npc") == "npc" else fields_zombie
    m.add("── Fields ──", "__sep__", True)
    for f in fields:
        val = sp.get(f, "?")
        m.add(f"  {f}: {val}", f"field:{f}", True)
    m.add("Back", "back", True)
    m.send(g.players[index].peer_id)


def _apply_spawner_field_edit(index, new_value_str):
    """Save a single field edit for a spawner."""
    ctx = _player_ctx(index)
    map_name = ctx.get("spawner_map", "")
    spawner_id = ctx.get("spawner_id", "")
    field_key = ctx.get("field_key", "").replace("spawner:", "")
    pid = g.players[index].peer_id
    admin = g.players[index].name

    cfg = _bs().get_spawners_cache()
    sp = next((s for s in cfg.get(map_name, []) if s.get("id") == spawner_id), None)
    if sp is None:
        g.n.send_reliable(pid, "Spawner not found.", 0)
        ctx["awaiting_input"] = False
        ctx["field_key"] = None
        _spawner_list_for_map(index, map_name)
        return

    # Coerce value by existing type, or guess
    old_val = sp.get(field_key, "")
    if isinstance(old_val, bool):
        sp[field_key] = new_value_str.lower() in ("true", "1", "yes")
    elif isinstance(old_val, int):
        try:
            sp[field_key] = int(new_value_str)
        except ValueError:
            g.n.send_reliable(pid, f"Invalid integer: {new_value_str}", 0)
            ctx["awaiting_input"] = False
            ctx["field_key"] = None
            _spawner_fields_menu(index, map_name, spawner_id)
            return
    else:
        sp[field_key] = new_value_str.strip()

    _bs().save_spawners()
    _bs().load_spawners()
    g.n.send_reliable(pid, f"Spawner '{spawner_id}': {field_key} = {sp[field_key]}", 0)
    _log_edit(admin, "bot_spawners", spawner_id, field_key, new_value_str)
    ctx["awaiting_input"] = False
    ctx["field_key"] = None
    _spawner_fields_menu(index, map_name, spawner_id)


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------

def handle_data_editor(e, parsed, index):
    if index < 0:
        return False

    cmd = parsed[0] if parsed else ""

    # ── Main menu / category select ──────────────────────────────────────────
    if cmd == "de_main":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else ""
        if not choice:
            _player_ctx(index)["awaiting_input"] = False
            _send_main_menu(index); return True
        if choice == "back":
            _player_ctx(index)["awaiting_input"] = False
            m = server_menu()
            m.intro = "Select an option"
            m.initial_packet = "adminlog"
            m.add("Copy what commands used, system notification, reports, etc", "log2")
            m.add("check what commands used, system notification, reports, etc", "log")
            m.add("view suggestions", "suggestion")
            p = g.players[index]
            if p.is_admin() or p.dev:
                m.add("View Admin Help", "adminhelp")
            m.add("View moderator Help", "moderatorhelp")
            if p.is_admin() or p.builder or p.dev:
                m.add("View builder Help", "builderhelp")
            if p.is_admin() or p.dev:
                m.add("Data Editor - edit game balance configs live", "dataeditor")
            m.send(p.peer_id)
            return True
        if choice == "reload":
            _reload(index)
            g.n.send_reliable(g.players[index].peer_id, "All configs reloaded from disk.", 0)
            _send_main_menu(index); return True
        if choice == "scan_sounds":
            _send_sound_search_menu(index)
            return True
        if choice == "give_player":
            _send_give_cat_menu(index)
            return True
        ctx = _player_ctx(index)
        ctx["category"] = choice; ctx["item_key"] = None; ctx["field_key"] = None
        if choice in ("zombie", "chest", "loot"):
            ctx["item_key"] = choice
            _send_field_list(index, choice, choice)
        elif choice in ("ranks", "weapons", "characters", "match_modes"):
            _send_item_list(index, choice)
        elif choice == "announcements":
            _send_announcements_main_menu(index)
        elif choice == "bot_spawners":
            _spawner_main_menu(index)
        else:
            _send_main_menu(index)
        return True

    # ── Item list selection ──────────────────────────────────────────────────
    if cmd == "de_itemlist":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        ctx = _player_ctx(index)
        if choice == "back":
            _send_main_menu(index); return True
        cat = ctx.get("category", "")
        if choice == "__add__":
            ctx["item_key"] = None; ctx["field_key"] = None
            if cat == "ranks":
                _prompt_new_rank_score(index)
            else:
                _prompt_new_key(index, cat)
            return True
        ctx["item_key"] = choice; ctx["field_key"] = None
        _send_field_list(index, cat, choice); return True

    # ── Field list selection ─────────────────────────────────────────────────
    if cmd == "de_fieldlist":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        ctx = _player_ctx(index)
        cat = ctx.get("category", "")

        if choice == "back":
            if cat in ("zombie", "chest", "loot"):
                _send_main_menu(index)
            else:
                _send_item_list(index, cat)
            return True

        # Separator items — do nothing
        if choice in ("__sep_pool__", "__sep_drops__"):
            _send_field_list(index, cat, ctx.get("item_key", cat)); return True

        # Add new pool item
        if choice == "__add_pool__":
            _prompt_new_pool_item(index); return True

        # Add new loot drop
        if choice == "__add_drop__":
            _prompt_new_drop(index); return True

        # Normal field / pool.X / drop.N → prompt for value
        ctx["field_key"] = choice
        _send_value_prompt(index, cat, ctx.get("item_key", cat), choice)
        return True

    # ── Value submitted ──────────────────────────────────────────────────────
    if cmd == "de_setval":
        if _require_admin(index): return True
        if len(parsed) < 3:
            g.n.send_reliable(g.players[index].peer_id,
                "Usage: de_setval <field_name> <new_value>", 0)
            return True
        ctx = _player_ctx(index)
        field_name = parsed[1]
        
        # Intercept spawner field edits
        if field_name.startswith("spawner:"):
            ctx["field_key"] = field_name
            new_val_str = " ".join(parsed[2:])
            _apply_spawner_field_edit(index, new_val_str)
            return True

        # Intercept announcement edits
        if field_name in ("ann_create_title", "ann_create_content") or field_name.startswith("ann_edit_title:") or field_name.startswith("ann_edit_content:"):
            ctx["field_key"] = field_name
            new_val_str = " ".join(parsed[2:])
            _apply_edit(index, new_val_str)
            return True

        ctx["field_key"] = field_name
        new_val_str = " ".join(parsed[2:])
        _apply_edit(index, new_val_str)
        # _apply_edit handles all navigation internally
        cat = ctx.get("category", "")
        item = ctx.get("item_key", "")
        if cat and item and ctx.get("field_key") is None and not ctx.get("awaiting_input"):
            _send_field_list(index, cat, item)
        return True

    # ── Cancel ───────────────────────────────────────────────────────────────
    if cmd == "de_sounds_main":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back":
            _send_main_menu(index); return True
        ctx = _player_ctx(index)
        if choice == "search":
            ctx["field_key"] = "_soundquery"
            ctx["awaiting_input"] = True
            _deinput(g.players[index].peer_id, "_soundquery", "Enter sound name query (case-insensitive):")
            return True
        if choice == "all":
            ctx["sound_query"] = ""
            _send_sounds_list(index)
            return True
        return True

    if cmd == "de_sounds_list":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back":
            _send_sound_search_menu(index); return True
        if choice == "__sep__":
            _send_sounds_list(index); return True
        pid = g.players[index].peer_id
        g.n.send_reliable(pid, "clip " + choice, 0)
        g.n.send_reliable(pid, f"Copied '{choice}' to clipboard.", 0)
        _send_sounds_list(index)
        return True

    if cmd == "de_give_cat":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back":
            _send_main_menu(index); return True
        ctx = _player_ctx(index)
        ctx["give_category"] = choice
        ctx["give_item"] = None
        _send_give_items_list(index)
        return True

    if cmd == "de_give_item":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back":
            _send_give_cat_menu(index); return True
        ctx = _player_ctx(index)
        ctx["give_item"] = choice
        _send_give_player_list(index)
        return True

    if cmd == "de_give_player":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        ctx = _player_ctx(index)
        if choice == "back":
            _send_give_items_list(index); return True
        if choice == "__manual__":
            ctx["field_key"] = "_give_manual_player"
            ctx["awaiting_input"] = True
            _deinput(g.players[index].peer_id, "_give_manual_player", "Enter target player name:")
            return True
        target_idx = g.get_player_index_from(choice)
        if target_idx == -1 or g.players[target_idx] is None:
            g.n.send_reliable(g.players[index].peer_id, "Player not found or offline.", 0)
            _send_give_player_list(index)
            return True
        _apply_give(index, target_idx)
        return True

    if cmd == "de_cancel":
        ctx = _player_ctx(index)
        prev_field = ctx.get("field_key")
        
        # Intercept announcement cancel
        if prev_field in ("ann_create_title", "ann_create_content"):
            ctx["awaiting_input"] = False
            ctx["field_key"] = None
            ctx.pop("ann_temp_title", None)
            g.n.send_reliable(g.players[index].peer_id, "Edit cancelled.", 0)
            _send_announcements_main_menu(index)
            return True
        elif prev_field and (prev_field.startswith("ann_edit_title:") or prev_field.startswith("ann_edit_content:")):
            ctx["awaiting_input"] = False
            ctx["field_key"] = None
            ann_id = prev_field.split(":")[1]
            g.n.send_reliable(g.players[index].peer_id, "Edit cancelled.", 0)
            _send_announcement_fields(index, ann_id)
            return True

        ctx["awaiting_input"] = False; ctx["field_key"] = None
        ctx.pop("_pending_score", None)
        g.n.send_reliable(g.players[index].peer_id, "Edit cancelled.", 0)

        if prev_field == "_soundquery":
            _send_sound_search_menu(index)
        elif prev_field == "_give_manual_player":
            _send_give_player_list(index)
        elif prev_field in ("_give_amount", "_give_custom_paid", "_give_custom_tokens"):
            _send_give_player_list(index)
        elif prev_field == "_spawner_newmap":
            _spawner_main_menu(index)
        elif prev_field == "_spawner_newtype":
            map_name = ctx.get("spawner_map", "")
            _spawner_list_for_map(index, map_name)
        elif prev_field and prev_field.startswith("spawner:"):
            map_name = ctx.get("spawner_map", "")
            spawner_id = ctx.get("spawner_id", "")
            _spawner_fields_menu(index, map_name, spawner_id)
        else:
            cat = ctx.get("category", "")
            item = ctx.get("item_key", "")
            if cat and item:
                _send_field_list(index, cat, item)
            else:
                _send_main_menu(index)
        return True

    # ── Announcements manager packet handlers ────────────────────────────────
    if cmd == "de_ann_main":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back":
            _send_main_menu(index)
        elif choice == "list":
            _send_announcements_list(index)
        elif choice == "create":
            _prompt_announcement_create_title(index)
        return True

    if cmd == "de_ann_list":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back" or choice == "__none__":
            _send_announcements_main_menu(index)
        else:
            _send_announcement_fields(index, choice)
        return True

    if cmd == "de_ann_fields":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        if choice == "back":
            _send_announcements_list(index)
            return True
        
        parts = choice.split(":")
        field = parts[0]
        ann_id = parts[1]
        
        if field == "title":
            ctx = _player_ctx(index)
            ctx["field_key"] = f"ann_edit_title:{ann_id}"
            ctx["awaiting_input"] = True
            _deinput(g.players[index].peer_id, f"ann_edit_title:{ann_id}", "Enter new title:")
            return True
            
        elif field == "content":
            ctx = _player_ctx(index)
            ctx["field_key"] = f"ann_edit_content:{ann_id}"
            ctx["awaiting_input"] = True
            _deinput(g.players[index].peer_id, f"ann_edit_content:{ann_id}", "Enter new content:")
            return True
            
        elif field == "pinned":
            path = os.path.join(ANN_DIR, f"{ann_id}.announcement")
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    data["pinned"] = not data.get("pinned", False)
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                    g.n.send_reliable(g.players[index].peer_id, f"Announcement pinned status set to {data['pinned']}.", 0)
                except Exception as ex:
                    g.n.send_reliable(g.players[index].peer_id, f"Error toggling pinned status: {ex}", 0)
            _send_announcement_fields(index, ann_id)
            return True
            
        elif field == "delete":
            path = os.path.join(ANN_DIR, f"{ann_id}.announcement")
            if os.path.exists(path):
                try:
                    os.remove(path)
                    g.n.send_reliable(g.players[index].peer_id, "Announcement deleted successfully.", 0)
                except Exception as ex:
                    g.n.send_reliable(g.players[index].peer_id, f"Error deleting announcement: {ex}", 0)
            _send_announcements_list(index)
            return True

    # ── Bot Spawner: map list ────────────────────────────────────────────────
    if cmd == "de_spawner_maps":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        ctx = _player_ctx(index)
        if choice == "back":
            _send_main_menu(index); return True
        if choice == "__newmap__":
            ctx["field_key"] = "_spawner_newmap"
            ctx["awaiting_input"] = True
            _deinput(g.players[index].peer_id, "_spawner_newmap", "Enter map name for new spawner group (e.g. massacre_in_the_city):")
            return True
        ctx["spawner_map"] = choice
        _spawner_list_for_map(index, choice)
        return True

    # ── Bot Spawner: spawner list for map ────────────────────────────────────
    if cmd == "de_spawner_list":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        ctx = _player_ctx(index)
        map_name = ctx.get("spawner_map", "")
        if choice == "back":
            _spawner_main_menu(index); return True
        if choice == "__add__":
            ctx["field_key"] = "_spawner_newtype"
            ctx["awaiting_input"] = True
            _deinput(g.players[index].peer_id, "_spawner_newtype", "Enter bot type for new spawner (npc or zombie):")
            return True
        ctx["spawner_id"] = choice
        _spawner_fields_menu(index, map_name, choice)
        return True

    # ── Bot Spawner: spawner field/action menu ────────────────────────────────
    if cmd == "de_spawner_fields":
        if _require_admin(index): return True
        choice = " ".join(parsed[1:]) if len(parsed) > 1 else "back"
        ctx = _player_ctx(index)
        map_name = ctx.get("spawner_map", "")
        spawner_id = ctx.get("spawner_id", "")
        pid = g.players[index].peer_id
        admin = g.players[index].name

        if choice == "back":
            _spawner_list_for_map(index, map_name); return True

        if choice == "__sep__":
            _spawner_fields_menu(index, map_name, spawner_id); return True

        if choice == "toggle_enabled":
            cfg = _bs().get_spawners_cache()
            sp = next((s for s in cfg.get(map_name, []) if s.get("id") == spawner_id), None)
            if sp:
                sp["enabled"] = not sp.get("enabled", False)
                _bs().save_spawners()
                _bs().load_spawners()
                state = "enabled" if sp["enabled"] else "disabled"
                g.n.send_reliable(pid, f"Spawner '{spawner_id}' {state}.", 0)
                _log_edit(admin, "bot_spawners", spawner_id, "enabled", str(sp["enabled"]))
            _spawner_fields_menu(index, map_name, spawner_id); return True

        if choice == "spawn_now":
            cfg = _bs().get_spawners_cache()
            sp = next((s for s in cfg.get(map_name, []) if s.get("id") == spawner_id), None)
            if sp:
                ok = _bs().spawn_bot_now(map_name, sp)
                if ok:
                    g.n.send_reliable(pid, f"Spawned one {sp.get('type','npc')} on '{map_name}'.", 0)
                else:
                    g.n.send_reliable(pid, f"Cap reached ({sp.get('max_count',5)}) — no bot spawned.", 0)
            _spawner_fields_menu(index, map_name, spawner_id); return True

        if choice == "kill_bots":
            _bs().kill_spawner_bots(map_name, spawner_id)
            g.n.send_reliable(pid, f"Killed all bots from spawner '{spawner_id}'.", 0)
            _spawner_fields_menu(index, map_name, spawner_id); return True

        if choice == "delete":
            cfg = _bs().get_spawners_cache()
            lst = cfg.get(map_name, [])
            cfg[map_name] = [s for s in lst if s.get("id") != spawner_id]
            if not cfg[map_name]:
                del cfg[map_name]
            _bs().kill_spawner_bots(map_name, spawner_id)
            _bs().save_spawners()
            _bs().load_spawners()
            g.n.send_reliable(pid, f"Spawner '{spawner_id}' deleted.", 0)
            _spawner_main_menu(index); return True

        if choice.startswith("field:"):
            field_key = choice[len("field:"):]
            ctx["field_key"] = f"spawner:{field_key}"
            ctx["awaiting_input"] = True
            cfg = _bs().get_spawners_cache()
            sp = next((s for s in cfg.get(map_name, []) if s.get("id") == spawner_id), None)
            current = sp.get(field_key, "?") if sp else "?"
            _deinput(pid, f"spawner:{field_key}", f"{field_key} (current: {current}):")
            return True

        _spawner_fields_menu(index, map_name, spawner_id)
        return True

    return False
