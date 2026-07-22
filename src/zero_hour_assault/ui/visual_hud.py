"""
visual_hud.py — High-quality in-game minimap overlay for sighted players.

Renders at 2× internal resolution then smoothscales down (supersampling),
giving crisp anti-aliased edges on all platforms, circles, and lines.
"""

from __future__ import annotations
import hashlib
import math
import os
from typing import TYPE_CHECKING

import pygame
import pygame.gfxdraw

if TYPE_CHECKING:
    import globals as g_type


# ── Tile colour palette ───────────────────────────────────────────────────────
_TILE_OVERRIDES: dict[str, tuple[int, int, int]] = {
    "concrete":     (110, 110, 115),
    "concrete2":    (120, 118, 114),
    "concrete3":    (108, 105, 100),
    "concrete4":    (115, 112, 108),
    "concrete5":    (105, 103,  98),
    "concrete6":    ( 95,  93,  90),
    "concrete14":   (130, 128, 125),
    "grass":        ( 72, 140,  50),
    "grass2":       ( 60, 130,  45),
    "dirt":         (140, 105,  65),
    "mud":          (100,  75,  45),
    "hardwood":     (160, 110,  55),
    "wood":         (175, 120,  60),
    "woodfloor":    (190, 140,  80),
    "stone":        (150, 145, 140),
    "rock":         (135, 130, 125),
    "gravel":       (145, 140, 135),
    "metal":        (170, 175, 180),
    "metal2":       (155, 160, 165),
    "sand":         (210, 195, 140),
    "desert":       (205, 185, 120),
    "water":        ( 40,  80, 180),
    "swamp":        ( 50, 100,  60),
    "wallbuilding": ( 80,  80,  85),
    "wall":         ( 90,  90,  95),
    "brick":        (160,  80,  55),
    "tile":         (200, 200, 200),
    "snow":         (220, 230, 240),
    "ice":          (180, 210, 240),
    "void":         ( 10,  10,  15),
    "lava":         (220,  60,  10),
    "carpet":       (140,  40,  60),
}

def _tile_color(name: str) -> tuple[int, int, int]:
    n = name.lower().strip()
    if n in _TILE_OVERRIDES:
        return _TILE_OVERRIDES[n]
    for plen in range(len(n) - 1, 0, -1):
        if n[:plen] in _TILE_OVERRIDES:
            base = _TILE_OVERRIDES[n[:plen]]
            h = int(hashlib.md5(n.encode()).hexdigest(), 16)
            d = (h & 0x1F) - 15
            return (max(0, min(255, base[0]+d)),
                    max(0, min(255, base[1]+(d>>1))),
                    max(0, min(255, base[2]-(d>>2))))
    h = int(hashlib.sha256(n.encode()).hexdigest(), 16)
    return (100+(h&0xFF)%100, 100+((h>>8)&0xFF)%100, 100+((h>>16)&0xFF)%100)


# ── Map parser ────────────────────────────────────────────────────────────────

def _parse_map(map_name: str, maps_dir: str) -> dict:
    path = os.path.join(maps_dir, f"{map_name}.map")
    result = {"maxx": 200, "maxy": 200, "platforms": [], "zones": []}
    if not os.path.exists(path):
        return result
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("//"):
                    continue
                parts = line.split(":")
                key = parts[0].lower()
                if key == "maxx" and len(parts) >= 2:
                    result["maxx"] = int(parts[1].strip())
                elif key == "maxy" and len(parts) >= 2:
                    result["maxy"] = int(parts[1].strip())
                elif key == "platform" and len(parts) >= 8:
                    tile = parts[7].strip()
                    result["platforms"].append({
                        "x1": int(parts[1]), "x2": int(parts[2]),
                        "y1": int(parts[3]), "y2": int(parts[4]),
                        "z1": int(parts[5]), "z2": int(parts[6]),
                        "tile": tile, "color": _tile_color(tile),
                    })
                elif key == "zone" and len(parts) >= 8:
                    result["zones"].append({
                        "x1": int(parts[1]), "x2": int(parts[2]),
                        "y1": int(parts[3]), "y2": int(parts[4]),
                        "name": ":".join(parts[7:]).strip(),
                    })
    except Exception:
        pass
    return result


