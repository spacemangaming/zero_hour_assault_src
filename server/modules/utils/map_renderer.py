"""
map_renderer.py — Procedural map parser and color engine.

Parses .map files and assigns deterministic tile colors derived from the
tile name via a hash-seeded palette. Used by the dashboard live-map API
and can be imported by any module that needs map geometry.

Public API:
  parse_map(map_name)   -> dict  (platforms, zones, ambs, bounds)
  tile_color(tile_name) -> (r, g, b)
  all_map_names()       -> list[str]
"""

from __future__ import annotations
import os
import hashlib

# Where .map files live, relative to server root
_SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_MAPS_DIR = os.path.join(_SERVER_ROOT, "maps")


# ── Curated overrides so common surfaces look sensible ────────────────────────
_TILE_COLOR_OVERRIDES: dict[str, tuple[int, int, int]] = {
    # Concrete family
    "concrete":    (110, 110, 115),
    "concrete2":   (120, 118, 114),
    "concrete3":   (108, 105, 100),
    "concrete4":   (115, 112, 108),
    "concrete5":   (105, 103,  98),
    "concrete6":   ( 95,  93,  90),
    "concrete14":  (130, 128, 125),
    # Dirt / grass
    "grass":       ( 72, 140,  50),
    "grass2":      ( 60, 130,  45),
    "dirt":        (140, 105,  65),
    "mud":         (100,  75,  45),
    # Wood
    "hardwood":    (160, 110,  55),
    "wood":        (175, 120,  60),
    "woodfloor":   (190, 140,  80),
    # Stone / rock
    "stone":       (150, 145, 140),
    "rock":        (135, 130, 125),
    "gravel":      (145, 140, 135),
    # Metal
    "metal":       (170, 175, 180),
    "metal2":      (155, 160, 165),
    # Sand
    "sand":        (210, 195, 140),
    "desert":      (205, 185, 120),
    # Water
    "water":       ( 40,  80, 180),
    "swamp":       ( 50, 100,  60),
    # Buildings / walls
    "wallbuilding": ( 80,  80,  85),
    "wall":        ( 90,  90,  95),
    "brick":       (160,  80,  55),
    "tile":        (200, 200, 200),
    # Snow / ice
    "snow":        (220, 230, 240),
    "ice":         (180, 210, 240),
    # Special
    "void":        ( 10,  10,  15),
    "lava":        (220,  60,  10),
    "carpet":      (140,  40,  60),
}


def tile_color(tile_name: str) -> tuple[int, int, int]:
    """Return an RGB tuple for a tile type.

    Named tiles use the curated overrides; everything else gets a
    deterministic colour derived from SHA-256 of the tile name so that
    the same unknown tile always renders the same colour.
    """
    name = tile_name.lower().strip()
    if name in _TILE_COLOR_OVERRIDES:
        return _TILE_COLOR_OVERRIDES[name]

    # Find longest matching prefix in the overrides
    for prefix_len in range(len(name) - 1, 0, -1):
        if name[:prefix_len] in _TILE_COLOR_OVERRIDES:
            base = _TILE_COLOR_OVERRIDES[name[:prefix_len]]
            # Slightly vary the base color using the hash of the full name
            h = int(hashlib.md5(name.encode()).hexdigest(), 16)
            delta = ((h >> 0) & 0x1F) - 15  # -15..+16
            return (
                max(0, min(255, base[0] + delta)),
                max(0, min(255, base[1] + (delta >> 1))),
                max(0, min(255, base[2] - (delta >> 2))),
            )

    # Fully unknown tile: hash-derived pastel
    h = int(hashlib.sha256(name.encode()).hexdigest(), 16)
    r = 100 + (h & 0xFF) % 100
    g = 100 + ((h >> 8) & 0xFF) % 100
    b = 100 + ((h >> 16) & 0xFF) % 100
    return (r, g, b)


def parse_map(map_name: str) -> dict:
    """Parse a .map file and return structured geometry.

    Returns a dict with keys:
      name      str
      maxx, maxy, maxz  int
      platforms list[dict]  — each: {x1,x2,y1,y2,z1,z2,tile,color}
      zones     list[dict]  — each: {x1,x2,y1,y2,z1,z2,name}
      ambs      list[dict]  — each: {x1,x2,y1,y2,z1,z2,file,vol}
    """
    path = os.path.join(_MAPS_DIR, f"{map_name}.map")
    if not os.path.exists(path):
        return {}

    result: dict = {
        "name":      map_name,
        "maxx":      200,
        "maxy":      200,
        "maxz":      500,
        "platforms": [],
        "zones":     [],
        "ambs":      [],
    }

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("//"):
                    continue
                parts = line.split(":")
                key = parts[0].lower()

                if key == "maxx" and len(parts) >= 2:
                    result["maxx"] = _int(parts[1])
                elif key == "maxy" and len(parts) >= 2:
                    result["maxy"] = _int(parts[1])
                elif key == "maxz" and len(parts) >= 2:
                    result["maxz"] = _int(parts[1])

                elif key == "platform" and len(parts) >= 8:
                    tile = parts[7].strip()
                    result["platforms"].append({
                        "x1":    _int(parts[1]),
                        "x2":    _int(parts[2]),
                        "y1":    _int(parts[3]),
                        "y2":    _int(parts[4]),
                        "z1":    _int(parts[5]),
                        "z2":    _int(parts[6]),
                        "tile":  tile,
                        "color": tile_color(tile),
                    })

                elif key == "zone" and len(parts) >= 8:
                    result["zones"].append({
                        "x1":   _int(parts[1]),
                        "x2":   _int(parts[2]),
                        "y1":   _int(parts[3]),
                        "y2":   _int(parts[4]),
                        "z1":   _int(parts[5]),
                        "z2":   _int(parts[6]),
                        "name": ":".join(parts[7:]).strip(),
                    })

                elif key == "amb" and len(parts) >= 8:
                    result["ambs"].append({
                        "x1":   _int(parts[1]),
                        "x2":   _int(parts[2]),
                        "y1":   _int(parts[3]),
                        "y2":   _int(parts[4]),
                        "z1":   _int(parts[5]),
                        "z2":   _int(parts[6]),
                        "file": parts[7].strip(),
                        "vol":  float(parts[8]) if len(parts) >= 9 else 0.0,
                    })
    except Exception:
        pass

    return result


def all_map_names() -> list[str]:
    """Return sorted list of available map names (no extension)."""
    if not os.path.isdir(_MAPS_DIR):
        return []
    return sorted(
        f[:-4] for f in os.listdir(_MAPS_DIR)
        if f.endswith(".map") and not f.startswith(".")
    )


def _int(s: str) -> int:
    try:
        return int(s.strip())
    except ValueError:
        return 0
