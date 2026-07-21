"""
mega_boss.py — The Mega Boss entity, exclusive to the megaboss map.

Phase 1 (25000 → 12500 HP):
  - Chases nearest player, melee attacks.

Phase 2 (12500 → 0 HP):
  - 3× movement speed, 2× melee damage.
  - Periodically shoots fire (spawns molotovs at player positions).
  - Periodically teleports to a random arena location.

Players who land 5+ hits receive a weapon_spawner (48-hour timed item).
"""

from timer import timer
from random import randint as random
import globals as g
from rotation import get_3d_distance
from item import spawn_item
from timeditem import new_timeditem
from molotof import spawn_molotof

# ── tuning constants ──────────────────────────────────────────────────────────
MUSIC_FILE        = "finalboss.ogg"
PITCH_MIN         = 100
PITCH_MAX         = 160

BOSS_MAP          = "megaboss"
BOSS_MAX_HEALTH   = 25000
BOSS_PHASE2_HP    = 12500

# Phase 1
P1_DAMAGE         = 25
P1_WALK_MS        = 300
P1_ATTACK_MS      = 1200

# Phase 2 — 3× speed, 2× damage
P2_DAMAGE         = 50
P2_WALK_MS        = 100
P2_ATTACK_MS      = 1200
P2_FIRE_MS_MIN    = 5000    # min ms between fire attacks
P2_FIRE_MS_MAX    = 9000    # max ms between fire attacks
P2_TELEPORT_MS_MIN = 10000  # min ms between teleports
P2_TELEPORT_MS_MAX = 18000  # max ms between teleports

BOSS_RANGE        = 4
BOSS_VOICE_MS     = 8000

HITS_FOR_REWARD   = 5
REWARD_ITEM       = "weapon_spawner"
REWARD_DURATION   = 48 * 60 * 60 * 1000   # 48 h in ms

# Arena bounds (matches megaboss.map walls at 0–200)
ARENA_MIN         = 5
ARENA_MAX         = 195