# ── Drawing helpers ───────────────────────────────────────────────────────────

def _aa_circle(surf: pygame.Surface, color: tuple, cx: int, cy: int, r: int) -> None:
    """Anti-aliased filled circle."""
    if r <= 0:
        return
    pygame.gfxdraw.filled_circle(surf, cx, cy, r, color)
    pygame.gfxdraw.aacircle(surf, cx, cy, r, color)

def _aa_circle_outline(surf: pygame.Surface, fill: tuple, outline: tuple,
                        cx: int, cy: int, r: int, thickness: int = 2) -> None:
    """Filled circle with a contrasting anti-aliased outline."""
    _aa_circle(surf, fill, cx, cy, r)
    for t in range(thickness):
        pygame.gfxdraw.aacircle(surf, cx, cy, r + t, outline)

def _glow_circle(surf: pygame.Surface, color: tuple, cx: int, cy: int,
                 r: int, layers: int = 5) -> None:
    """Draw a glowing halo around a point using decreasing-alpha circles."""
    for i in range(layers, 0, -1):
        alpha = int(80 * (i / layers))
        radius = r + i * 4
        glow_surf = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(glow_surf, radius + 1, radius + 1, radius,
                                     (*color[:3], alpha))
        surf.blit(glow_surf, (cx - radius - 1, cy - radius - 1),
                  special_flags=pygame.BLEND_ALPHA_SDL2)

def _rounded_rect(surf: pygame.Surface, color: tuple, rect: pygame.Rect,
                  radius: int) -> None:
    """Fill a rounded rectangle."""
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def _shadow_rect(surf: pygame.Surface, rect: pygame.Rect, radius: int,
                 blur: int = 8) -> None:
    """Draw a soft drop-shadow behind a rounded rect."""
    for i in range(blur, 0, -1):
        alpha = int(120 * (1 - i / blur))
        s = pygame.Surface((rect.width + i*2, rect.height + i*2), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, alpha),
                         s.get_rect(), border_radius=radius + i)
        surf.blit(s, (rect.x - i, rect.y - i))

def _draw_arrow(surf: pygame.Surface, color: tuple,
                cx: int, cy: int, facing_deg: float,
                length: int = 14, head: int = 6) -> None:
    """Draw a direction arrow (anti-aliased line + arrowhead)."""
    rad = math.radians(facing_deg - 90)
    ex = cx + int(math.cos(rad) * length)
    ey = cy + int(math.sin(rad) * length)
    pygame.draw.aaline(surf, color, (cx, cy), (ex, ey))
    # arrowhead
    left  = math.radians(facing_deg - 90 + 140)
    right = math.radians(facing_deg - 90 - 140)
    pts = [
        (ex, ey),
        (ex + int(math.cos(left)  * head), ey + int(math.sin(left)  * head)),
        (ex + int(math.cos(right) * head), ey + int(math.sin(right) * head)),
    ]
    pygame.gfxdraw.filled_trigon(surf, pts[0][0], pts[0][1],
                                       pts[1][0], pts[1][1],
                                       pts[2][0], pts[2][1], color)
    pygame.gfxdraw.aatrigon(surf, pts[0][0], pts[0][1],
                                   pts[1][0], pts[1][1],
                                   pts[2][0], pts[2][1], color)

