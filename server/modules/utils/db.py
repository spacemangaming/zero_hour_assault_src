"""
db.py — SQLite persistence layer for Zero Hour Assault player accounts.

Replaces the flat-file chars/<name>/<field>.usr system with a single
zha_players.db SQLite database stored in the server/ directory.

Public API (mirrors the old file-based helpers):
    init_db(db_path)            — call once at server startup
    player_exists(name)         — True if player row exists
    player_exists_icase(name)   — case-insensitive existence check
    create_player_row(name)     — insert a blank row
    delete_player_row(name)     — remove a player row
    charwrite(name, field, val) — write text/int/real value
    charwriteb(name, field, b)  — write raw bytes (BLOB)
    charread(name, field, default="") -> str
    charreadb(name, field) -> bytes
    charexists(name, field) -> bool
    chardelete(name, field)     — set field to NULL / remove from extras
    get_all_players() -> list[dict]   — all player rows as dicts
    get_player(name) -> dict | None
"""

import sqlite3
import os
import json
import threading
import base64
import traceback

# ── module-level state ────────────────────────────────────────────────────────

_DB_PATH: str | None = None
_local = threading.local()   # per-thread connections

# ── column type registry ──────────────────────────────────────────────────────
# Every field that gets its own column. Anything not listed here goes into
# the JSON `extra` catch-all column.

_INT_COLS = frozenset({
    'x', 'y', 'z', 'facing', 'health',
    'scorepoint', 'playerkills', 'playerdeaths', 'botkills', 'botdeaths',
    'headhits', 'headshots', 'leghits', 'legshots',
    'zhtoken', 'paid', 'paidtime', 'eventpoint', 'currenteventpoint',
    'chesttoken', 'developer', 'hidden', 'authreq', 'permaban',
    'adrenalinetime', 'jammertime', 'helitimer', 'helijumptimer',
    'spatializertimer', 'backpacks_level', 'freedomhelicopter',
    'freedomhelicoptertimer', 'parachuted', 'maldied', 'lasthp2',
    'ticketmail', 'matchinvite', 'eventalerts', 'mapsound', 'tokentransfer',
    'istyping', 'chestpickupnotify', 'votenotify',
    'friendonlinemessage', 'friendmessage', 'voicemessage', 'voicemessage2',
    'matchmessage', 'teammessage', 'groupmessage', 'mapmessage', 'pmmessage',
    'groupinvitation', 'communityinvitation', 'communitymessage',
    'flag', 'corpse_bomb', 'beacon', 'blockvoice3',
    'shieldhitchance', 'helmethitchance', 'lasthelmethitchance',
    'last_admin_login_ticket_count',
})

_REAL_COLS = frozenset({'paidmonths'})

_BLOB_COLS = frozenset({
    'inventory', 'storeinventory', 'ammo', 'current_char', 'bought_chars',
    'friendlist', 'pendingfriendlist', 'blocks', 'silenced', 'tokenplayers',
    'task_data', 'banned', 'banenddate', 'backpacktimer',
    'groupinvitations', 'communityinvitations',
})

_TEXT_COLS = frozenset({
    'pass', 'mail', 'compid', 'authorized_compids', 'createdate',
    'map', 'gender', 'weapon', 'weapon2', 'spatialized_by',
    'lang', 'langchan', 'motorhistory', 'status', 'banreason',
    'lastactive', 'matchteam', 'joinedmatch', 'matchmode', 'scorerank',
    'jailreason', 'spatialized_by',
})

_ALL_KNOWN_COLS = _INT_COLS | _REAL_COLS | _BLOB_COLS | _TEXT_COLS

# ── schema ────────────────────────────────────────────────────────────────────