class MegaBoss:
    def __init__(self, x: int = 100, y: int = 100, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
        self.map = BOSS_MAP
        self.health = BOSS_MAX_HEALTH
        self.maxhealth = BOSS_MAX_HEALTH
        self.dying = False
        self.phase2 = False

        # hit tracking: {player_name: hit_count}
        self.hit_log: dict[str, int] = {}

        # timers
        self.walktimer    = timer()
        self.attacktimer  = timer()
        self.voicetimer   = timer()
        self.pitchtimer   = timer()
        self.firetimer    = timer()
        self.teleporttimer = timer()
        self._last_pitch  = PITCH_MIN

        # randomise first fire/teleport intervals
        self._next_fire_ms      = random(P2_FIRE_MS_MIN, P2_FIRE_MS_MAX)
        self._next_teleport_ms  = random(P2_TELEPORT_MS_MIN, P2_TELEPORT_MS_MAX)

    # ── properties ────────────────────────────────────────────────────────────

    @property
    def walk_ms(self) -> int:
        return P2_WALK_MS if self.phase2 else P1_WALK_MS

    @property
    def melee_damage(self) -> int:
        return P2_DAMAGE if self.phase2 else P1_DAMAGE

    # ── helpers ───────────────────────────────────────────────────────────────

    def register_hit(self, player_name: str) -> None:
        self.hit_log[player_name] = self.hit_log.get(player_name, 0) + 1

    def _players_on_map(self):
        return [p for p in g.players if p.map == self.map and not p.dead and not p.zombie]

    def _nearest_player(self):
        best, best_dist = None, 9999
        for p in self._players_on_map():
            d = get_3d_distance(self.x, self.y, self.z, p.x, p.y, p.z)
            if d < best_dist:
                best_dist = d
                best = p
        return best

    def _broadcast_map(self, msg: str, channel: int = 2) -> None:
        for p in self._players_on_map():
            g.n.send_reliable(p.peer_id, msg, channel)

    # ── phase 2 abilities ─────────────────────────────────────────────────────

    def _fire_attack(self, target) -> None:
        """Spawn molotovs on and around the target."""
        g.play("zombievoice" + str(random(1, 5)), self.x, self.y, self.z, self.map)
        self._broadcast_map("The Mega Boss breathes fire!", 2)
        # One molotov directly on the target, one slightly offset to keep players moving
        spawn_molotof(target.x, target.y, target.z, self.map, "mega_boss")
        offset_x = target.x + random(-10, 10)
        offset_y = target.y + random(-10, 10)
        offset_x = max(ARENA_MIN, min(ARENA_MAX, offset_x))
        offset_y = max(ARENA_MIN, min(ARENA_MAX, offset_y))
        spawn_molotof(offset_x, offset_y, target.z, self.map, "mega_boss")

    def _teleport(self) -> None:
        """Teleport to a random arena position and announce it."""
        new_x = random(ARENA_MIN + 10, ARENA_MAX - 10)
        new_y = random(ARENA_MIN + 10, ARENA_MAX - 10)
        g.play("misc177", self.x, self.y, self.z, self.map)   # vanish sound
        self.x = new_x
        self.y = new_y
        g.play("misc177", self.x, self.y, self.z, self.map)   # appear sound
        self._broadcast_map(
            f"The Mega Boss teleported to {new_x}, {new_y}!", 2
        )

    # ── death ─────────────────────────────────────────────────────────────────

    def _die(self) -> None:
        self.dying = True

        g.play("voice17", self.x, self.y, self.z, self.map)
        g.n.broadcast("play_s important.ogg", 0)
        g.n.broadcast(
            "The Mega Boss has been defeated! "
            "Heroes who struck it hard will find a reward in their inventory.",
            2
        )
        g.n.broadcast("boss_dead", 0)

        spawn_item(self.x, self.y, self.z, self.map, "revival_nectar", 5)
        spawn_item(self.x, self.y, self.z, self.map, "vitality_potion", 10)

        for pname, hits in self.hit_log.items():
            if hits >= HITS_FOR_REWARD:
                idx = g.get_player_index_from(pname)
                if idx > -1:
                    g.players[idx].give(REWARD_ITEM, 1)
                    new_timeditem(pname, REWARD_ITEM, REWARD_DURATION)
                    try:
                        g.n.send_reliable(
                            g.players[idx].peer_id,
                            f"You receive a {REWARD_ITEM} for helping defeat the Mega Boss! "
                            f"It lasts 48 hours and can be used any number of times.",
                            2
                        )
                    except Exception:
                        pass
                else:
                    from timeditem import offlinegive
                    offlinegive(pname, REWARD_ITEM, 1)
                    new_timeditem(pname, REWARD_ITEM, REWARD_DURATION)

        # Reset music pitch
        for p in g.players:
            if p.map == self.map:
                try:
                    g.n.send_reliable(p.peer_id, f"amb_pitch {MUSIC_FILE} {PITCH_MIN}", 0)
                except Exception:
                    pass

        g.mega_boss = None
        g.mega_boss_alive = False

    # ── main loop ─────────────────────────────────────────────────────────────

    def loop(self) -> None:
        if self.dying:
            return
        if self.health <= 0:
            self._die()
            return

        # ── Phase 2 transition ────────────────────────────────────────────────
        if not self.phase2 and self.health <= BOSS_PHASE2_HP:
            self.phase2 = True
            g.play("voice17", self.x, self.y, self.z, self.map)
            g.n.broadcast("play_s important.ogg", 0)
            g.n.broadcast(
                "WARNING! The Mega Boss has entered Phase 2! "
                "It is now 3× faster, hits twice as hard, and can breathe fire and teleport!",
                2
            )
            # Reset timers so abilities fire soon after transition
            self.firetimer.restart()
            self.teleporttimer.restart()
            self._next_fire_ms     = random(P2_FIRE_MS_MIN, P2_FIRE_MS_MAX)
            self._next_teleport_ms = random(P2_TELEPORT_MS_MIN, P2_TELEPORT_MS_MAX)

        # ── Music pitch + minimap position broadcast ──────────────────────────
        if self.pitchtimer.elapsed >= 2000:
            self.pitchtimer.restart()
            hp_frac = 1.0 - (self.health / self.maxhealth)
            hp_frac = max(0.0, min(1.0, hp_frac))
            new_pitch = int(PITCH_MIN + (PITCH_MAX - PITCH_MIN) * hp_frac)
            p2_flag = "1" if self.phase2 else "0"
            for p in self._players_on_map():
                if new_pitch != self._last_pitch:
                    g.n.send_reliable(p.peer_id, f"amb_pitch {MUSIC_FILE} {new_pitch}", 0)
                g.n.send_reliable(p.peer_id, f"boss_pos {self.x} {self.y} {p2_flag}", 0)
            if new_pitch != self._last_pitch:
                self._last_pitch = new_pitch

        # ── Periodic roar ─────────────────────────────────────────────────────
        if self.voicetimer.elapsed >= BOSS_VOICE_MS:
            self.voicetimer.restart()
            g.play("zombievoice" + str(random(1, 5)), self.x, self.y, self.z, self.map)

        target = self._nearest_player()
        if target is None:
            return

        # ── Phase 2 abilities ─────────────────────────────────────────────────
        if self.phase2:
            if self.firetimer.elapsed >= self._next_fire_ms:
                self.firetimer.restart()
                self._next_fire_ms = random(P2_FIRE_MS_MIN, P2_FIRE_MS_MAX)
                self._fire_attack(target)

            if self.teleporttimer.elapsed >= self._next_teleport_ms:
                self.teleporttimer.restart()
                self._next_teleport_ms = random(P2_TELEPORT_MS_MIN, P2_TELEPORT_MS_MAX)
                self._teleport()

        # ── Movement ──────────────────────────────────────────────────────────
        if self.walktimer.elapsed >= self.walk_ms:
            self.walktimer.restart()
            if self.x < target.x:
                self.x += 1
            elif self.x > target.x:
                self.x -= 1
            if self.y < target.y:
                self.y += 1
            elif self.y > target.y:
                self.y -= 1
            tile = g.get_tile_at(self.x, self.y, self.z, self.map)
            g.play(tile + "step" + str(random(1, 5)), self.x, self.y, self.z, self.map, pitch=80)

        # ── Melee attack ──────────────────────────────────────────────────────
        if self.attacktimer.elapsed >= P1_ATTACK_MS:
            dist = get_3d_distance(self.x, self.y, self.z, target.x, target.y, target.z)
            if dist <= BOSS_RANGE:
                self.attacktimer.restart()
                target.health -= self.melee_damage
                target.hitby = "mega_boss"
                target.play_hit_sound()
                g.play("zombiehit", self.x, self.y, self.z, self.map)
                g.n.broadcast(
                    "distsound doorhitdist "
                    + str(self.x) + " " + str(self.y) + " " + str(self.z)
                    + " " + self.map, 0
                )


# ── public API ────────────────────────────────────────────────────────────────

def spawn_mega_boss(x: int = 100, y: int = 100, z: int = 0) -> bool:
    """Spawn the boss. Returns False if one is already alive."""
    if getattr(g, "mega_boss_alive", False):
        return False
    g.mega_boss = MegaBoss(x, y, z)
    g.mega_boss_alive = True
    g.n.broadcast("play_s important.ogg", 0)
    g.n.broadcast(
        "ALERT! A Mega Boss has appeared in the Mega Boss Arena! "
        "Travel to the megaboss map and defeat it — "
        "hit it 5 or more times to earn a weapon_spawner!",
        2
    )
    return True


def register_boss_hit(player_name: str) -> None:
    boss = getattr(g, "mega_boss", None)
    if boss is not None and not boss.dying:
        boss.register_hit(player_name)


def megabossloop() -> None:
    boss = getattr(g, "mega_boss", None)
    if boss is not None:
        boss.loop()
