"""
data_loader.py — central config loader for Zero Hour Assault.

Loads all JSON files from server/data/ at startup and exposes typed
accessor functions. Call reload_all() at runtime to hot-reload without
restarting the server.

All paths are relative to the server/ working directory (where
zhaserver.py lives), so data/ resolves to server/data/.
"""

import json
import os

# ── internal state ────────────────────────────────────────────────────────────
_weapons: dict = {}       # key: weapon name, value: stat dict
_characters: dict = {}    # key: char name, value: stat dict
_ranks: list = []         # sorted list of {score, name}
_zombie: dict = {}
_npc_loadouts: dict = {}
_npc_random_loadouts: dict = {}
_npc_healing: list = []
_loot_table: dict = {}
_chest_pool: dict = {}
_inventory_limits: dict = {}
_token_packs: dict = {}
_item_sounds: dict = {}

_DATA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
)



# ── helpers ───────────────────────────────────────────────────────────────────

def _load_json(path: str) -> dict | list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_subdir(subdir: str) -> dict:
    """Merge all .json files in data/<subdir>/ into one dict.

    Each file's stem becomes the key unless the JSON itself has a
    'weapon_key' override (used for filenames that can't contain special
    chars like '&').
    """
    result = {}
    folder = os.path.join(_DATA_DIR, subdir)
    if not os.path.isdir(folder):
        return result
    for fname in os.listdir(folder):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        data = _load_json(path)
        # Allow the JSON to declare its own key (e.g. "S&WModel66")
        key = data.get("weapon_key") or os.path.splitext(fname)[0]
        result[key] = data
    return result


# ── load / reload ─────────────────────────────────────────────────────────────

def _load_weapons():
    global _weapons
    _weapons = _load_subdir("weapons")
    _validate_weapons()


def _validate_weapons():
    required = {"bullet", "range", "min_damage", "max_damage", "spread"}
    for name, w in _weapons.items():
        missing = required - w.keys()
        if missing:
            raise ValueError(f"Weapon '{name}' is missing fields: {missing}")


def _load_characters():
    global _characters
    _characters = _load_subdir("characters")


def _load_ranks():
    global _ranks
    path = os.path.join(_DATA_DIR, "ranks", "ranks.json")
    _ranks = _load_json(path)
    _ranks.sort(key=lambda r: r["score"])


def _load_zombie():
    global _zombie
    path = os.path.join(_DATA_DIR, "zombies", "zombie.json")
    _zombie = _load_json(path)


def _load_npc():
    global _npc_loadouts, _npc_random_loadouts, _npc_healing
    _npc_loadouts = _load_json(os.path.join(_DATA_DIR, "npc", "loadouts.json"))
    _npc_random_loadouts = _load_json(os.path.join(_DATA_DIR, "npc", "random_loadouts.json"))
    _npc_healing = _load_json(os.path.join(_DATA_DIR, "npc", "healing.json"))


def _load_items():
    global _loot_table, _inventory_limits, _item_sounds
    _loot_table = _load_json(os.path.join(_DATA_DIR, "items", "loot_table.json"))
    _inventory_limits = _load_json(os.path.join(_DATA_DIR, "items", "inventory_limits.json"))
    _item_sounds = _load_json(os.path.join(_DATA_DIR, "items", "sounds.json"))


def _load_chest():
    global _chest_pool
    _chest_pool = _load_json(os.path.join(_DATA_DIR, "chest", "chest_items.json"))


def _load_economy():
    global _token_packs
    _token_packs = _load_json(os.path.join(_DATA_DIR, "economy", "token_packs.json"))


def reload_all():
    """Hot-reload every config file. Safe to call at runtime."""
    _load_weapons()
    _load_characters()
    _load_ranks()
    _load_zombie()
    _load_npc()
    _load_items()
    _load_chest()
    _load_economy()
    print("[data_loader] All configs reloaded.")


# Load on import
reload_all()


# ── public accessors ──────────────────────────────────────────────────────────

def get_weapon(name: str) -> dict:
    """Return the stat dict for a weapon, or {} if unknown."""
    return _weapons.get(name, {})


def get_all_weapons() -> dict:
    return _weapons


def get_character(name: str) -> dict:
    """Return the stat dict for a character. Falls back to 'tristan'."""
    return _characters.get(name) or _characters.get("tristan", {})


def get_all_characters() -> dict:
    """Return every loaded character keyed by name."""
    return _characters


def get_rank(score: int) -> str:
    """Return the rank name for a given score (highest threshold that fits)."""
    rank = "Bronze"
    for entry in _ranks:
        if score >= entry["score"]:
            rank = entry["name"]
    return rank


def get_zombie_stats() -> dict:
    return _zombie


def get_npc_loadout(matchmode: str) -> dict:
    """Return the loadout dict for a matchmode, falling back to 'default'."""
    return _npc_loadouts.get(matchmode) or _npc_loadouts.get("default", {})


def get_npc_random_loadouts() -> list:
    return _npc_random_loadouts.get("npc", [])


def get_player_random_loadouts() -> list:
    return _npc_random_loadouts.get("player", [])


def get_npc_healing() -> list:
    return _npc_healing


def get_loot_table() -> dict:
    return _loot_table


def get_chest_config() -> dict:
    return _chest_pool


def get_chest_pool() -> dict:
    return _chest_pool.get("pool", {})


def get_inventory_limits() -> dict:
    return _inventory_limits


def get_inventory_limit(item: str) -> int:
    return _inventory_limits.get(item, -1)


def get_token_pack_amount(pack: str) -> int:
    return _token_packs.get(pack, 0)


def get_item_sounds() -> dict:
    return _item_sounds


def get_item_sound(item: str) -> str:
    """Return the pickup sound for an item, defaulting to '_default'."""
    sounds = _item_sounds
    return sounds.get(item) or sounds.get("_default", "itemget")


def get_wdata_string(name: str) -> str:
    """Return the legacy 'wdata' string '<fire_interval> <auto|norm>' for a weapon."""
    w = _weapons.get(name)
    if not w:
        return ""
    interval = w.get("fire_interval", 1000)
    mode = "auto" if w.get("auto", False) else "norm"
    return f"{interval} {mode}"


def build_wdata_dict() -> dict:
    """Build the complete g.wdata dict from weapon configs."""
    result = {}
    for name, w in _weapons.items():
        interval = w.get("fire_interval", 1000)
        mode = "auto" if w.get("auto", False) else "norm"
        result[name] = f"{interval} {mode}"
    return result


def get_guns_list() -> list:
    """Return all weapons that use ammo (ammo_type is not null), sorted alphabetically."""
    return sorted(name for name, w in _weapons.items() if w.get("ammo_type") is not None)


def get_guns2_list() -> list:
    """Return all weapons sorted by npc_priority (ascending = preferred by NPCs)."""
    items = [(w.get("npc_priority", 99), name) for name, w in _weapons.items()]
    items.sort()
    return [name for _, name in items]
