"""
visual_hud.py — In-game 2D visual minimap overlay for sighted players.

Renders a top-down minimap in the bottom-right corner of the pygame screen
showing the current map geometry, player positions, nearby NPCs, items, and
(when on the megaboss map) the boss.

Usage:
  from ui.visual_hud import VisualHUD
  hud = VisualHUD()
  # In main loop:
  hud.toggle()   # call when M key pressed
  hud.draw(g.screen, g)

The minimap is purely additive — it never interferes with audio gameplay.
Blind players are not affected; the HUD is invisible until toggled on.
"""

from __future__ import annotations
import hashlib
import math
import os
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    import globals as g_type  # type annotation only


# ── Tile color palette (mirrors map_renderer.py for consistency) ──────────────
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
    for plen in range(len(n)-1, 0, -1):
        if n[:plen] in _TILE_OVERRIDES:
            base = _TILE_OVERRIDES[n[:plen]]
            h = int(hashlib.md5(n.encode()).hexdigest(), 16)
            d = (h & 0x1F) - 15
            return (max(0,min(255,base[0]+d)), max(0,min(255,base[1]+(d>>1))), max(0,min(255,base[2]-(d>>2))))
    h = int(hashlib.sha256(n.encode()).hexdigest(), 16)
    return (100+(h&0xFF)%100, 100+((h>>8)&0xFF)%100, 100+((h>>16)&0xFF)%100)


# ── Map geometry parser (client-side, reads maps/ folder) ────────────────────

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


