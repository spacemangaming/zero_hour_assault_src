"""
zh_bot_spawner.py -- data-editor-driven bot spawning system.

Bots (NPCs or zombies) can be spawned on any map either manually
or on a schedule.  Configuration lives at:
    server/data/bot_spawners/spawners.json

Schema for each map entry:
{
  "massacre_in_the_city": [
    {
      "id":           "ff_npc_1",      # unique id (auto-generated)
      "type":         "npc",           # "npc" or "zombie"
      "enabled":      false,           # false = config saved but not running
      "max_count":    5,               # hard cap of live bots from this spawner
      "schedule_ms":  30000,           # ms between auto-spawns; 0 = manual only
      "minx": 0, "maxx": 200,
      "miny": 0, "maxy": 200,
      "z":    0,
      # NPC-only fields (ignored for zombie):
      "mind":       30,
      "maxd":       50,
      "health":     100,
      "hitrange":   30,
      "walktime":   150,
      "shoottime":  10,
      "voicesound": "botbeacon"
    }
  ]
}
"""

import globals as g
import json
import os
from timer import timer
from random import randint as random
from npc import npc
from zombie import zombie

_SPAWNER_CONFIG_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "data", "bot_spawners", "spawners.json"
    )
)

# In-memory cache: { map_name: [ spawner_dict, ... ] }
_spawners_cache = {}

# Per spawner-id timers, kept alive for the server lifetime
_spawner_timers = {}


# ---------------------------------------------------------------------------
# Config I/O
# ---------------------------------------------------------------------------

def load_spawners():
    """Load spawner configs from disk into the in-memory cache."""
    global _spawners_cache
    try:
        with open(_SPAWNER_CONFIG_PATH, "r", encoding="utf-8") as f:
            _spawners_cache = json.load(f)
    except FileNotFoundError:
        _spawners_cache = {}
    except Exception as e:
        print(f"[bot_spawner] Error loading spawners: {e}")
        _spawners_cache = {}


def save_spawners():
    """Persist the in-memory cache to disk."""
    os.makedirs(os.path.dirname(_SPAWNER_CONFIG_PATH), exist_ok=True)
    with open(_SPAWNER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(_spawners_cache, f, indent=2)


def get_spawners_cache():
    """Return the live in-memory spawner config dict."""
    return _spawners_cache


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _count_bots(map_name, spawner_id, bot_type):
    """Count currently live bots tagged with this spawner_id on map_name."""
    count = 0
    if bot_type == "npc":
        for n in g.npcs:
            if getattr(n, "_spawner_id", "") == spawner_id and n.map == map_name:
                count += 1
    elif bot_type == "zombie":
        for z in g.zombies:
            if getattr(z, "_spawner_id", "") == spawner_id and z.map == map_name:
                count += 1
    return count


def _do_spawn_npc(map_name, sp, spawner_id):
    n = npc(
        0, 0, "bot", map_name,
        sp.get("voicesound", "botbeacon"),
        sp.get("walktime", 150),
        1, 1,
        sp.get("mind", 30), sp.get("maxd", 50),
        "voice", 16, "nothing", 0,
        5000,
        sp.get("hitrange", 30),
        sp.get("health", 100),
        "voice17", 0,
        sp.get("shoottime", 10),
        sp.get("minx", 0), sp.get("maxx", 200),
        sp.get("miny", 0), sp.get("maxy", 200),
        sp.get("z", 0),
        750, 5, 200
    )
    n._spawner_id = spawner_id
    g.npcs.append(n)


def _do_spawn_zombie(map_name, sp, spawner_id):
    x = random(sp.get("minx", 0), sp.get("maxx", 200))
    y = random(sp.get("miny", 0), sp.get("maxy", 200))
    zb = zombie(x, y, sp.get("z", 0), map_name, "")
    zb._spawner_id = spawner_id
    g.zombies.append(zb)


# ---------------------------------------------------------------------------
# Public spawn API
# ---------------------------------------------------------------------------

def spawn_bot_now(map_name, sp):
    """
    Attempt to spawn one bot for the given spawner config dict.
    Returns True if a bot was spawned, False if the cap was already reached.
    """
    sid = sp.get("id", "manual")
    bot_type = sp.get("type", "npc")
    max_count = sp.get("max_count", 5)
    if _count_bots(map_name, sid, bot_type) >= max_count:
        return False
    if bot_type == "npc":
        _do_spawn_npc(map_name, sp, sid)
    elif bot_type == "zombie":
        _do_spawn_zombie(map_name, sp, sid)
    return True


def kill_spawner_bots(map_name, spawner_id):
    """Remove all live bots belonging to a specific spawner."""
    for n in list(g.npcs):
        if getattr(n, "_spawner_id", "") == spawner_id and n.map == map_name:
            n.health = 0
    for z in list(g.zombies):
        if getattr(z, "_spawner_id", "") == spawner_id and z.map == map_name:
            z.health = 0


# ---------------------------------------------------------------------------
# Game loop hook
# ---------------------------------------------------------------------------

def spawnerloop():
    """Called every game-loop tick. Handles scheduled bot spawns."""
    if not _spawners_cache:
        return
    for map_name, spawners in _spawners_cache.items():
        for sp in spawners:
            if not sp.get("enabled", False):
                continue
            schedule_ms = sp.get("schedule_ms", 0)
            if schedule_ms <= 0:
                continue  # manual-only spawner, skip auto
            sid = sp.get("id", "")
            if not sid:
                continue
            if sid not in _spawner_timers:
                t = timer()
                # Force the timer so the first spawn happens immediately
                t.elapsed = schedule_ms
                _spawner_timers[sid] = t
            t = _spawner_timers[sid]
            if t.elapsed < schedule_ms:
                continue
            t.restart()
            bot_type = sp.get("type", "npc")
            max_count = sp.get("max_count", 5)
            if _count_bots(map_name, sid, bot_type) >= max_count:
                continue
            if bot_type == "npc":
                _do_spawn_npc(map_name, sp, sid)
            elif bot_type == "zombie":
                _do_spawn_zombie(map_name, sp, sid)


# Load config once at import time
load_spawners()