_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS server_state (
    key         TEXT PRIMARY KEY,
    data        BLOB,
    text_val    TEXT,
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS players (
    name                        TEXT PRIMARY KEY,
    -- auth & identity
    pass                        TEXT DEFAULT '',
    mail                        TEXT DEFAULT '',
    compid                      TEXT DEFAULT '',
    authorized_compids          TEXT DEFAULT '',
    authreq                     INTEGER DEFAULT 0,
    createdate                  TEXT DEFAULT '',
    gender                      TEXT DEFAULT 'male',
    -- position
    x                           INTEGER DEFAULT 5,
    y                           INTEGER DEFAULT 0,
    z                           INTEGER DEFAULT 0,
    map                         TEXT DEFAULT 'lobby',
    facing                      INTEGER DEFAULT 0,
    -- health / combat stats
    health                      INTEGER DEFAULT 100,
    scorepoint                  INTEGER DEFAULT 0,
    scorerank                   TEXT DEFAULT 'Bronze',
    playerkills                 INTEGER DEFAULT 0,
    playerdeaths                INTEGER DEFAULT 0,
    botkills                    INTEGER DEFAULT 0,
    botdeaths                   INTEGER DEFAULT 0,
    headhits                    INTEGER DEFAULT 0,
    headshots                   INTEGER DEFAULT 0,
    leghits                     INTEGER DEFAULT 0,
    legshots                    INTEGER DEFAULT 0,
    maldied                     INTEGER DEFAULT 0,
    lasthp2                     INTEGER DEFAULT 0,
    -- economy
    zhtoken                     INTEGER DEFAULT 0,
    paid                        INTEGER DEFAULT 0,
    paidtime                    INTEGER DEFAULT 0,
    paidmonths                  REAL    DEFAULT 0,
    eventpoint                  INTEGER DEFAULT 0,
    currenteventpoint           INTEGER DEFAULT 0,
    chesttoken                  INTEGER DEFAULT 0,
    -- weapons / inventory (binary)
    weapon                      TEXT DEFAULT 'punch',
    weapon2                     TEXT DEFAULT 'feet',
    inventory                   BLOB,
    storeinventory              BLOB,
    ammo                        BLOB,
    current_char                BLOB,
    bought_chars                BLOB,
    -- privileges
    developer                   INTEGER DEFAULT 0,
    hidden                      INTEGER DEFAULT 0,
    permaban                    INTEGER DEFAULT 0,
    banreason                   TEXT DEFAULT '',
    banenddate                  BLOB,
    banned                      BLOB,
    -- social (binary)
    friendlist                  BLOB,
    pendingfriendlist           BLOB,
    blocks                      BLOB,
    silenced                    BLOB,
    groupinvitations            BLOB,
    communityinvitations        BLOB,
    tokenplayers                BLOB,
    task_data                   BLOB,
    -- timer / equipment state
    adrenalinetime              INTEGER DEFAULT 0,
    jammertime                  INTEGER DEFAULT 0,
    helitimer                   INTEGER DEFAULT 0,
    helijumptimer               INTEGER DEFAULT 0,
    spatializertimer            INTEGER DEFAULT 0,
    spatialized_by              TEXT DEFAULT '',
    backpacks_level             INTEGER DEFAULT 0,
    backpacktimer               BLOB,
    freedomhelicopter           INTEGER DEFAULT 0,
    freedomhelicoptertimer      INTEGER DEFAULT 0,
    parachuted                  INTEGER DEFAULT 0,
    -- notification prefs
    ticketmail                  INTEGER DEFAULT 1,
    matchinvite                 INTEGER DEFAULT 1,
    eventalerts                 INTEGER DEFAULT 1,
    mapsound                    INTEGER DEFAULT 1,
    tokentransfer               INTEGER DEFAULT 1,
    istyping                    INTEGER DEFAULT 1,
    chestpickupnotify           INTEGER DEFAULT 1,
    votenotify                  INTEGER DEFAULT 1,
    friendonlinemessage         INTEGER DEFAULT 1,
    friendmessage               INTEGER DEFAULT 1,
    voicemessage                INTEGER DEFAULT 1,
    voicemessage2               INTEGER DEFAULT 1,
    matchmessage                INTEGER DEFAULT 1,
    teammessage                 INTEGER DEFAULT 1,
    groupmessage                INTEGER DEFAULT 1,
    mapmessage                  INTEGER DEFAULT 1,
    pmmessage                   INTEGER DEFAULT 1,
    groupinvitation             INTEGER DEFAULT 1,
    communityinvitation         INTEGER DEFAULT 1,
    communitymessage            INTEGER DEFAULT 1,
    -- match state
    matchteam                   TEXT DEFAULT '',
    joinedmatch                 TEXT DEFAULT '',
    matchmode                   TEXT DEFAULT '',
    flag                        INTEGER DEFAULT 0,
    -- misc
    corpse_bomb                 INTEGER DEFAULT 0,
    beacon                      INTEGER DEFAULT 0,
    blockvoice3                 INTEGER DEFAULT 0,
    shieldhitchance             INTEGER DEFAULT 0,
    helmethitchance             INTEGER DEFAULT 0,
    lasthelmethitchance         INTEGER DEFAULT 0,
    last_admin_login_ticket_count INTEGER DEFAULT 0,
    lastactive                  TEXT DEFAULT '',
    motorhistory                TEXT DEFAULT '',
    status                      TEXT DEFAULT '',
    lang                        TEXT DEFAULT '',
    langchan                    TEXT DEFAULT '',
    jailreason                  TEXT DEFAULT '',
    -- catch-all for any ad-hoc fields
    extra                       TEXT DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_players_name_lower ON players (LOWER(name));
CREATE INDEX IF NOT EXISTS idx_players_compid     ON players (compid);
CREATE INDEX IF NOT EXISTS idx_players_mail       ON players (mail);
"""

# ── internal helpers ──────────────────────────────────────────────────────────

def _conn() -> sqlite3.Connection:
    """Return a per-thread SQLite connection, creating it if needed."""
    if not hasattr(_local, 'conn') or _local.conn is None:
        if _DB_PATH is None:
            raise RuntimeError("db.init_db() has not been called yet")
        c = sqlite3.connect(_DB_PATH, check_same_thread=False, timeout=30)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA synchronous=NORMAL")
        c.execute("PRAGMA foreign_keys=ON")
        _local.conn = c
    return _local.conn


def _execute(sql: str, params=()) -> sqlite3.Cursor:
    c = _conn()
    cur = c.execute(sql, params)
    c.commit()
    return cur


def _fetchone(sql: str, params=()) -> sqlite3.Row | None:
    return _conn().execute(sql, params).fetchone()


def _fetchall(sql: str, params=()) -> list:
    return _conn().execute(sql, params).fetchall()


def _get_extra(name: str, field: str):
    """Read a value from the JSON extra column."""
    row = _fetchone("SELECT extra FROM players WHERE name=?", (name,))
    if row is None:
        return None
    try:
        d = json.loads(row[0] or '{}')
        return d.get(field)
    except Exception:
        return None


def _set_extra(name: str, field: str, value) -> None:
    """Write a value into the JSON extra column."""
    row = _fetchone("SELECT extra FROM players WHERE name=?", (name,))
    if row is None:
        return
    try:
        d = json.loads(row[0] or '{}')
    except Exception:
        d = {}
    if value is None:
        d.pop(field, None)
    else:
        d[field] = value
    _execute("UPDATE players SET extra=? WHERE name=?", (json.dumps(d), name))


def _del_extra(name: str, field: str) -> None:
    _set_extra(name, field, None)

# ── public API ────────────────────────────────────────────────────────────────

def init_db(db_path: str) -> None:
    """Initialise (or open) the SQLite database. Call once at server startup."""
    global _DB_PATH
    _DB_PATH = db_path
    c = _conn()
    c.executescript(_CREATE_SQL)
    c.commit()
    print(f"[db] SQLite player database ready: {db_path}")


def player_exists(name: str) -> bool:
    row = _fetchone("SELECT 1 FROM players WHERE name=?", (name,))
    return row is not None


def player_exists_icase(name: str) -> bool:
    """Case-insensitive existence check (replaces directory_exists2)."""
    row = _fetchone("SELECT 1 FROM players WHERE LOWER(name)=LOWER(?)", (name,))
    return row is not None


def create_player_row(name: str) -> None:
    """Insert a blank player row if it doesn't already exist."""
    _execute(
        "INSERT OR IGNORE INTO players (name, extra) VALUES (?, '{}')",
        (name,)
    )


def delete_player_row(name: str) -> None:
    _execute("DELETE FROM players WHERE name=?", (name,))


def charwrite(name: str, field: str, value) -> None:
    """Write a text/int/real value for a player field."""
    if field in _ALL_KNOWN_COLS:
        try:
            _execute(f'UPDATE players SET "{field}"=? WHERE name=?', (value, name))
        except Exception:
            traceback.print_exc()
    else:
        _set_extra(name, field, value)


def charwriteb(name: str, field: str, data: bytes) -> None:
    """Write raw bytes for a player field (BLOB)."""
    if field in _BLOB_COLS:
        try:
            _execute(f'UPDATE players SET "{field}"=? WHERE name=?', (data, name))
        except Exception:
            traceback.print_exc()
    else:
        # Store binary data in extra as base64
        encoded = base64.b64encode(data).decode('ascii')
        _set_extra(name, field, {'__blob__': encoded})


def charread(name: str, field: str, default: str = "") -> str:
    """Read a player field as a string."""
    if field in _ALL_KNOWN_COLS:
        try:
            row = _fetchone(f'SELECT "{field}" FROM players WHERE name=?', (name,))
            if row is None or row[0] is None:
                return default
            return str(row[0])
        except Exception:
            return default
    else:
        val = _get_extra(name, field)
        if val is None:
            return default
        if isinstance(val, dict) and '__blob__' in val:
            return default   # binary stored here, not text
        return str(val)


def charreadb(name: str, field: str) -> bytes:
    """Read a player field as raw bytes."""
    if field in _BLOB_COLS:
        try:
            row = _fetchone(f'SELECT "{field}" FROM players WHERE name=?', (name,))
            if row is None or row[0] is None:
                return b""
            return bytes(row[0])
        except Exception:
            return b""
    else:
        val = _get_extra(name, field)
        if isinstance(val, dict) and '__blob__' in val:
            try:
                return base64.b64decode(val['__blob__'])
            except Exception:
                return b""
        return b""


def charexists(name: str, field: str) -> bool:
    """Return True if a player field has been set (not NULL / not missing)."""
    if field in _ALL_KNOWN_COLS:
        try:
            row = _fetchone(f'SELECT "{field}" FROM players WHERE name=?', (name,))
            if row is None:
                return False
            return row[0] is not None
        except Exception:
            return False
    else:
        return _get_extra(name, field) is not None


def chardelete(name: str, field: str) -> None:
    """Clear a player field (set to NULL, or remove from extras)."""
    if field in _ALL_KNOWN_COLS:
        try:
            _execute(f'UPDATE players SET "{field}"=NULL WHERE name=?', (name,))
        except Exception:
            traceback.print_exc()
    else:
        _del_extra(name, field)


def get_player(name: str) -> dict | None:
    """Return all stored fields for a player as a plain dict, or None."""
    row = _fetchone("SELECT * FROM players WHERE name=?", (name,))
    if row is None:
        return None
    return dict(row)


def get_all_players() -> list[dict]:
    """Return every player row as a list of dicts (for dashboard / admin use)."""
    rows = _fetchall("SELECT * FROM players ORDER BY LOWER(name)")
    return [dict(r) for r in rows]


def get_players_matching(query: str) -> list[dict]:
    """Case-insensitive substring search on player name."""
    rows = _fetchall(
        "SELECT * FROM players WHERE LOWER(name) LIKE LOWER(?) ORDER BY LOWER(name)",
        (f"%{query}%",)
    )
    return [dict(r) for r in rows]


def count_players() -> int:
    row = _fetchone("SELECT COUNT(*) FROM players")
    return row[0] if row else 0


def get_banned_players() -> list[dict]:
    """Return all players with permaban=1 or a non-empty banreason."""
    rows = _fetchall(
        "SELECT * FROM players WHERE permaban=1 OR (banreason IS NOT NULL AND banreason != '') ORDER BY LOWER(name)"
    )
    return [dict(r) for r in rows]


# ── server-state API ──────────────────────────────────────────────────────────
# Stores arbitrary game-world data (formerly .dat / .txt / .svr files) in
# the server_state table.  Key = original filename, e.g. "groups.dat".

def sv_write(key: str, data: bytes) -> None:
    """Store raw bytes (pickle blob) under key."""
    _execute(
        "INSERT INTO server_state(key,data,updated_at) VALUES(?,?,datetime('now'))"
        " ON CONFLICT(key) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at",
        (key, data)
    )


def sv_read(key: str) -> bytes:
    """Return raw bytes stored under key, or b'' if missing."""
    row = _fetchone("SELECT data FROM server_state WHERE key=?", (key,))
    if row is None or row[0] is None:
        return b""
    return bytes(row[0])


def sv_write_text(key: str, text: str) -> None:
    """Store a text value under key."""
    _execute(
        "INSERT INTO server_state(key,text_val,updated_at) VALUES(?,?,datetime('now'))"
        " ON CONFLICT(key) DO UPDATE SET text_val=excluded.text_val, updated_at=excluded.updated_at",
        (key, text)
    )


def sv_read_text(key: str, default: str = "") -> str:
    """Return the text value stored under key, or default if missing."""
    row = _fetchone("SELECT text_val FROM server_state WHERE key=?", (key,))
    if row is None or row[0] is None:
        return default
    return str(row[0])


def sv_exists(key: str) -> bool:
    """Return True if the key exists in server_state."""
    row = _fetchone("SELECT 1 FROM server_state WHERE key=?", (key,))
    return row is not None


def sv_delete(key: str) -> None:
    """Remove a key from server_state."""
    _execute("DELETE FROM server_state WHERE key=?", (key,))