def _label(surf: pygame.Surface, font: pygame.font.Font, text: str,
           cx: int, cy: int, color: tuple) -> None:
    """Render a small centred label with a drop shadow."""
    # shadow
    sh = font.render(text, True, (0, 0, 0))
    surf.blit(sh, (cx - sh.get_width()//2 + 1, cy + 1))
    # main text
    tx = font.render(text, True, color)
    surf.blit(tx, (cx - tx.get_width()//2, cy))


# ── Main HUD class ────────────────────────────────────────────────────────────

class VisualHUD:
    """High-quality minimap overlay.

    Renders internally at SCALE× resolution then smoothscales down so every
    edge, circle and line comes out crisp on the actual display.
    """

    # Display size (what the player sees)
    HUD_W   = 420
    HUD_H   = 420
    HUD_PAD = 16
    MAP_PAD = 10

    # Internal supersampling scale — 2 means render at 840×840, display at 420×420
    SCALE   = 2

    OPACITY  = 215
    CORNER_R = 14

    # Font sizes (at display resolution — scaled up internally)
    FONT_SZ  = 11
    TITLE_SZ = 14
    LABEL_SZ = 9

    # Entity sizes (at internal resolution)
    PLAYER_R = 7
    BOT_R    = 6
    NPC_R    = 6
    ITEM_R   = 5
    BOSS_R   = 12

    # Colours
    C_BG        = ( 15,  18,  24)
    C_BG2       = ( 20,  25,  35)   # subtle gradient second colour
    C_BORDER    = ( 55,  65,  80)
    C_BORDER2   = ( 80, 100, 130)   # highlight edge
    C_MAP_BG    = ( 10,  13,  20)
    C_PLAYER    = ( 79, 195, 247)
    C_PLAYER_OL = ( 20,  80, 140)
    C_BOT       = (248, 113, 113)
    C_BOT_OL    = (120,  30,  30)
    C_NPC       = (251, 146,  60)
    C_NPC_OL    = (140,  70,  10)
    C_ITEM      = (250, 204,  21)
    C_BOSS_P1   = (255,  50,  50)
    C_BOSS_P2   = (255, 140,  20)
    C_BOSS_OL   = (255, 255, 100)
    C_SELF      = (100, 255, 120)
    C_SELF_OL   = ( 20, 120,  40)
    C_ZONE      = ( 88, 166, 255)
    C_TITLE     = (230, 237, 243)
    C_SUB       = (139, 148, 158)
    C_WALL_EDGE = (  0,   0,   0, 60)

    def __init__(self) -> None:
        self.visible: bool = False
        self._geo: dict = {}
        self._geo_map: str = ""
        self._font:        pygame.font.Font | None = None
        self._title_font:  pygame.font.Font | None = None
        self._label_font:  pygame.font.Font | None = None
        self._maps_dir: str = ""
        # cached surfaces so we don't recreate each frame
        self._panel_cache: pygame.Surface | None = None
        self._last_map_geo_key: str = ""

    def toggle(self) -> None:
        self.visible = not self.visible

    # ── internal helpers ──────────────────────────────────────────────────────

    def _init_fonts(self) -> None:
        if self._font is not None:
            return
        try:
            self._font       = pygame.font.SysFont("segoeui", self.FONT_SZ)
            self._title_font = pygame.font.SysFont("segoeui", self.TITLE_SZ, bold=True)
            self._label_font = pygame.font.SysFont("segoeui", self.LABEL_SZ)
        except Exception:
            self._font       = pygame.font.Font(None, self.FONT_SZ + 4)
            self._title_font = pygame.font.Font(None, self.TITLE_SZ + 4)
            self._label_font = pygame.font.Font(None, self.LABEL_SZ + 4)

    def _ensure_geo(self, map_name: str, maps_dir: str) -> None:
        if map_name != self._geo_map:
            self._geo_map = map_name
            self._geo = _parse_map(map_name, maps_dir)
            self._panel_cache = None  # invalidate geometry cache

    def _s(self, v: int) -> int:
        """Scale a value to internal resolution."""
        return v * self.SCALE

    # ── static panel (background + map geometry, rebuilt when map changes) ────

    def _build_geo_surface(self, IW: int, IH: int,
                            map_top: int, map_left: int,
                            map_w: int, map_h: int) -> pygame.Surface:
        """Build the static geometry layer (platforms + zones) at internal res."""
        geo  = self._geo
        maxx = max(geo.get("maxx", 200), 1)
        maxy = max(geo.get("maxy", 200), 1)
        sx   = map_w / maxx
        sy   = map_h / maxy

        geo_surf = pygame.Surface((map_w, map_h))
        geo_surf.fill(self.C_MAP_BG)

        def w2s(wx, wy):
            return int(wx * sx), int(wy * sy)

        # Platforms — floor first, then walls on top
        floors = [p for p in geo.get("platforms", []) if p["z1"] == 0 and p["z2"] == 0]
        walls  = [p for p in geo.get("platforms", []) if not (p["z1"] == 0 and p["z2"] == 0)]

        for plat in floors + walls:
            px, py = w2s(plat["x1"], plat["y1"])
            pw = max(2, int((plat["x2"] - plat["x1"]) * sx))
            ph = max(2, int((plat["y2"] - plat["y1"]) * sy))
            col = plat["color"]
            is_wall = plat not in floors
            if is_wall:
                col = (max(0, col[0]-40), max(0, col[1]-40), max(0, col[2]-40))
            pygame.draw.rect(geo_surf, col, (px, py, pw, ph))
            # subtle inner border for depth
            border_col = (min(255, col[0]+30), min(255, col[1]+30), min(255, col[2]+30))
            pygame.draw.rect(geo_surf, border_col, (px, py, pw, ph), 1)

        # Zone fills
        for zone in geo.get("zones", []):
            zx, zy = w2s(zone["x1"], zone["y1"])
            zw = max(2, int((zone["x2"] - zone["x1"]) * sx))
            zh = max(2, int((zone["y2"] - zone["y1"]) * sy))
            zs = pygame.Surface((zw, zh), pygame.SRCALPHA)
            zs.fill((*self.C_ZONE, 25))
            geo_surf.blit(zs, (zx, zy))
            pygame.draw.rect(geo_surf, (*self.C_ZONE, 80), (zx, zy, zw, zh), 1)

        return geo_surf

    # ── main draw ─────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, g) -> None:
        if not self.visible:
            return
        self._init_fonts()

        map_name = getattr(g, "mapname", "")
        maps_dir = self._maps_dir or os.path.join(os.getcwd(), "maps")
        self._ensure_geo(map_name, maps_dir)

        sw, sh = screen.get_size()

        # ── Internal (supersampled) surface ───────────────────────────────────
        S      = self.SCALE
        IW     = self.HUD_W * S
        IH     = self.HUD_H * S
        ipad   = self.MAP_PAD * S
        ititle = (self.TITLE_SZ + 8) * S
        MAP_TOP  = ipad + ititle
        MAP_LEFT = ipad
        MAP_W    = IW - ipad * 2
        MAP_H    = IH - MAP_TOP - ipad * 2 - self.FONT_SZ * S  # leave legend room

        internal = pygame.Surface((IW, IH), pygame.SRCALPHA)

        # ── Background ────────────────────────────────────────────────────────
        # Gradient: darker at top, slightly lighter at bottom
        for y in range(IH):
            t = y / IH
            r = int(self.C_BG[0] + (self.C_BG2[0] - self.C_BG[0]) * t)
            gv = int(self.C_BG[1] + (self.C_BG2[1] - self.C_BG[1]) * t)
            b = int(self.C_BG[2] + (self.C_BG2[2] - self.C_BG[2]) * t)
            pygame.draw.line(internal, (r, gv, b, self.OPACITY), (0, y), (IW, y))

        # Rounded border
        pygame.draw.rect(internal, (*self.C_BORDER2, 180),
                         pygame.Rect(0, 0, IW, IH),
                         width=S * 2, border_radius=self.CORNER_R * S)
        pygame.draw.rect(internal, (*self.C_BORDER, 120),
                         pygame.Rect(S, S, IW - S*2, IH - S*2),
                         width=S, border_radius=(self.CORNER_R - 1) * S)

        # ── Title bar ─────────────────────────────────────────────────────────
        # Subtle separator line under title
        sep_y = MAP_TOP - ipad // 2
        pygame.draw.line(internal, (*self.C_BORDER, 180),
                         (ipad, sep_y), (IW - ipad, sep_y), S)

        title_surf = self._title_font.render(map_name or "Map", True, self.C_TITLE)
        ts = pygame.transform.smoothscale(title_surf,
             (title_surf.get_width() * S, title_surf.get_height() * S))
        internal.blit(ts, (ipad, ipad))

        hint_surf = self._font.render("Alt+M: hide", True, self.C_SUB)
        hs = pygame.transform.smoothscale(hint_surf,
             (hint_surf.get_width() * S, hint_surf.get_height() * S))
        internal.blit(hs, (IW - hs.get_width() - ipad, ipad + S*2))

        # ── Map background ────────────────────────────────────────────────────
        map_rect = pygame.Rect(MAP_LEFT, MAP_TOP, MAP_W, MAP_H)
        pygame.draw.rect(internal, self.C_MAP_BG, map_rect, border_radius=S * 4)

        # Clip all map drawing to the map area
        map_surf = pygame.Surface((MAP_W, MAP_H), pygame.SRCALPHA)

        geo  = self._geo
        maxx = max(geo.get("maxx", 200), 1)
        maxy = max(geo.get("maxy", 200), 1)
        sx   = MAP_W / maxx
        sy   = MAP_H / maxy

        def w2s(wx, wy):
            return int(float(wx) * sx), int(float(wy) * sy)

        # ── Static geometry ───────────────────────────────────────────────────
        geo_key = f"{map_name}_{MAP_W}_{MAP_H}"
        if geo_key != self._last_map_geo_key or self._panel_cache is None:
            self._panel_cache  = self._build_geo_surface(IW, IH, MAP_TOP, MAP_LEFT, MAP_W, MAP_H)
            self._last_map_geo_key = geo_key
        map_surf.blit(self._panel_cache, (0, 0))

        # ── Items ─────────────────────────────────────────────────────────────
        for item in getattr(g, "items", []):
            if getattr(item, "map", "") != map_name:
                continue
            ix, iy = w2s(getattr(item, "x", 0), getattr(item, "y", 0))
            _aa_circle_outline(map_surf, self.C_ITEM, (100, 80, 0),
                               ix, iy, self.ITEM_R, 2)

        # ── NPCs ──────────────────────────────────────────────────────────────
        for npc in getattr(g, "npcs", []):
            if getattr(npc, "map", "") != map_name or getattr(npc, "dead", False):
                continue
            nx, ny = w2s(getattr(npc, "x", 0), getattr(npc, "y", 0))
            r = self.NPC_R
            pts = [(nx, ny - r), (nx + r, ny + r), (nx - r, ny + r)]
            pygame.gfxdraw.filled_trigon(map_surf,
                pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1],
                (*self.C_NPC, 255))
            pygame.gfxdraw.aatrigon(map_surf,
                pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1],
                self.C_NPC_OL)

        # ── Boss ──────────────────────────────────────────────────────────────
        boss_data = getattr(g, "tracked_boss", None)
        if boss_data and boss_data.get("map") == map_name:
            bx, by = w2s(boss_data["x"], boss_data["y"])
            t       = pygame.time.get_ticks() / 600.0
            pulse   = int(abs(math.sin(t)) * 4)
            col     = self.C_BOSS_P2 if boss_data.get("phase2") else self.C_BOSS_P1
            _glow_circle(map_surf, col, bx, by, self.BOSS_R + pulse, layers=6)
            _aa_circle_outline(map_surf, col, self.C_BOSS_OL,
                               bx, by, self.BOSS_R + pulse, 3)
            # X mark
            d = self.BOSS_R - 2
            pygame.draw.aaline(map_surf, (255,255,255), (bx-d, by-d), (bx+d, by+d))
            pygame.draw.aaline(map_surf, (255,255,255), (bx+d, by-d), (bx-d, by+d))

        # ── Other players ─────────────────────────────────────────────────────
        for p in getattr(g, "players", []):
            if getattr(p, "map", "") != map_name or getattr(p, "dead", False):
                continue
            px2, py2  = w2s(getattr(p, "x", 0), getattr(p, "y", 0))
            is_bot    = getattr(p, "isbot", False)
            col       = self.C_BOT    if is_bot else self.C_PLAYER
            col_ol    = self.C_BOT_OL if is_bot else self.C_PLAYER_OL
            r         = self.BOT_R    if is_bot else self.PLAYER_R
            _aa_circle_outline(map_surf, col, col_ol, px2, py2, r, 2)
            facing = getattr(p, "facing", 0)
            _draw_arrow(map_surf, col, px2, py2, facing, length=r+6, head=4)
            # name label
            pname = getattr(p, "name", "")
            if pname and self._label_font:
                _label(map_surf, self._label_font, pname,
                       px2, py2 - r - 10, col)

        # ── Self ──────────────────────────────────────────────────────────────
        me = getattr(g, "me", None)
        if me is not None:
            mx2, my2 = w2s(getattr(me, "x", 0), getattr(me, "y", 0))
            _glow_circle(map_surf, self.C_SELF, mx2, my2, self.PLAYER_R, layers=3)
            _aa_circle_outline(map_surf, self.C_SELF, self.C_SELF_OL,
                               mx2, my2, self.PLAYER_R + 1, 2)
            facing = getattr(g, "facing", 0)
            _draw_arrow(map_surf, self.C_SELF, mx2, my2, facing,
                        length=self.PLAYER_R + 8, head=5)

        internal.blit(map_surf, (MAP_LEFT, MAP_TOP))

        # ── Legend ────────────────────────────────────────────────────────────
        legend_y = MAP_TOP + MAP_H + ipad // 2
        legend_items = [
            (self.C_SELF,   "You"),
            (self.C_PLAYER, "Player"),
            (self.C_BOT,    "Bot"),
            (self.C_NPC,    "NPC"),
            (self.C_BOSS_P1,"Boss"),
            (self.C_ITEM,   "Item"),
        ]
        lx = ipad + S * 4
        for col, lbl in legend_items:
            _aa_circle(internal, col, lx, legend_y + self.FONT_SZ * S // 2, S * 4)
            txt = self._font.render(lbl, True, self.C_SUB)
            ts2 = pygame.transform.smoothscale(txt,
                  (txt.get_width() * S, txt.get_height() * S))
            internal.blit(ts2, (lx + S * 7, legend_y))
            lx += ts2.get_width() + S * 14
            if lx > IW - S * 20:
                break

        # ── Smoothscale down to display size and blit ─────────────────────────
        final = pygame.transform.smoothscale(internal, (self.HUD_W, self.HUD_H))

        # Drop shadow
        hx = sw - self.HUD_W - self.HUD_PAD
        hy = sh - self.HUD_H - self.HUD_PAD
        shadow = pygame.Surface((self.HUD_W + 20, self.HUD_H + 20), pygame.SRCALPHA)
        for i in range(10, 0, -1):
            a = int(100 * (1 - i / 10))
            pygame.draw.rect(shadow, (0, 0, 0, a),
                             pygame.Rect(i, i, self.HUD_W + (10-i)*2, self.HUD_H + (10-i)*2),
                             border_radius=self.CORNER_R + i)
        screen.blit(shadow, (hx - 10, hy - 10))
        screen.blit(final, (hx, hy))

        # ── Stats panel (always visible when inthegame) ───────────────────────
        self._draw_stats(screen, g, sw, sh)

    # ── Stats panel ───────────────────────────────────────────────────────────

    # Stats panel dimensions
    STATS_W = 280
    STATS_H = 160

    def _draw_stats(self, screen: pygame.Surface, g, sw: int, sh: int) -> None:
        """Draw health/ammo/coords panel in the bottom-left corner."""
        S  = self.STATS_W * 2   # internal width (2× supersampling)
        SH = self.STATS_H * 2
        PAD = 16

        surf = pygame.Surface((S, SH), pygame.SRCALPHA)

        # Background gradient
        for y in range(SH):
            t = y / SH
            r = int(self.C_BG[0] + (self.C_BG2[0] - self.C_BG[0]) * t)
            gv = int(self.C_BG[1] + (self.C_BG2[1] - self.C_BG[1]) * t)
            b = int(self.C_BG[2] + (self.C_BG2[2] - self.C_BG[2]) * t)
            pygame.draw.line(surf, (r, gv, b, self.OPACITY), (0, y), (S, y))

        pygame.draw.rect(surf, (*self.C_BORDER2, 180),
                         pygame.Rect(0, 0, S, SH), width=2, border_radius=14*2)

        def blit_text(text, x, y, color, font):
            ts = font.render(text, True, (0, 0, 0))
            surf.blit(ts, (x+1, y+1))  # shadow
            ts = font.render(text, True, color)
            surf.blit(ts, (x, y))

        font_big  = pygame.font.SysFont("segoeui", 22, bold=True)
        font_med  = pygame.font.SysFont("segoeui", 17)
        font_sm   = pygame.font.SysFont("segoeui", 14)

        hp      = getattr(g, "hud_health",    100)
        maxhp   = getattr(g, "hud_maxhealth", 100)
        w1      = getattr(g, "hud_weapon",    "none")
        loaded1 = getattr(g, "hud_loaded",    -1)
        res1    = getattr(g, "hud_reserve",   -1)
        w2      = getattr(g, "hud_weapon2",   "none")
        loaded2 = getattr(g, "hud_loaded2",   -1)
        res2    = getattr(g, "hud_reserve2",  -1)
        shield  = getattr(g, "hud_shield",    0)
        helmet  = getattr(g, "hud_helmet",    0)
        me      = getattr(g, "me", None)
        facing  = getattr(g, "facing", 0)

        cx, cy = PAD, PAD

        # ── Health bar ────────────────────────────────────────────────────────
        ratio = max(0.0, min(1.0, hp / max(maxhp, 1)))
        bar_w = S - PAD * 2
        bar_h = 22
        # track
        pygame.draw.rect(surf, (40, 10, 10, 200), (cx, cy, bar_w, bar_h), border_radius=6)
        # fill — colour shifts red→yellow→green
        if ratio > 0.5:
            fill_col = (int(255*(1-ratio)*2), 220, 40)
        else:
            fill_col = (220, int(220*ratio*2), 20)
        fill_w = max(4, int(bar_w * ratio))
        pygame.draw.rect(surf, fill_col, (cx, cy, fill_w, bar_h), border_radius=6)
        # highlight strip
        pygame.draw.rect(surf, (255, 255, 255, 50), (cx, cy, fill_w, bar_h//3), border_radius=6)
        # label
        hp_text = f"HP  {hp} / {maxhp}"
        blit_text(hp_text, cx + 6, cy + 2, (230, 237, 243), font_med)
        cy += bar_h + 8

        # ── Shield / helmet strip ─────────────────────────────────────────────
        if shield > 0 or helmet > 0:
            detail = []
            if shield > 0: detail.append(f"🛡 {shield}%")
            if helmet > 0: detail.append(f"⛑ {helmet}%")
            blit_text("  ".join(detail), cx, cy, (139, 148, 158), font_sm)
            cy += 20

        # ── Weapon 1 ──────────────────────────────────────────────────────────
        if w1 and w1 not in ("none", "punch"):
            ammo_str = f"{loaded1} | {res1}" if loaded1 >= 0 else "∞"
            blit_text(f"▶ {w1}", cx, cy, (79, 195, 247), font_med)
            blit_text(ammo_str, S - PAD - font_med.size(ammo_str)[0], cy, (250, 204, 21), font_med)
            cy += 22

        # ── Weapon 2 ──────────────────────────────────────────────────────────
        if w2 and w2 not in ("none", "feet"):
            ammo_str2 = f"{loaded2} | {res2}" if loaded2 >= 0 else "∞"
            blit_text(f"  {w2}", cx, cy, (139, 148, 158), font_sm)
            blit_text(ammo_str2, S - PAD - font_sm.size(ammo_str2)[0], cy, (180, 160, 60), font_sm)
            cy += 18

        # ── Coordinates ───────────────────────────────────────────────────────
        if me is not None:
            mx = round(getattr(me, "x", 0))
            my = round(getattr(me, "y", 0))
            mz = round(getattr(me, "z", 0))
            coord_str = f"X {mx}  Y {my}  Z {mz}  ↗ {facing}°"
            blit_text(coord_str, cx, SH - PAD - font_sm.get_height(), (139, 148, 158), font_sm)

        # Scale down and blit bottom-left
        final = pygame.transform.smoothscale(surf, (self.STATS_W, self.STATS_H))

        # drop shadow
        shadow = pygame.Surface((self.STATS_W + 16, self.STATS_H + 16), pygame.SRCALPHA)
        for i in range(8, 0, -1):
            a = int(90 * (1 - i / 8))
            pygame.draw.rect(shadow, (0, 0, 0, a),
                             pygame.Rect(i, i, self.STATS_W + (8-i)*2, self.STATS_H + (8-i)*2),
                             border_radius=14 + i)
        screen.blit(shadow, (self.HUD_PAD - 8, sh - self.STATS_H - self.HUD_PAD - 8))
        screen.blit(final,  (self.HUD_PAD,     sh - self.STATS_H - self.HUD_PAD))


# Module-level singleton
hud = VisualHUD()
