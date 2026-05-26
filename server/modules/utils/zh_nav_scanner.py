# zh_nav_scanner.py
# Passive 6-direction wall proximity scanner (Navigation Assist).
# Called from playerloop() each time the player moves to a new tile.
#
# State-change rules per direction:
#   wall appears                  -> 3D wall-material step sound at wall position
#   wall distance or type changes -> 3D new-material step sound at wall position
#   direction clears (<= range)   -> 3D bikeradar ping at scan-boundary position
#
# get_tile_at and g (network) are injected by the Bottom Binder in zhaserver.py.

SCAN_RANGE = 15        # max tiles to scan in each direction
CLEAR_SOUND = "bikeradar"  # "no obstacle" ping already used in bike.py

# Axis direction offsets: (dx, dy, dz)
DIRECTIONS = {
    "right": ( 1,  0,  0),
    "left":  (-1,  0,  0),
    "front": ( 0,  1,  0),
    "back":  ( 0, -1,  0),
    "up":    ( 0,  0,  1),
    "down":  ( 0,  0, -1),
}


def _get_wall_base(tiletype):
    """
    Strip the 'wall' prefix to get the base material for the step-sound filename.
    e.g. 'wallbrick' -> 'brick', 'wallbuilding3' -> 'building3'.
    """
    if tiletype.startswith("wall"):
        return tiletype[4:]
    return tiletype


def _scan_direction(px, py, pz, dx, dy, dz, mapname):
    """
    Cast a ray from (px, py, pz) in direction (dx, dy, dz) up to SCAN_RANGE tiles.
    Returns (tiletype, distance) of the first wall tile found, or (None, None) if clear.
    Uses the bare get_tile_at function from map.py (same as player.py / grenade.py).
    """
    for dist in range(1, SCAN_RANGE + 1):
        tx = px + dx * dist
        ty = py + dy * dist
        tz = pz + dz * dist
        tile = get_tile_at(tx, ty, tz, mapname)   # bare call - injected by Bottom Binder
        if tile and "wall" in tile:
            return tile, dist
    return None, None


def update_nav_scanner(player):
    """
    Scan all 6 directions for the given player and emit audio cues for changed directions.
    Only called when the player has moved to a new integer tile (cheap 6 ray-casts).
    All directions are evaluated independently - both sides can fire simultaneously.
    """
    if player.dead or not player.map:
        return

    px = round(player.x)
    py = round(player.y)
    pz = round(player.z)

    for direction, (dx, dy, dz) in DIRECTIONS.items():
        new_tile, new_dist = _scan_direction(px, py, pz, dx, dy, dz, player.map)

        prev_tile, prev_dist = player.nav_scan[direction]

        # Nothing changed in this direction — stay silent
        if new_tile == prev_tile and new_dist == prev_dist:
            continue

        # Persist the new state for this direction
        player.nav_scan[direction] = (new_tile, new_dist)

        if new_tile is not None:
            # Wall found (appeared, shifted distance, or changed material).
            # Emit the wall's actual tile-material step sound positioned at the
            # wall tile so the player hears it from the correct direction + distance.
            base = _get_wall_base(new_tile)
            snd = base + "step1"
            wx = px + dx * new_dist
            wy = py + dy * new_dist
            wz = pz + dz * new_dist
            g.n.send_reliable(
                player.peer_id,
                "{}.ogg {} {} {} {} 100".format(snd, wx, wy, wz, player.map),
                3
            )
        else:
            # Direction is now clear (no wall within SCAN_RANGE).
            # Emit the clear ping spatialized at the scan-boundary in that direction
            # so left-side clear sounds from the left, right-side from the right, etc.
            bx = px + dx * SCAN_RANGE
            by_ = py + dy * SCAN_RANGE
            bz = pz + dz * SCAN_RANGE
            g.n.send_reliable(
                player.peer_id,
                "{}.ogg {} {} {} {} 100".format(CLEAR_SOUND, bx, by_, bz, player.map),
                3
            )