class VisualHUD:
    """Pygame minimap overlay.

    Call `toggle()` on a keypress, `draw(screen, g)` every frame.
    Completely no-ops when hidden.
    """

    # HUD dimensions and position (bottom-right corner)
    HUD_W    = 280
    HUD_H    = 280
    HUD_PAD  = 12       # padding from screen edge
    MAP_PAD  = 8        # inner padding inside the map frame
    OPACITY  = 200      # 0-255 transparency of background panel
    FONT_SZ  = 11
    TITLE_SZ = 13

    # Entity dot sizes
    PLAYER_R = 4
    BOT_R    = 3
    NPC_R    = 3
    ITEM_R   = 3
    BOSS_R   = 7

    # Colors
    C_BG        = (22, 27, 34)
    C_BORDER    = (48, 54, 61)
    C_PLAYER    = (79, 195, 247)    # cyan
    C_BOT       = (248, 113, 113)   # red-ish
    C_NPC       = (251, 146, 60)    # orange
    C_ITEM      = (250, 204, 21)    # yellow
    C_BOSS_P1   = (255, 50, 50)
    C_BOSS_P2   = (255, 120, 20)
    C_ZONE_LINE = (88, 166, 255, 60)
    C_SELF      = (100, 255, 100)   # bright green = local player
    C_TITLE     = (230, 237, 243)
    C_SUB       = (139, 148, 158)

    def __init__(self) -> None:
        self.visible: bool = False
        self._geo: dict = {}
        self._geo_map: str = ""
        self._font: pygame.font.Font | None = None
        self._title_font: pygame.font.Font | None = None
        self._surface: pygame.Surface | None = None
        self._maps_dir: str = ""

    def toggle(self) -> None:
        self.visible = not self.visible

    def _init_fonts(self) -> None:
        if self._font is None:
            try:
                self._font       = pygame.font.SysFont("segoeui", self.FONT_SZ)
                self._title_font = pygame.font.SysFont("segoeui", self.TITLE_SZ, bold=True)
            except Exception:
                self._font       = pygame.font.Font(None, self.FONT_SZ + 4)
                self._title_font = pygame.font.Font(None, self.TITLE_SZ + 4)

    def _ensure_geo(self, map_name: str, maps_dir: str) -> None:
        if map_name != self._geo_map:
            self._geo_map = map_name
            self._geo = _parse_map(map_name, maps_dir)

    def draw(self, screen: pygame.Surface, g) -> None:
        """Render the HUD onto *screen*. Call every frame; no-ops if hidden."""
        if not self.visible:
            return
        self._init_fonts()

        map_name  = getattr(g, "mapname", "")
        maps_dir  = self._maps_dir or os.path.join(os.getcwd(), "maps")
        self._ensure_geo(map_name, maps_dir)

        sw, sh = screen.get_size()
        hx = sw - self.HUD_W - self.HUD_PAD
        hy = sh - self.HUD_H - self.HUD_PAD

        # ── Background panel ──────────────────────────────────────────────────
        panel = pygame.Surface((self.HUD_W, self.HUD_H), pygame.SRCALPHA)
        panel.fill((*self.C_BG, self.OPACITY))
        pygame.draw.rect(panel, self.C_BORDER, panel.get_rect(), 1)

        # ── Title ─────────────────────────────────────────────────────────────
        title = self._title_font.render(map_name or "Map", True, self.C_TITLE)
        panel.blit(title, (self.MAP_PAD, self.MAP_PAD))
        tip = self._font.render("M: hide", True, self.C_SUB)
        panel.blit(tip, (self.HUD_W - tip.get_width() - self.MAP_PAD, self.MAP_PAD + 1))

        # ── Map draw area ─────────────────────────────────────────────────────
        MAP_TOP  = self.MAP_PAD + self.TITLE_SZ + 6
        MAP_LEFT = self.MAP_PAD
        MAP_W    = self.HUD_W - self.MAP_PAD * 2
        MAP_H    = self.HUD_H - MAP_TOP - self.MAP_PAD

        map_surf = pygame.Surface((MAP_W, MAP_H))
        map_surf.fill((13, 17, 23))

        geo   = self._geo
        maxx  = max(geo.get("maxx", 200), 1)
        maxy  = max(geo.get("maxy", 200), 1)
        sx    = MAP_W / maxx
        sy    = MAP_H / maxy

        def w2s(wx, wy):
            return int(wx * sx), int(wy * sy)

        # Draw platforms
        for plat in geo.get("platforms", []):
            px, py = w2s(plat["x1"], plat["y1"])
            pw     = max(1, int((plat["x2"] - plat["x1"]) * sx))
            ph     = max(1, int((plat["y2"] - plat["y1"]) * sy))
            is_wall = not (plat["z1"] == 0 and plat["z2"] == 0)
            col = plat["color"]
            if is_wall:
                col = (max(0,col[0]-30), max(0,col[1]-30), max(0,col[2]-30))
            pygame.draw.rect(map_surf, col, (px, py, pw, ph))

        # Draw zone outlines
        for zone in geo.get("zones", []):
            zx, zy = w2s(zone["x1"], zone["y1"])
            zw = max(1, int((zone["x2"] - zone["x1"]) * sx))
            zh = max(1, int((zone["y2"] - zone["y1"]) * sy))
            zone_surf = pygame.Surface((zw, zh), pygame.SRCALPHA)
            pygame.draw.rect(zone_surf, (88, 166, 255, 40), zone_surf.get_rect())
            map_surf.blit(zone_surf, (zx, zy))

        # Draw items
        for item in getattr(g, "items", []):
            if getattr(item, "map", "") != map_name: continue
            ix, iy = w2s(getattr(item, "x", 0), getattr(item, "y", 0))
            pygame.draw.rect(map_surf, self.C_ITEM, (ix-2, iy-2, 4, 4))

        # Draw NPCs
        for npc in getattr(g, "npcs", []):
            if getattr(npc, "map", "") != map_name: continue
            if getattr(npc, "dead", False): continue
            nx, ny = w2s(getattr(npc, "x", 0), getattr(npc, "y", 0))
            pts = [(nx, ny-self.NPC_R), (nx+self.NPC_R, ny+self.NPC_R), (nx-self.NPC_R, ny+self.NPC_R)]
            pygame.draw.polygon(map_surf, self.C_NPC, pts)

        # Draw boss
        boss_data = getattr(g, "tracked_boss", None)  # set by net packet handler
        if boss_data and boss_data.get("map") == map_name:
            bx, by = w2s(boss_data["x"], boss_data["y"])
            pulse = abs(math.sin(pygame.time.get_ticks() / 400)) * 2
            col = self.C_BOSS_P2 if boss_data.get("phase2") else self.C_BOSS_P1
            pygame.draw.circle(map_surf, col, (bx, by), int(self.BOSS_R + pulse))
            pygame.draw.line(map_surf, (255,255,255), (bx-4,by-4), (bx+4,by+4), 2)
            pygame.draw.line(map_surf, (255,255,255), (bx+4,by-4), (bx-4,by+4), 2)

        # Draw other players
        for p in getattr(g, "players", []):
            if getattr(p, "map", "") != map_name: continue
            if getattr(p, "dead", False): continue
            px2, py2 = w2s(getattr(p, "x", 0), getattr(p, "y", 0))
            col = self.C_BOT if getattr(p, "isbot", False) else self.C_PLAYER
            pygame.draw.circle(map_surf, col, (px2, py2), self.PLAYER_R)
            # Direction indicator
            facing = getattr(p, "facing", 0)
            rad = math.radians(facing - 90)
            lx = int(px2 + math.cos(rad) * (self.PLAYER_R + 3))
            ly = int(py2 + math.sin(rad) * (self.PLAYER_R + 3))
            pygame.draw.line(map_surf, col, (px2, py2), (lx, ly), 1)

        # Draw self (local player) last — always on top, bright green
        me = getattr(g, "me", None)
        if me is not None:
            mx2, my2 = w2s(getattr(me, "x", 0), getattr(me, "y", 0))
            pygame.draw.circle(map_surf, self.C_SELF, (mx2, my2), self.PLAYER_R + 1)
            facing = getattr(g, "facing", 0)
            rad = math.radians(facing - 90)
            lx = int(mx2 + math.cos(rad) * (self.PLAYER_R + 4))
            ly = int(my2 + math.sin(rad) * (self.PLAYER_R + 4))
            pygame.draw.line(map_surf, self.C_SELF, (mx2, my2), (lx, ly), 2)

        panel.blit(map_surf, (MAP_LEFT, MAP_TOP))

        # ── Legend strip along bottom ─────────────────────────────────────────
        legend_y = MAP_TOP + MAP_H + 4
        if legend_y + 14 <= self.HUD_H:
            items_legend = [
                (self.C_SELF,   "You"),
                (self.C_PLAYER, "Player"),
                (self.C_BOT,    "Bot"),
                (self.C_NPC,    "NPC"),
                (self.C_BOSS_P1,"Boss"),
                (self.C_ITEM,   "Item"),
            ]
            lx_off = self.MAP_PAD
            for col, lbl in items_legend:
                pygame.draw.circle(panel, col, (lx_off + 4, legend_y + 6), 4)
                txt = self._font.render(lbl, True, self.C_SUB)
                panel.blit(txt, (lx_off + 11, legend_y))
                lx_off += txt.get_width() + 20
                if lx_off > self.HUD_W - 20:
                    break

        screen.blit(panel, (hx, hy))


# Module-level singleton so callers just do `from ui.visual_hud import hud`
hud = VisualHUD()
