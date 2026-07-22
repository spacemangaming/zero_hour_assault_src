"""
dashboard/app.py — Flask admin panel for Zero Hour Assault.

Runs as a background thread inside the server process.
Access at http://localhost:8080 (port configurable via server.conf: dashboard_port).
Password configurable via server.conf: dashboard_password.

Pages:
  /                 — overview: player count, online list, server uptime
  /players          — all players table + search
  /player/<name>    — detail: stats, kick, ban, unban
  /bans             — banned players list + unban
  /weapons          — weapons JSON editor
  /characters       — character JSON editor
  /logs/chat        — last N lines of chats.log
  /logs/error       — last N lines of logs/server_errors.log (if present)
  /config           — view/edit server.conf keys (non-sensitive)
"""

from __future__ import annotations
import os
import sys
import json
import threading
import functools
import traceback
from datetime import datetime

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, flash, jsonify
)

# ── locate server root (two dirs up from this file) ──────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
SERVER_ROOT = os.path.abspath(os.path.join(_HERE, ".."))

app = Flask(__name__)
app.secret_key = os.urandom(32)   # regenerated each restart — sessions are ephemeral

# ── runtime globals (set by start_dashboard before Flask starts) ──────────────
_dashboard_password: str = "admin"
_dashboard_port: int = 8080
_dashboard_api_key: str = ""
_motd_file: str = ""
_g = None          # globals module reference (set at start)
_db = None         # db module reference
_data_loader = None

# ── auth helpers ──────────────────────────────────────────────────────────────

def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def api_key_required(f):
    """Decorator for bot-facing API endpoints — authenticates via X-API-Key header."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not _dashboard_api_key:
            return jsonify({"error": "Bot API not configured"}), 403
        key = request.headers.get("X-API-Key", "")
        if key != _dashboard_api_key:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

# ── CSS / base template ───────────────────────────────────────────────────────

BASE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ZHA Admin — {{ title }}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #0f1117; color: #c9d1d9; min-height: 100vh; }
    a { color: #58a6ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    nav { background: #161b22; border-bottom: 1px solid #30363d; padding: 0.6rem 1.5rem;
          display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap; }
    nav strong { color: #e6edf3; font-size: 1.1rem; margin-right: 0.5rem; }
    nav a { font-size: 0.9rem; }
    .content { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }
    h1 { font-size: 1.5rem; color: #e6edf3; margin-bottom: 1.2rem; }
    h2 { font-size: 1.15rem; color: #e6edf3; margin: 1.5rem 0 0.6rem; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px;
            padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
    .stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem; }
    .stat { background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
            padding: 1rem; text-align: center; }
    .stat .num { font-size: 2rem; font-weight: 700; color: #58a6ff; }
    .stat .lbl { font-size: 0.75rem; color: #8b949e; margin-top: 0.2rem; }
    table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
    th, td { padding: 0.55rem 0.8rem; border-bottom: 1px solid #21262d; text-align: left; }
    th { background: #0d1117; color: #8b949e; font-weight: 600; }
    tr:hover td { background: #1c2128; }
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 20px;
             font-size: 0.75rem; font-weight: 600; }
    .badge-green { background: #1f4423; color: #3fb950; }
    .badge-red   { background: #4c1825; color: #f85149; }
    .badge-gray  { background: #21262d; color: #8b949e; }
    input, textarea, select { background: #0d1117; color: #c9d1d9; border: 1px solid #30363d;
                               border-radius: 6px; padding: 0.45rem 0.7rem; font-size: 0.875rem; }
    input[type=text], input[type=password], input[type=search], input[type=number] { width: 100%; }
    textarea { width: 100%; font-family: monospace; }
    .btn { display: inline-block; padding: 0.45rem 1rem; border-radius: 6px; border: none;
           cursor: pointer; font-size: 0.875rem; font-weight: 600; }
    .btn-primary { background: #238636; color: #fff; }
    .btn-primary:hover { background: #2ea043; }
    .btn-danger  { background: #b62324; color: #fff; }
    .btn-danger:hover  { background: #da3633; }
    .btn-secondary { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; }
    .btn-secondary:hover { background: #30363d; }
    .btn-warn { background: #9a6700; color: #fff; }
    .btn-warn:hover { background: #bb8009; }
    .alert { padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.875rem; }
    .alert-success { background: #1f4423; border: 1px solid #3fb950; color: #3fb950; }
    .alert-error   { background: #4c1825; border: 1px solid #f85149; color: #f85149; }
    .search-bar { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
    .search-bar input { flex: 1; }
    pre { font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; word-break: break-all;
          background: #0d1117; border: 1px solid #21262d; border-radius: 6px;
          padding: 1rem; max-height: 60vh; overflow-y: auto; }
    .form-row { display: flex; flex-direction: column; gap: 0.3rem; margin-bottom: 0.8rem; }
    .form-row label { font-size: 0.8rem; color: #8b949e; }
  </style>
</head>
<body>
  <nav>
    <strong>⚡ ZHA Admin</strong>
    <a href="/">Dashboard</a>
    <a href="/players">Players</a>
    <a href="/bans">Bans</a>
    <a href="/data">Game Data</a>
    <a href="/sounds">Sounds</a>
    <a href="/live">Live Map</a>
    <a href="/logs/chat">Chat Log</a>
    <a href="/logs/error">Error Log</a>
    <a href="/logs/admin">Admin Log</a>
    <a href="/config">Config</a>
    <a href="/logout" style="margin-left:auto;color:#8b949e;">Logout</a>
  </nav>
  <div class="content">
    {% for cat, msg in get_flashed_messages(with_categories=True) %}
      <div class="alert alert-{{ 'success' if cat == 'success' else 'error' }}">{{ msg }}</div>
    {% endfor %}
    {% block body %}{% endblock %}
  </div>
</body>
</html>
"""

LOGIN_PAGE = BASE.replace("{% block body %}{% endblock %}", """
{% block body %}
<div style="max-width:360px;margin:4rem auto;">
  <div class="card">
    <h1 style="margin-bottom:1.2rem;">ZHA Admin Login</h1>
    <form method="post">
      <div class="form-row">
        <label>Password</label>
        <input type="password" name="password" autofocus required>
      </div>
      <button class="btn btn-primary" style="width:100%;margin-top:0.5rem;">Log in</button>
    </form>
  </div>
</div>
{% endblock %}
""")


# ── helpers ───────────────────────────────────────────────────────────────────

def _online_players():
    """Return list of online player objects (skipping None slots)."""
    if _g is None:
        return []
    return [p for p in getattr(_g, "players", []) if p is not None and getattr(p, "name", "")]


def _tail(path: str, n: int = 300) -> str:
    if not os.path.exists(path):
        return f"(file not found: {path})"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        return "".join(lines[-n:])
    except Exception as ex:
        return f"(error reading file: {ex})"


def _json_path(filename: str) -> str:
    return os.path.join(SERVER_ROOT, "data", filename)


def _read_json(filename: str) -> tuple[dict | list, str]:
    path = _json_path(filename)
    if not os.path.exists(path):
        # try one level up (server/filename)
        path = os.path.join(SERVER_ROOT, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), path
    except Exception as ex:
        return {}, str(ex)


def _write_json(path: str, data) -> str | None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return None
    except Exception as ex:
        return str(ex)


def _kick_player(name: str) -> bool:
    """Kick a player from the server (thread-safe best-effort)."""
    if _g is None:
        return False
    for i, p in enumerate(_g.players):
        if p is not None and getattr(p, "name", "") == name:
            try:
                _g.remove_from_server(i, True)
            except Exception:
                pass
            return True
    return False


def _find_server_conf() -> str:
    return os.path.join(SERVER_ROOT, "server.conf")


def _read_conf() -> dict:
    path = _find_server_conf()
    result = {}
    if not os.path.exists(path):
        return result
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                result[k.strip()] = v.strip()
    return result


def _write_conf(data: dict) -> None:
    path = _find_server_conf()
    lines = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    # update existing keys in-place, append new ones
    written = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith(";") or not stripped:
            new_lines.append(line)
            continue
        if "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k in data:
                new_lines.append(f"{k} = {data[k]}\n")
                written.add(k)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    for k, v in data.items():
        if k not in written:
            new_lines.append(f"{k} = {v}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


# ── routes ─────────────────────────────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == _dashboard_password:
            session["logged_in"] = True
            return redirect(url_for("index"))
        flash("Wrong password.", "error")
    return render_template_string(LOGIN_PAGE, title="Login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    online = _online_players()
    total = _db.count_players() if _db else 0
    banned = len(_db.get_banned_players()) if _db else 0

    rows = ""
    for p in online:
        name = getattr(p, "name", "?")
        map_ = getattr(p, "map", "?")
        hp   = getattr(p, "health", "?")
        rows += f"""
        <tr>
          <td><a href="/player/{name}">{name}</a></td>
          <td>{map_}</td>
          <td>{hp}</td>
          <td>
            <form method="post" action="/kick/{name}" style="display:inline">
              <button class="btn btn-warn" onclick="return confirm('Kick {name}?')">Kick</button>
            </form>
          </td>
        </tr>"""

    import globals as _g
    boss_alive = getattr(_g, "mega_boss_alive", False)
    boss_hp = ""
    if boss_alive:
        _b = getattr(_g, "mega_boss", None)
        if _b:
            boss_hp = f"{max(0, _b.health):,} / {_b.maxhealth:,} HP"

    boss_card = f"""
    <div class="card" style="border-color:{'#da3633' if boss_alive else '#30363d'};margin-bottom:1rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <h2 style="margin:0;color:{'#ff7b72' if boss_alive else '#f0f6fc'}">
            {"🔴 Mega Boss — ACTIVE" if boss_alive else "Mega Boss"}
          </h2>
          {f'<p style="color:#ff7b72;margin:0.3rem 0 0">{boss_hp}</p>' if boss_alive else
           '<p style="color:#8b949e;margin:0.3rem 0 0">No boss is currently active.</p>'}
        </div>
        <form method="post" action="/boss/spawn">
          <button class="btn {'btn-warn' if boss_alive else 'btn-primary'}"
                  {'onclick="return confirm(\'A boss is already alive. Spawn another anyway?\')"' if boss_alive else ''}>
            {'Spawn Another Boss' if boss_alive else 'Spawn Mega Boss'}
          </button>
        </form>
      </div>
    </div>"""

    body = f"""
    <h1>Dashboard</h1>
    <div class="stat-grid" style="margin-bottom:1.5rem;">
      <div class="stat"><div class="num">{len(online)}</div><div class="lbl">Online</div></div>
      <div class="stat"><div class="num">{total}</div><div class="lbl">Total players</div></div>
      <div class="stat"><div class="num">{banned}</div><div class="lbl">Banned</div></div>
    </div>
    {boss_card}
    <div class="card">
      <h2 style="margin-top:0">Online players</h2>
      {"<p style='color:#8b949e;margin-top:0.5rem'>No players online.</p>" if not online else f'''
      <table>
        <thead><tr><th>Name</th><th>Map</th><th>HP</th><th>Actions</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>'''}
    </div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Dashboard")


@app.route("/boss/spawn", methods=["POST"])
@login_required
def boss_spawn():
    try:
        from mega_boss import spawn_mega_boss
        result = spawn_mega_boss(100, 100, 0)
        if result:
            flash("Mega Boss spawned! Server announcement sent.", "success")
        else:
            flash("A Mega Boss is already alive.", "error")
    except Exception as ex:
        flash(f"Failed to spawn boss: {ex}", "error")
    return redirect(url_for("index"))


@app.route("/kick/<name>", methods=["POST"])
@login_required
def kick(name):
    if _kick_player(name):
        flash(f"Kicked {name}.", "success")
    else:
        flash(f"{name} is not online.", "error")
    return redirect(request.referrer or url_for("index"))


@app.route("/players")
@login_required
def players():
    q = request.args.get("q", "").strip()
    if q and _db:
        all_players = _db.get_players_matching(q)
    elif _db:
        all_players = _db.get_all_players()
    else:
        all_players = []
    online_names = {getattr(p, "name", "") for p in _online_players()}

    rows = ""
    for p in all_players:
        name = p.get("name", "")
        online_badge = '<span class="badge badge-green">Online</span>' if name in online_names else '<span class="badge badge-gray">Offline</span>'
        banned_badge = '<span class="badge badge-red">Banned</span>' if p.get("permaban") or p.get("banreason") else ""
        rows += f"""
        <tr>
          <td><a href="/player/{name}">{name}</a></td>
          <td>{online_badge} {banned_badge}</td>
          <td>{p.get('scorepoint', 0)}</td>
          <td>{p.get('map', '')}</td>
          <td>{p.get('createdate', '')}</td>
        </tr>"""

    body = f"""
    <h1>Players ({len(all_players)})</h1>
    <div class="card">
      <form class="search-bar" method="get">
        <input type="search" name="q" value="{q}" placeholder="Search by name…">
        <button class="btn btn-primary">Search</button>
        {"<a class='btn btn-secondary' href='/players'>Clear</a>" if q else ""}
      </form>
      <table>
        <thead><tr><th>Name</th><th>Status</th><th>Score</th><th>Map</th><th>Created</th></tr></thead>
        <tbody>{rows if rows else "<tr><td colspan='5' style='color:#8b949e'>No players found.</td></tr>"}</tbody>
      </table>
    </div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Players")


@app.route("/player/<name>")
@login_required
def player_detail(name):
    if not _db:
        flash("Database not available.", "error")
        return redirect(url_for("players"))
    p = _db.get_player(name)
    if p is None:
        flash(f"Player '{name}' not found.", "error")
        return redirect(url_for("players"))

    online = any(getattr(op, "name", "") == name for op in _online_players())
    banned = bool(p.get("permaban") or p.get("banreason"))

    status_badge = '<span class="badge badge-green">Online</span>' if online else '<span class="badge badge-gray">Offline</span>'
    ban_badge = '<span class="badge badge-red">Banned</span>' if banned else ""

    # stat rows — skip binary blobs and internal extras
    SKIP = {"pass", "inventory", "storeinventory", "ammo", "current_char",
            "bought_chars", "friendlist", "pendingfriendlist", "blocks",
            "silenced", "tokenplayers", "task_data", "banned", "banenddate",
            "backpacktimer", "groupinvitations", "communityinvitations", "extra"}
    stat_rows = ""
    for k, v in sorted(p.items()):
        if k in SKIP or (isinstance(v, (bytes, bytearray)) and len(v) > 20):
            continue
        val_str = str(v)[:120] if v is not None else "<em style='color:#8b949e'>null</em>"
        stat_rows += f"<tr><td style='color:#8b949e'>{k}</td><td>{val_str}</td></tr>"

    body = f"""
    <h1>{name} {status_badge} {ban_badge}</h1>
    <div style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-bottom:1rem;">
      {"" if not online else f'''
      <form method="post" action="/kick/{name}">
        <button class="btn btn-warn" onclick="return confirm('Kick {name}?')">Kick</button>
      </form>
      '''}
      {"" if banned else f'''
      <a class="btn btn-danger" href="/ban/{name}">Ban…</a>
      '''}
      {"" if not banned else f'''
      <form method="post" action="/unban/{name}">
        <button class="btn btn-secondary" onclick="return confirm('Unban {name}?')">Unban</button>
      </form>
      '''}
      <a class="btn btn-secondary" href="/players">← Back</a>
    </div>
    <div class="card">
      <table>
        <thead><tr><th>Field</th><th>Value</th></tr></thead>
        <tbody>{stat_rows}</tbody>
      </table>
    </div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title=f"Player — {name}")


@app.route("/ban/<name>", methods=["GET", "POST"])
@login_required
def ban_player(name):
    if request.method == "POST":
        reason = request.form.get("reason", "No reason given")
        permaban = request.form.get("permaban") == "1"
        duration = request.form.get("duration_hours", "0")
        try:
            hours = int(duration)
        except ValueError:
            hours = 0

        if _db:
            _db.charwrite(name, "banreason", reason)
            _db.charwrite(name, "permaban", 1 if permaban else 0)
            if not permaban and hours > 0:
                import pickle, datetime as dt
                end = dt.datetime.now() + dt.timedelta(hours=hours)
                _db.charwriteb(name, "banenddate", pickle.dumps(end))

        # add to compbans
        if _g:
            compid = _db.charread(name, "compid", "") if _db else ""
            if compid:
                _g.compbans[name] = compid
                try:
                    from compban import save_bans
                    save_bans()
                except Exception:
                    pass
        _kick_player(name)
        flash(f"Banned {name}. Reason: {reason}", "success")
        return redirect(url_for("player_detail", name=name))

    body = f"""
    <h1>Ban player: {name}</h1>
    <div class="card">
      <form method="post">
        <div class="form-row">
          <label>Reason</label>
          <input type="text" name="reason" placeholder="Reason for ban" required>
        </div>
        <div class="form-row">
          <label>Duration (hours, 0 = permanent)</label>
          <input type="number" name="duration_hours" value="0" min="0">
        </div>
        <div class="form-row">
          <label style="display:flex;align-items:center;gap:0.4rem;">
            <input type="checkbox" name="permaban" value="1" style="width:auto"> Permanent ban
          </label>
        </div>
        <button class="btn btn-danger">Apply ban</button>
        <a class="btn btn-secondary" href="/player/{name}" style="margin-left:0.5rem;">Cancel</a>
      </form>
    </div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title=f"Ban — {name}")


@app.route("/unban/<name>", methods=["POST"])
@login_required
def unban_player(name):
    if _db:
        try:
            from compban import comp_unban
            comp_unban(name)
        except Exception:
            _db.charwrite(name, "banreason", "")
            _db.chardelete(name, "banenddate")
            _db.charwrite(name, "permaban", 0)
    flash(f"Unbanned {name}.", "success")
    return redirect(url_for("player_detail", name=name))


@app.route("/bans")
@login_required
def bans():
    banned = _db.get_banned_players() if _db else []
    rows = ""
    for p in banned:
        name = p.get("name", "")
        reason = p.get("banreason") or "—"
        perma = "Yes" if p.get("permaban") else "No"
        rows += f"""
        <tr>
          <td><a href="/player/{name}">{name}</a></td>
          <td>{reason}</td>
          <td>{perma}</td>
          <td>
            <form method="post" action="/unban/{name}" style="display:inline">
              <button class="btn btn-secondary btn-sm" onclick="return confirm('Unban {name}?')">Unban</button>
            </form>
          </td>
        </tr>"""
    body = f"""
    <h1>Banned Players ({len(banned)})</h1>
    <div class="card">
      <table>
        <thead><tr><th>Name</th><th>Reason</th><th>Permanent</th><th>Actions</th></tr></thead>
        <tbody>{rows if rows else "<tr><td colspan='4' style='color:#8b949e'>No banned players.</td></tr>"}</tbody>
      </table>
    </div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Bans")


# ── Game Data CRUD ────────────────────────────────────────────────────────────

_DATA_ROOT = os.path.join(SERVER_ROOT, "data")

# Field schemas for per-file directories.
# Each field: (key, label, input_type, default)
# input_type: "int" | "float" | "str" | "bool" | "nullable_int" | "nullable_str"
_WEAPON_FIELDS = [
    ("bullet",         "Fires bullets",      "bool",         True),
    ("fire_interval",  "Fire interval (ms)", "int",          300),
    ("auto",           "Automatic",          "bool",         False),
    ("range",          "Range",              "int",          50),
    ("min_damage",     "Min damage",         "int",          10),
    ("max_damage",     "Max damage",         "int",          20),
    ("spread",         "Spread",             "int",          5),
    ("mag_size",       "Mag size",           "nullable_int", None),
    ("ammo_type",      "Ammo type",          "nullable_str", None),
    ("reload_time",    "Reload time (ms)",   "nullable_int", None),
    ("npc_priority",   "NPC priority",       "int",          50),
    ("bulletfall_min", "Bullet fall min",    "nullable_int", None),
    ("bulletfall_max", "Bullet fall max",    "nullable_int", None),
    ("thrown",         "Thrown",             "nullable_str", None),
]

_CHARACTER_FIELDS = [
    ("walk_time",     "Walk time",      "int",  235),
    ("max_walk_time", "Max walk time",  "int",  145),
    ("health",        "Health",         "int",  150),
    ("plus_damage",   "Bonus damage",   "int",  0),
    ("jump_time",     "Jump time",      "int",  90),
    ("purchasable",   "Purchasable",    "bool", True),
]

_SCHEMAS = {
    "weapons":    _WEAPON_FIELDS,
    "characters": _CHARACTER_FIELDS,
}


def _safe_data_path(subdir: str, filename: str = "") -> str | None:
    """Return abs path if safe, else None."""
    base = os.path.normpath(_DATA_ROOT)
    candidate = os.path.normpath(os.path.join(_DATA_ROOT, subdir, filename))
    return candidate if candidate.startswith(base) else None


def _hot_reload():
    if _data_loader:
        try:
            getattr(_data_loader, "reload_all", lambda: None)()
        except Exception as ex:
            flash(f"Reload warning: {ex}", "error")


def _coerce_field(value: str, ftype: str):
    """Coerce a form string value to the correct Python type."""
    if ftype == "bool":
        return value.lower() in ("1", "true", "yes", "on")
    if ftype == "int":
        return int(value) if value.strip() else 0
    if ftype == "float":
        return float(value) if value.strip() else 0.0
    if ftype == "nullable_int":
        return int(value) if value.strip() else None
    if ftype == "nullable_str":
        return value.strip() or None
    return value  # str


def _render_field(key: str, label: str, ftype: str, value, is_new: bool = False):
    """Render a single form row for a field."""
    vid = f"f_{key}"
    if ftype == "bool":
        checked = "checked" if value else ""
        return (f'<div class="form-row"><label for="{vid}">{label}</label>'
                f'<input type="checkbox" id="{vid}" name="{key}" value="1" {checked}'
                f' style="width:auto;margin-top:0.3rem;"></div>')
    placeholder = "" if value is None else ""
    val_str = "" if value is None else str(value)
    input_type = "number" if ftype in ("int", "float", "nullable_int") else "text"
    return (f'<div class="form-row"><label for="{vid}">{label}'
            f'{"" if ftype not in ("nullable_int","nullable_str") else " (optional)"}</label>'
            f'<input type="{input_type}" id="{vid}" name="{key}" value="{val_str}" '
            f'placeholder="{placeholder}"></div>')


def _item_form(schema, data: dict, action: str, submit_label: str,
               name_val: str = "", name_locked: bool = False) -> str:
    """Render a complete add/edit form for a per-file item."""
    name_input = (
        f'<div class="form-row"><label>Name (filename)</label>'
        f'<input type="text" name="_name" value="{name_val}" '
        f'{"readonly" if name_locked else "required"} placeholder="e.g. ak47"></div>'
    )
    fields_html = "".join(_render_field(k, lbl, ft, data.get(k, dflt))
                          for k, lbl, ft, dflt in schema)
    return (f'<form method="post" action="{action}">'
            f'{name_input}{fields_html}'
            f'<div style="margin-top:1rem;display:flex;gap:0.5rem;">'
            f'<button class="btn btn-primary">{submit_label}</button>'
            f'<a href="/data" class="btn btn-secondary">Cancel</a>'
            f'</div></form>')


# ── /data index ───────────────────────────────────────────────────────────────

@app.route("/data")
@login_required
def data_index():
    sections = ""

    # ── Weapons ──────────────────────────────────────────────────────────────
    wpn_dir = os.path.join(_DATA_ROOT, "weapons")
    if os.path.isdir(wpn_dir):
        rows = ""
        for fname in sorted(os.listdir(wpn_dir)):
            if not fname.endswith(".json"):
                continue
            wname = fname[:-5]
            try:
                w = json.load(open(os.path.join(wpn_dir, fname), encoding="utf-8"))
            except Exception:
                w = {}
            dmg = f"{w.get('min_damage','?')}–{w.get('max_damage','?')}"
            fi = w.get("fire_interval", "?")
            rng = w.get("range", "?")
            auto = "✓" if w.get("auto") else ""
            rows += (f'<tr><td style="font-family:monospace">{wname}</td>'
                     f'<td>{dmg}</td><td>{fi}</td><td>{rng}</td><td>{auto}</td>'
                     f'<td><a href="/data/weapons/{wname}/edit" class="btn btn-secondary" style="font-size:0.78rem;padding:0.25rem 0.6rem;">Edit</a> '
                     f'<form method="post" action="/data/weapons/{wname}/delete" style="display:inline">'
                     f'<button class="btn btn-danger" style="font-size:0.78rem;padding:0.25rem 0.6rem;" '
                     f'onclick="return confirm(\'Delete {wname}?\')">Del</button></form></td></tr>')
        sections += f"""
        <div class="card" id="weapons">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
            <h2 style="margin:0">Weapons</h2>
            <a href="/data/weapons/new" class="btn btn-primary" style="font-size:0.85rem;">+ Add Weapon</a>
          </div>
          <table><thead><tr><th>Name</th><th>Damage</th><th>Fire (ms)</th><th>Range</th><th>Auto</th><th>Actions</th></tr></thead>
          <tbody>{rows or "<tr><td colspan='6' style='color:#8b949e'>No weapons.</td></tr>"}</tbody></table>
        </div>"""

    # ── Characters ───────────────────────────────────────────────────────────
    char_dir = os.path.join(_DATA_ROOT, "characters")
    if os.path.isdir(char_dir):
        rows = ""
        for fname in sorted(os.listdir(char_dir)):
            if not fname.endswith(".json"):
                continue
            cname = fname[:-5]
            try:
                c = json.load(open(os.path.join(char_dir, fname), encoding="utf-8"))
            except Exception:
                c = {}
            hp = c.get("health", "?")
            pd = c.get("plus_damage", "?")
            wt = c.get("walk_time", "?")
            pur = "✓" if c.get("purchasable") else ""
            rows += (f'<tr><td style="font-family:monospace">{cname}</td>'
                     f'<td>{hp}</td><td>{pd}</td><td>{wt}</td><td>{pur}</td>'
                     f'<td><a href="/data/characters/{cname}/edit" class="btn btn-secondary" style="font-size:0.78rem;padding:0.25rem 0.6rem;">Edit</a> '
                     f'<form method="post" action="/data/characters/{cname}/delete" style="display:inline">'
                     f'<button class="btn btn-danger" style="font-size:0.78rem;padding:0.25rem 0.6rem;" '
                     f'onclick="return confirm(\'Delete {cname}?\')">Del</button></form></td></tr>')
        sections += f"""
        <div class="card" id="characters">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
            <h2 style="margin:0">Characters</h2>
            <a href="/data/characters/new" class="btn btn-primary" style="font-size:0.85rem;">+ Add Character</a>
          </div>
          <table><thead><tr><th>Name</th><th>HP</th><th>+Dmg</th><th>Walk time</th><th>Buyable</th><th>Actions</th></tr></thead>
          <tbody>{rows or "<tr><td colspan='6' style='color:#8b949e'>No characters.</td></tr>"}</tbody></table>
        </div>"""

    # ── Ranks ─────────────────────────────────────────────────────────────────
    ranks_path = os.path.join(_DATA_ROOT, "ranks", "ranks.json")
    if os.path.exists(ranks_path):
        sections += f"""
        <div class="card" id="ranks">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
            <h2 style="margin:0">Ranks</h2>
            <a href="/data/ranks/edit" class="btn btn-secondary" style="font-size:0.85rem;">Edit Ranks</a>
          </div>
          <p style="color:#8b949e;font-size:0.85rem;">Score thresholds → rank names.</p>
        </div>"""

    # ── Other single-file sections ────────────────────────────────────────────
    others = [
        ("items/loot_table.json",       "Loot Table",        "loot"),
        ("chest/chest_items.json",      "Chest Items",       "chest"),
        ("economy/token_packs.json",    "Token Packs",       "token_packs"),
        ("items/inventory_limits.json", "Inventory Limits",  "inv_limits"),
        ("items/sounds.json",           "Item Sounds",       "sounds"),
        ("match_modes.json",            "Match Modes",       "match_modes"),
    ]
    for rel, label, anchor in others:
        p = os.path.join(_DATA_ROOT, rel)
        if os.path.exists(p):
            sections += f"""
            <div class="card" id="{anchor}">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <h2 style="margin:0">{label}</h2>
                <a href="/data/file/{rel}" class="btn btn-secondary" style="font-size:0.85rem;">Edit</a>
              </div>
            </div>"""

    body = f"<h1>Game Data</h1>{sections or '<p style=\"color:#8b949e\">No data directory found.</p>'}"
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Game Data")


# ── Per-file CRUD (weapons, characters) ───────────────────────────────────────

@app.route("/data/<subdir>/new", methods=["GET", "POST"])
@login_required
def data_item_new(subdir):
    schema = _SCHEMAS.get(subdir)
    if not schema:
        flash(f"No schema for {subdir}.", "error")
        return redirect(url_for("data_index"))

    if request.method == "POST":
        name = request.form.get("_name", "").strip()
        if not name:
            flash("Name is required.", "error")
        else:
            path = _safe_data_path(subdir, name + ".json")
            if not path:
                flash("Invalid name.", "error")
            elif os.path.exists(path):
                flash(f"{name} already exists — edit it instead.", "error")
            else:
                obj = {k: _coerce_field(request.form.get(k, ""), ft)
                       for k, _, ft, _ in schema}
                err = _write_json(path, obj)
                if err:
                    flash(f"Save failed: {err}", "error")
                else:
                    _hot_reload()
                    flash(f"Created {name}.", "success")
                    return redirect(url_for("data_index") + f"#{subdir}")

    label = subdir.rstrip("s").capitalize()
    defaults = {k: dflt for k, _, _, dflt in schema}
    form = _item_form(schema, defaults, f"/data/{subdir}/new",
                      f"Create {label}", name_val="", name_locked=False)
    body = f"""
    <div style="margin-bottom:0.8rem;">
      <a href="/data#{subdir}" class="btn btn-secondary">← Back</a>
    </div>
    <h1>New {label}</h1>
    <div class="card">{form}</div>"""
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body),
                                  title=f"New {label}")


@app.route("/data/<subdir>/<name>/edit", methods=["GET", "POST"])
@login_required
def data_item_edit(subdir, name):
    schema = _SCHEMAS.get(subdir)
    if not schema:
        flash(f"No schema for {subdir}.", "error")
        return redirect(url_for("data_index"))

    path = _safe_data_path(subdir, name + ".json")
    if not path or not os.path.exists(path):
        flash(f"{name} not found.", "error")
        return redirect(url_for("data_index"))

    with open(path, encoding="utf-8") as f:
        obj = json.load(f)

    if request.method == "POST":
        for k, _, ft, _ in schema:
            obj[k] = _coerce_field(request.form.get(k, ""), ft)
        err = _write_json(path, obj)
        if err:
            flash(f"Save failed: {err}", "error")
        else:
            _hot_reload()
            flash(f"Saved {name}.", "success")
            return redirect(url_for("data_index") + f"#{subdir}")

    label = subdir.rstrip("s").capitalize()
    form = _item_form(schema, obj, f"/data/{subdir}/{name}/edit",
                      f"Save {name}", name_val=name, name_locked=True)
    body = f"""
    <div style="margin-bottom:0.8rem;">
      <a href="/data#{subdir}" class="btn btn-secondary">← Back</a>
    </div>
    <h1>Edit {label}: {name}</h1>
    <div class="card">{form}</div>"""
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body),
                                  title=f"Edit {name}")


@app.route("/data/<subdir>/<name>/delete", methods=["POST"])
@login_required
def data_item_delete(subdir, name):
    schema = _SCHEMAS.get(subdir)
    if not schema:
        flash("Delete not supported for this type.", "error")
        return redirect(url_for("data_index"))
    path = _safe_data_path(subdir, name + ".json")
    if path and os.path.exists(path):
        try:
            os.remove(path)
            _hot_reload()
            flash(f"Deleted {name}.", "success")
        except Exception as ex:
            flash(f"Delete failed: {ex}", "error")
    else:
        flash(f"{name} not found.", "error")
    return redirect(url_for("data_index") + f"#{subdir}")


# ── Ranks editor (array of {score, name}) ─────────────────────────────────────

@app.route("/data/ranks/edit", methods=["GET", "POST"])
@login_required
def ranks_editor():
    path = os.path.join(_DATA_ROOT, "ranks", "ranks.json")
    if request.method == "POST":
        scores = request.form.getlist("score")
        names  = request.form.getlist("rname")
        ranks = sorted(
            [{"score": int(s), "name": n.strip()}
             for s, n in zip(scores, names) if s.strip() and n.strip()],
            key=lambda r: r["score"]
        )
        err = _write_json(path, ranks)
        if err:
            flash(f"Save failed: {err}", "error")
        else:
            _hot_reload()
            flash("Ranks saved.", "success")
            return redirect(url_for("ranks_editor"))

    try:
        ranks = json.load(open(path, encoding="utf-8"))
    except Exception:
        ranks = []

    rows = ""
    for r in ranks:
        rows += (f'<tr>'
                 f'<td><input type="number" name="score" value="{r["score"]}" style="width:100px"></td>'
                 f'<td><input type="text" name="rname" value="{r["name"]}" style="width:200px"></td>'
                 f'</tr>')
    # blank add row
    rows += ('<tr><td><input type="number" name="score" value="" placeholder="score" style="width:100px"></td>'
             '<td><input type="text" name="rname" value="" placeholder="New rank name" style="width:200px"></td></tr>')

    body = f"""
    <div style="margin-bottom:0.8rem;"><a href="/data#ranks" class="btn btn-secondary">← Back</a></div>
    <h1>Edit Ranks</h1>
    <div class="card">
      <form method="post">
        <table>
          <thead><tr><th>Score threshold</th><th>Rank name</th></tr></thead>
          <tbody id="rank-rows">{rows}</tbody>
        </table>
        <div style="margin-top:0.8rem;display:flex;gap:0.5rem;">
          <button class="btn btn-primary">Save</button>
          <button type="button" class="btn btn-secondary" onclick="addRankRow()">+ Add row</button>
        </div>
      </form>
    </div>
    <script>
    function addRankRow(){{
      var tb=document.getElementById("rank-rows");
      var tr=document.createElement("tr");
      tr.innerHTML='<td><input type="number" name="score" value="" placeholder="score" style="width:100px"></td>'
                  +'<td><input type="text" name="rname" value="" placeholder="Rank name" style="width:200px"></td>';
      tb.appendChild(tr);
    }}
    </script>"""
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Ranks")


# ── Generic JSON file editor (for single-file configs) ───────────────────────

@app.route("/data/file/<path:rel_path>", methods=["GET", "POST"])
@login_required
def data_file_editor(rel_path):
    abs_path = os.path.normpath(os.path.join(_DATA_ROOT, rel_path))
    if not abs_path.startswith(os.path.normpath(_DATA_ROOT)):
        flash("Invalid path.", "error")
        return redirect(url_for("data_index"))

    content = ""
    if request.method == "POST":
        raw = request.form.get("json_content", "")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as ex:
            flash(f"Invalid JSON: {ex}", "error")
            content = raw
        else:
            err = _write_json(abs_path, parsed)
            if err:
                flash(f"Save failed: {err}", "error")
                content = raw
            else:
                _hot_reload()
                flash("Saved.", "success")
                content = json.dumps(parsed, indent=2, ensure_ascii=False)

    if not content:
        if not os.path.exists(abs_path):
            flash("File not found.", "error")
            return redirect(url_for("data_index"))
        try:
            data = json.load(open(abs_path, encoding="utf-8"))
            content = json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as ex:
            flash(f"Read error: {ex}", "error")
            return redirect(url_for("data_index"))

    fname = os.path.basename(rel_path)
    nrows = min(max(len(content.splitlines()) + 2, 15), 60)
    body = f"""
    <div style="margin-bottom:0.8rem;"><a href="/data" class="btn btn-secondary">← Back</a></div>
    <h1>{fname}</h1>
    <div class="card">
      <p style="color:#8b949e;font-size:0.8rem;margin-bottom:0.8rem;font-family:monospace">data/{rel_path}</p>
      <form method="post">
        <textarea name="json_content" rows="{nrows}"
                  style="font-family:monospace;font-size:0.82rem;">{content}</textarea>
        <div style="margin-top:0.8rem;">
          <button class="btn btn-primary">Save &amp; Reload</button>
        </div>
      </form>
    </div>"""
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title=fname)


# backwards-compat redirects for old nav links
@app.route("/weapons")
@login_required
def weapons_editor():
    return redirect(url_for("data_index") + "#weapons")


@app.route("/characters")
@login_required
def characters_editor():
    return redirect(url_for("data_index") + "#characters")


def _tail_db(key: str, n: int = 300) -> str:
    """Read a log stored in the DB's server_state table, return last n lines."""
    if _db is None:
        return "(DB not available)"
    try:
        text = _db.sv_read_text(key, "")
        if not text:
            return f"(no log data for '{key}')"
        lines = text.splitlines()
        return "\n".join(lines[-n:])
    except Exception as ex:
        return f"(error reading log: {ex})"


@app.route("/logs/chat")
@login_required
def log_chat():
    content = _tail_db("chats.log")
    body = f"""
    <h1>Chat Log (last 300 lines)</h1>
    <div class="card"><pre>{content}</pre></div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Chat Log")


@app.route("/logs/error")
@login_required
def log_error():
    content = _tail_db("error.log") or _tail_db("errors.log")
    body = f"""
    <h1>Error Log (last 300 lines)</h1>
    <div class="card"><pre>{content}</pre></div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Error Log")


@app.route("/logs/admin")
@login_required
def log_admin():
    content = _tail_db("adminlog.txt")
    body = f"""
    <h1>Admin Log (last 300 lines)</h1>
    <div class="card"><pre>{content}</pre></div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Admin Log")


@app.route("/config", methods=["GET", "POST"])
@login_required
def config():
    # Keys we allow editing via the web UI (omit passwords shown in plain text in the browser is fine here
    # since this whole page is already auth-gated, but we omit internal keys)
    EDITABLE = {"port", "dashboard_port", "dashboard_password", "server_name", "max_players"}
    conf = _read_conf()

    if request.method == "POST":
        updates = {}
        for k in EDITABLE:
            v = request.form.get(k, "").strip()
            if v:
                updates[k] = v
        _write_conf(updates)
        flash("server.conf updated. Restart server for port/password changes to take effect.", "success")
        conf = _read_conf()

    rows = ""
    for k, v in sorted(conf.items()):
        editable = k in EDITABLE
        cell = f'<input type="text" name="{k}" value="{v}">' if editable else f'<span style="color:#8b949e">{v}</span>'
        rows += f"<tr><td>{k}</td><td>{cell}</td></tr>"

    body = f"""
    <h1>Server Config</h1>
    <div class="card">
      <form method="post">
        <table>
          <thead><tr><th>Key</th><th>Value</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <div style="margin-top:1rem;">
          <button class="btn btn-primary">Save editable fields</button>
        </div>
      </form>
    </div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Config")


# ── Sound browser ─────────────────────────────────────────────────────────────

_SOUNDS_DIR = os.path.abspath(os.path.join(SERVER_ROOT, "..", "sounds"))
_WEAPON_SOUND_SLOTS = ["fire_sound", "reload_sound", "draw_sound", "empty_sound", "dist_sound"]


def _all_sounds() -> list[str]:
    """Return sorted list of all .ogg basenames (without extension) in sounds/."""
    if not os.path.isdir(_SOUNDS_DIR):
        return []
    return sorted(f[:-4] for f in os.listdir(_SOUNDS_DIR) if f.endswith(".ogg"))


def _sounds_for_weapon(wname: str, all_sounds: list[str]) -> dict[str, list[str]]:
    """Return grouped sound matches: fire variants, reload, draw, empty, dist."""
    groups = {s: [] for s in ["fire", "reload", "draw", "empty", "dist"]}
    prefix = wname.lower()
    for s in all_sounds:
        sl = s.lower()
        for slot in groups:
            if sl.startswith(prefix + slot):
                groups[slot].append(s)
    return groups


@app.route("/sounds", methods=["GET", "POST"])
@login_required
def sounds():
    all_snds = _all_sounds()
    sounds_json_path = os.path.join(_DATA_ROOT, "items", "sounds.json")
    weapons_dir = os.path.join(_DATA_ROOT, "weapons")

    # ── handle POST: item sounds save ──────────────────────────────────────────
    if request.method == "POST" and request.form.get("form_type") == "item_sounds":
        new_map = {}
        for k, v in request.form.items():
            if k.startswith("snd_") and v.strip():
                item = k[4:]
                new_map[item] = v.strip()
        err = _write_json(sounds_json_path, new_map)
        if err:
            flash(f"Save failed: {err}", "error")
        else:
            flash("Item sounds saved.", "success")
            if _data_loader:
                try: getattr(_data_loader, "reload_all", lambda: None)()
                except Exception as ex: flash(f"Reload warning: {ex}", "error")

    # ── handle POST: weapon sound override save ─────────────────────────────────
    if request.method == "POST" and request.form.get("form_type") == "weapon_sounds":
        wname = request.form.get("weapon_name", "")
        wpath = os.path.normpath(os.path.join(weapons_dir, wname + ".json"))
        if os.path.exists(wpath) and wpath.startswith(os.path.normpath(weapons_dir)):
            with open(wpath, "r", encoding="utf-8") as f:
                wdata = json.load(f)
            for slot in _WEAPON_SOUND_SLOTS:
                val = request.form.get(slot, "").strip()
                if val:
                    wdata[slot] = val
                else:
                    wdata.pop(slot, None)
            err = _write_json(wpath, wdata)
            if err:
                flash(f"Save failed: {err}", "error")
            else:
                flash(f"Saved sounds for {wname}.", "success")
                if _data_loader:
                    try: getattr(_data_loader, "reload_all", lambda: None)()
                    except Exception as ex: flash(f"Reload warning: {ex}", "error")

    # ── read current item sounds ────────────────────────────────────────────────
    item_sounds = {}
    if os.path.exists(sounds_json_path):
        try:
            with open(sounds_json_path, "r", encoding="utf-8") as f:
                item_sounds = json.load(f)
        except Exception:
            pass

    # ── read weapon list + their current sound overrides ───────────────────────
    weapons_data = {}
    if os.path.isdir(weapons_dir):
        for fname in sorted(os.listdir(weapons_dir)):
            if fname.endswith(".json"):
                wname = fname[:-5]
                try:
                    with open(os.path.join(weapons_dir, fname), "r", encoding="utf-8") as f:
                        weapons_data[wname] = json.load(f)
                except Exception:
                    weapons_data[wname] = {}

    # ── build sound options datalist ───────────────────────────────────────────
    datalist_opts = "\n".join(f'<option value="{s}">' for s in all_snds)

    # ── item sounds section ────────────────────────────────────────────────────
    item_rows = ""
    for item, snd in sorted(item_sounds.items()):
        item_rows += f"""
        <tr>
          <td style="font-family:monospace">{item}</td>
          <td>
            <input list="all-sounds" name="snd_{item}" value="{snd}"
                   style="width:280px" placeholder="sound name (no .ogg)">
          </td>
        </tr>"""

    # ── weapon sounds section ──────────────────────────────────────────────────
    weapon_cards = ""
    slot_labels = {
        "fire_sound": "Fire (base, 3 variants auto-appended)",
        "reload_sound": "Reload",
        "draw_sound": "Draw",
        "empty_sound": "Empty (no ammo)",
        "dist_sound": "Distance (base, 3 variants auto-appended)",
    }
    for wname, wdata in weapons_data.items():
        conventional = _sounds_for_weapon(wname, all_snds)
        slot_inputs = ""
        for slot, label in slot_labels.items():
            current = wdata.get(slot, "")
            conv_examples = ", ".join(conventional.get(slot.replace("_sound",""), [])[:3])
            hint = f'conventional: {conv_examples}' if conv_examples else "no conventional sounds found"
            slot_inputs += f"""
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
              <label style="width:240px;font-size:0.8rem;color:#8b949e;">{label}</label>
              <input list="all-sounds" name="{slot}" value="{current}"
                     style="width:260px;font-size:0.82rem;" placeholder="{hint}">
            </div>"""
        weapon_cards += f"""
        <details style="margin-bottom:0.5rem;">
          <summary style="cursor:pointer;padding:0.5rem 0.7rem;background:#0d1117;
                          border:1px solid #30363d;border-radius:6px;
                          font-family:monospace;font-size:0.9rem;">{wname}</summary>
          <div style="padding:0.8rem;border:1px solid #30363d;border-top:none;border-radius:0 0 6px 6px;">
            <form method="post">
              <input type="hidden" name="form_type" value="weapon_sounds">
              <input type="hidden" name="weapon_name" value="{wname}">
              {slot_inputs}
              <button class="btn btn-primary" style="margin-top:0.5rem;font-size:0.8rem;">
                Save {wname} sounds</button>
              <span style="color:#8b949e;font-size:0.75rem;margin-left:0.8rem;">
                Leave blank to use convention ({wname}fire1/2/3, etc.)</span>
            </form>
          </div>
        </details>"""

    body = f"""
    <datalist id="all-sounds">{datalist_opts}</datalist>
    <h1>Sound Browser &amp; Assignment</h1>
    <p style="color:#8b949e;margin-bottom:1.5rem;font-size:0.875rem;">
      {len(all_snds)} sounds available in sounds/ &mdash;
      type in any field below and use the dropdown to autocomplete.
      Leave weapon fields blank to keep the default naming convention.
    </p>

    <h2>Item Pickup Sounds</h2>
    <div class="card">
      <form method="post">
        <input type="hidden" name="form_type" value="item_sounds">
        <table>
          <thead><tr><th>Item</th><th>Pickup sound (no .ogg)</th></tr></thead>
          <tbody>{item_rows}</tbody>
        </table>
        <div style="margin-top:1rem;">
          <button class="btn btn-primary">Save item sounds</button>
        </div>
      </form>
    </div>

    <h2>Weapon Sound Overrides</h2>
    <p style="color:#8b949e;font-size:0.8rem;margin-bottom:0.8rem;">
      Click a weapon to expand. Set overrides only when you want a different
      sound than the naming convention ({'{weapon}fire1/2/3'}, {'{weapon}reload'}, etc.).
    </p>
    <div class="card">{weapon_cards}</div>
    """
    return render_template_string(BASE.replace("{% block body %}{% endblock %}", body), title="Sounds")


# ── JSON API endpoints (for quick AJAX-style tooling) ────────────────────────

@app.route("/api/online")
@login_required
def api_online():
    return jsonify([
        {"name": getattr(p, "name", ""), "map": getattr(p, "map", ""), "health": getattr(p, "health", 0)}
        for p in _online_players()
    ])


@app.route("/api/maps")
@login_required
def api_maps():
    try:
        import sys, os
        sys.path.insert(0, os.path.join(SERVER_ROOT, "modules", "utils"))
        from map_renderer import all_map_names
        return jsonify(all_map_names())
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route("/api/map-geometry/<map_name>")
@login_required
def api_map_geometry(map_name: str):
    """Return static map geometry (platforms, zones). Cached — parse once per map."""
    try:
        import sys, os
        sys.path.insert(0, os.path.join(SERVER_ROOT, "modules", "utils"))
        from map_renderer import parse_map
        data = parse_map(map_name)
        return jsonify(data)
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route("/api/map-state/<map_name>")
@login_required
def api_map_state(map_name: str):
    """Return live entity state for a map: players, boss, NPCs, items, weapons."""
    import globals as _g_live
    state: dict = {"players": [], "boss": None, "npcs": [], "items": [], "weapons": []}

    # Players
    for p in getattr(_g_live, "players", []):
        if p is None: continue
        if getattr(p, "map", "") != map_name: continue
        state["players"].append({
            "name":   getattr(p, "name", "?"),
            "x":      getattr(p, "x", 0),
            "y":      getattr(p, "y", 0),
            "z":      getattr(p, "z", 0),
            "health": getattr(p, "health", 0),
            "maxhp":  getattr(p, "maxhealth", 150),
            "dead":   getattr(p, "dead", False),
            "isbot":  getattr(p, "isbot", False),
            "facing": getattr(p, "facing", 0),
        })

    # Mega boss
    _boss = getattr(_g_live, "mega_boss", None)
    if _boss is not None and not _boss.dying and _boss.map == map_name:
        state["boss"] = {
            "x":      _boss.x,
            "y":      _boss.y,
            "z":      _boss.z,
            "health": max(0, _boss.health),
            "maxhp":  _boss.maxhealth,
            "phase2": _boss.phase2,
        }

    # NPCs
    for npc in getattr(_g_live, "npcs", []):
        if getattr(npc, "map", "") != map_name: continue
        if getattr(npc, "fulldied", False): continue
        state["npcs"].append({
            "name": getattr(npc, "soundname", "npc"),
            "x":    getattr(npc, "x", 0),
            "y":    getattr(npc, "y", 0),
            "z":    getattr(npc, "z", 0),
            "hp":   getattr(npc, "health", 0),
        })

    # Items on ground
    for item in getattr(_g_live, "items", []):
        if getattr(item, "map", "") != map_name: continue
        state["items"].append({
            "name": getattr(item, "name", "item"),
            "x":    getattr(item, "x", 0),
            "y":    getattr(item, "y", 0),
        })

    # Active bullets/weapons
    for w in getattr(_g_live, "weapons", []):
        if getattr(w, "map", "") != map_name: continue
        state["weapons"].append({
            "x": getattr(w, "x", 0),
            "y": getattr(w, "y", 0),
            "z": getattr(w, "z", 0),
        })

    return jsonify(state)


# ── Live Map page ─────────────────────────────────────────────────────────────

_LIVE_MAP_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ZHA Live Map</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0f1117; color: #c9d1d9; font-family: system-ui, sans-serif;
           display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
    header { background: #161b22; border-bottom: 1px solid #30363d;
             padding: 0.5rem 1rem; display: flex; align-items: center; gap: 1rem; flex-shrink: 0; }
    header strong { color: #e6edf3; }
    header a { color: #58a6ff; font-size: 0.85rem; }
    select, button { background: #21262d; color: #c9d1d9; border: 1px solid #30363d;
                     border-radius: 6px; padding: 0.35rem 0.7rem; font-size: 0.85rem; cursor: pointer; }
    button:hover { background: #30363d; }
    #wrap { flex: 1; display: flex; overflow: hidden; }
    #sidebar { width: 220px; flex-shrink: 0; background: #161b22; border-right: 1px solid #30363d;
               overflow-y: auto; padding: 0.75rem; font-size: 0.8rem; }
    #sidebar h3 { color: #8b949e; font-size: 0.7rem; text-transform: uppercase;
                  letter-spacing: 0.08em; margin: 0.75rem 0 0.3rem; }
    #sidebar h3:first-child { margin-top: 0; }
    .sentry { padding: 0.25rem 0; border-bottom: 1px solid #21262d; }
    .sentry .nm { color: #e6edf3; font-weight: 600; }
    .sentry .dt { color: #8b949e; font-size: 0.75rem; }
    .hpbar { height: 4px; background: #21262d; border-radius: 2px; margin-top: 3px; }
    .hpfill { height: 100%; border-radius: 2px; transition: width 0.4s; }
    #canvas-wrap { flex: 1; position: relative; overflow: hidden; display: flex;
                   align-items: center; justify-content: center; }
    canvas { display: block; cursor: crosshair; }
    #coords { position: absolute; bottom: 8px; right: 10px; font-size: 0.75rem; color: #8b949e; }
    #legend { position: absolute; top: 8px; right: 10px; background: rgba(22,27,34,0.9);
              border: 1px solid #30363d; border-radius: 6px; padding: 0.5rem 0.75rem;
              font-size: 0.75rem; line-height: 1.8; }
    .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%;
           vertical-align: middle; margin-right: 4px; }
    #zoom-ctrl { position: absolute; bottom: 8px; left: 10px; display: flex; gap: 4px; }
    #zoom-ctrl button { padding: 0.2rem 0.5rem; font-size: 0.85rem; }
  </style>
</head>
<body>
<header>
  <strong>⚡ ZHA Live Map</strong>
  <select id="mapsel"></select>
  <button onclick="loadMap()">Load</button>
  <span id="status" style="color:#8b949e;font-size:0.8rem;">Select a map</span>
  <a href="/" style="margin-left:auto;">← Dashboard</a>
</header>
<div id="wrap">
  <div id="sidebar">
    <h3>Players</h3><div id="sb-players"></div>
    <h3>Boss</h3><div id="sb-boss">—</div>
    <h3>NPCs</h3><div id="sb-npcs"></div>
  </div>
  <div id="canvas-wrap">
    <canvas id="c"></canvas>
    <div id="coords"></div>
    <div id="legend">
      <div><span class="dot" style="background:#4fc3f7"></span>Player</div>
      <div><span class="dot" style="background:#f87171"></span>Bot</div>
      <div><span class="dot" style="background:#ff4444;box-shadow:0 0 6px #ff0000"></span>Mega Boss</div>
      <div><span class="dot" style="background:#fb923c;border-radius:0"></span>NPC</div>
      <div><span class="dot" style="background:#facc15;transform:rotate(45deg);border-radius:1px"></span>Item</div>
      <div><span class="dot" style="background:#a78bfa"></span>Bullet</div>
    </div>
    <div id="zoom-ctrl">
      <button onclick="zoom(-0.5)">−</button>
      <button onclick="zoom(0.5)">+</button>
      <button onclick="resetZoom()">Reset</button>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
let geo = null, state = null, scale = 1, panX = 0, panY = 0;
let isDragging = false, dragStart = {x:0,y:0}, panStart = {x:0,y:0};
let currentMap = null, pollTimer = null;

// ── Map selector ──────────────────────────────────────────────────────────────
fetch('/api/maps').then(r=>r.json()).then(maps => {
  const sel = document.getElementById('mapsel');
  maps.forEach(m => { const o = document.createElement('option'); o.value = o.textContent = m; sel.appendChild(o); });
  if (maps.length) { sel.value = maps[0]; loadMap(); }
});

function loadMap() {
  const m = document.getElementById('mapsel').value;
  if (!m) return;
  if (pollTimer) clearInterval(pollTimer);
  currentMap = m;
  document.getElementById('status').textContent = 'Loading…';
  geo = null; state = null;
  fetch('/api/map-geometry/' + m).then(r=>r.json()).then(g => {
    geo = g;
    resetZoom();
    document.getElementById('status').textContent = m;
    startPoll();
  });
}

function startPoll() {
  pollState();
  pollTimer = setInterval(pollState, 500);
}

function pollState() {
  if (!currentMap) return;
  fetch('/api/map-state/' + currentMap).then(r=>r.json()).then(s => {
    state = s;
    render();
    updateSidebar();
  });
}

// ── Sizing ────────────────────────────────────────────────────────────────────
function resize() {
  const wrap = document.getElementById('canvas-wrap');
  canvas.width  = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
  if (geo) render();
}
window.addEventListener('resize', resize);
resize();

function resetZoom() {
  if (!geo) { scale=1; panX=0; panY=0; return; }
  const mx = geo.maxx || 200, my = geo.maxy || 200;
  const padding = 40;
  const sx = (canvas.width  - padding*2) / mx;
  const sy = (canvas.height - padding*2) / my;
  scale = Math.min(sx, sy);
  panX = (canvas.width  - mx * scale) / 2;
  panY = (canvas.height - my * scale) / 2;
  render();
}

function zoom(delta) { scale = Math.max(0.5, Math.min(20, scale + delta)); render(); }

// ── Pan/drag ──────────────────────────────────────────────────────────────────
canvas.addEventListener('mousedown', e => {
  isDragging = true; dragStart = {x:e.clientX, y:e.clientY}; panStart = {x:panX, y:panY};
});
canvas.addEventListener('mousemove', e => {
  if (isDragging) { panX = panStart.x + (e.clientX-dragStart.x); panY = panStart.y + (e.clientY-dragStart.y); render(); }
  const [wx, wy] = screenToWorld(e.offsetX, e.offsetY);
  document.getElementById('coords').textContent = `x:${wx.toFixed(0)} y:${wy.toFixed(0)}`;
});
canvas.addEventListener('mouseup', () => isDragging = false);
canvas.addEventListener('mouseleave', () => isDragging = false);
canvas.addEventListener('wheel', e => { e.preventDefault(); zoom(e.deltaY < 0 ? 0.5 : -0.5); }, {passive:false});

function screenToWorld(sx, sy) { return [(sx-panX)/scale, (sy-panY)/scale]; }
function worldToScreen(wx, wy)  { return [wx*scale+panX,  wy*scale+panY]; }

// ── Rendering ─────────────────────────────────────────────────────────────────
function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  if (!geo) return;
  drawPlatforms();
  drawZones();
  if (state) {
    drawItems();
    drawWeapons();
    drawNPCs();
    drawBoss();
    drawPlayers();
  }
}

function drawPlatforms() {
  // Draw floor platforms (z1==z2==0) first, then walls
  const floors = geo.platforms.filter(p => p.z1 === 0 && p.z2 === 0);
  const walls  = geo.platforms.filter(p => !(p.z1 === 0 && p.z2 === 0));
  [...floors, ...walls].forEach(p => {
    const [sx, sy] = worldToScreen(p.x1, p.y1);
    const w = (p.x2 - p.x1) * scale, h = (p.y2 - p.y1) * scale;
    if (w <= 0 || h <= 0) return;
    const [r,g,b] = p.color;
    // Walls slightly darker + outlined
    const isWall = !(p.z1 === 0 && p.z2 === 0);
    ctx.fillStyle = isWall ? `rgb(${Math.max(0,r-30)},${Math.max(0,g-30)},${Math.max(0,b-30)})` : `rgb(${r},${g},${b})`;
    ctx.fillRect(sx, sy, Math.max(1,w), Math.max(1,h));
    if (isWall && scale > 1) {
      ctx.strokeStyle = 'rgba(0,0,0,0.4)'; ctx.lineWidth = 0.5; ctx.strokeRect(sx,sy,w,h);
    }
  });
}

function drawZones() {
  if (scale < 1.5) return;
  geo.zones.forEach(z => {
    const [sx, sy] = worldToScreen(z.x1, z.y1);
    const w = (z.x2 - z.x1) * scale, h = (z.y2 - z.y1) * scale;
    ctx.strokeStyle = 'rgba(88,166,255,0.25)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4,4]);
    ctx.strokeRect(sx, sy, w, h);
    ctx.setLineDash([]);
    if (scale > 2) {
      ctx.fillStyle = 'rgba(88,166,255,0.5)';
      ctx.font = `${Math.max(9, scale*3)}px system-ui`;
      ctx.fillText(z.name, sx+4, sy+12);
    }
  });
}

function drawPlayers() {
  state.players.forEach(p => {
    if (p.dead) return;
    const [sx, sy] = worldToScreen(p.x, p.y);
    const r = Math.max(4, scale*1.5);
    // Direction line
    const rad = (p.facing - 90) * Math.PI / 180;
    ctx.strokeStyle = p.isbot ? '#f87171' : '#4fc3f7';
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(sx,sy); ctx.lineTo(sx+Math.cos(rad)*r*2, sy+Math.sin(rad)*r*2); ctx.stroke();
    // Body dot
    ctx.fillStyle = p.isbot ? '#f87171' : '#4fc3f7';
    ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI*2); ctx.fill();
    // Name + HP
    if (scale > 1.5) {
      ctx.fillStyle = '#e6edf3';
      ctx.font = `bold ${Math.max(10, scale*2.5)}px system-ui`;
      ctx.fillText(p.name, sx+r+2, sy+4);
      const hpW = Math.max(20, scale*8), hpH = 3;
      ctx.fillStyle = '#21262d'; ctx.fillRect(sx-hpW/2, sy+r+2, hpW, hpH);
      const pct = Math.max(0, p.health / p.maxhp);
      ctx.fillStyle = pct>0.5 ? '#3fb950' : pct>0.25 ? '#d29922' : '#f85149';
      ctx.fillRect(sx-hpW/2, sy+r+2, hpW*pct, hpH);
    }
  });
}

function drawBoss() {
  if (!state.boss) return;
  const b = state.boss;
  const [sx, sy] = worldToScreen(b.x, b.y);
  const r = Math.max(8, scale*3);
  // Pulse glow
  const t = Date.now()/400;
  const glow = (Math.sin(t)*0.4+0.6);
  ctx.shadowColor = b.phase2 ? '#ff6600' : '#ff0000';
  ctx.shadowBlur = r * 3 * glow;
  ctx.fillStyle = b.phase2 ? '#ff6600' : '#ff2222';
  ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI*2); ctx.fill();
  ctx.shadowBlur = 0;
  // Skull cross
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(sx-r*0.5,sy-r*0.5); ctx.lineTo(sx+r*0.5,sy+r*0.5); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(sx+r*0.5,sy-r*0.5); ctx.lineTo(sx-r*0.5,sy+r*0.5); ctx.stroke();
  // HP bar
  const barW = Math.max(40, r*6), barH = 6;
  ctx.fillStyle = '#21262d'; ctx.fillRect(sx-barW/2, sy-r-12, barW, barH);
  const pct = b.health/b.maxhp;
  ctx.fillStyle = pct>0.5 ? '#f85149' : '#ff6600';
  ctx.fillRect(sx-barW/2, sy-r-12, barW*pct, barH);
  if (scale > 1) {
    ctx.fillStyle = '#ff4444';
    ctx.font = `bold ${Math.max(11, scale*3)}px system-ui`;
    ctx.fillText(`BOSS ${Math.round(pct*100)}%${b.phase2?' ⚡':''}`, sx-barW/2, sy-r-14);
  }
}

function drawNPCs() {
  state.npcs.forEach(n => {
    const [sx, sy] = worldToScreen(n.x, n.y);
    const r = Math.max(4, scale*1.2);
    ctx.fillStyle = '#fb923c';
    ctx.beginPath(); ctx.moveTo(sx,sy-r); ctx.lineTo(sx+r,sy+r); ctx.lineTo(sx-r,sy+r); ctx.closePath(); ctx.fill();
    if (scale > 2) { ctx.fillStyle='#fb923c'; ctx.font=`${Math.max(9,scale*2)}px system-ui`; ctx.fillText(n.name,sx+r+2,sy+4); }
  });
}

function drawItems() {
  state.items.forEach(it => {
    const [sx,sy] = worldToScreen(it.x, it.y);
    const r = Math.max(3, scale);
    ctx.fillStyle = '#facc15';
    ctx.save(); ctx.translate(sx,sy); ctx.rotate(Math.PI/4);
    ctx.fillRect(-r,-r,r*2,r*2); ctx.restore();
  });
}

function drawWeapons() {
  state.weapons.forEach(w => {
    const [sx,sy] = worldToScreen(w.x, w.y);
    ctx.fillStyle = 'rgba(167,139,250,0.7)';
    ctx.beginPath(); ctx.arc(sx,sy,Math.max(2,scale*0.6),0,Math.PI*2); ctx.fill();
  });
}

// Request animation frame to animate the boss pulse
function animLoop() { if (state && state.boss) render(); requestAnimationFrame(animLoop); }
animLoop();

// ── Sidebar ───────────────────────────────────────────────────────────────────
function hpColor(pct) { return pct>0.5 ? '#3fb950' : pct>0.25 ? '#d29922' : '#f85149'; }

function updateSidebar() {
  if (!state) return;
  // Players
  const pp = document.getElementById('sb-players');
  if (!state.players.length) { pp.innerHTML='<div style="color:#8b949e">—</div>'; }
  else {
    pp.innerHTML = state.players.map(p => {
      const pct = Math.max(0, p.health/p.maxhp);
      return `<div class="sentry">
        <div class="nm">${p.isbot?'🤖 ':''}${p.name}${p.dead?' <span style="color:#f85149">(dead)</span>':''}</div>
        <div class="dt">HP ${p.health}/${p.maxhp} · ${p.x},${p.y}</div>
        <div class="hpbar"><div class="hpfill" style="width:${pct*100}%;background:${hpColor(pct)}"></div></div>
      </div>`;
    }).join('');
  }
  // Boss
  const bb = document.getElementById('sb-boss');
  if (!state.boss) { bb.innerHTML='<div style="color:#8b949e">Not active</div>'; }
  else {
    const b = state.boss, pct = b.health/b.maxhp;
    bb.innerHTML = `<div class="sentry">
      <div class="nm" style="color:#f87171">Mega Boss${b.phase2?' ⚡ PHASE 2':''}</div>
      <div class="dt">HP ${b.health.toLocaleString()} / ${b.maxhp.toLocaleString()}</div>
      <div class="hpbar"><div class="hpfill" style="width:${pct*100}%;background:#f85149"></div></div>
    </div>`;
  }
  // NPCs
  const nn = document.getElementById('sb-npcs');
  nn.innerHTML = !state.npcs.length ? '<div style="color:#8b949e">—</div>'
    : state.npcs.map(n=>`<div class="sentry"><div class="nm">${n.name}</div><div class="dt">${n.x},${n.y} HP ${n.hp}</div></div>`).join('');
}
</script>
</body>
</html>
"""


@app.route("/live")
@login_required
def live_map():
    return _LIVE_MAP_PAGE


# ── startup ───────────────────────────────────────────────────────────────────

# ── MOTD helpers ─────────────────────────────────────────────────────────────

def _motd_path() -> str:
    if _motd_file:
        return os.path.join(SERVER_ROOT, _motd_file)
    return os.path.join(SERVER_ROOT, "motd.txt")

def _read_motd() -> str:
    p = _motd_path()
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def _write_motd(text: str) -> None:
    with open(_motd_path(), "w", encoding="utf-8") as f:
        f.write(text)

def _broadcast_all(msg: str) -> int:
    """Send a message to every online player. Returns count sent."""
    if _g is None:
        return 0
    count = 0
    for p in _g.players:
        try:
            _g.n.send_reliable(p.peer_id, msg, 2)
            count += 1
        except Exception:
            pass
    return count


# ── public MOTD route (fetched by game clients) ───────────────────────────────

@app.route("/motd.txt")
def serve_motd():
    from flask import Response
    return Response(_read_motd(), mimetype="text/plain")


# ── bot API routes (/api/bot/*) ───────────────────────────────────────────────

@app.route("/api/bot/status")
@api_key_required
def bot_status():
    players = _online_players()
    boss = getattr(_g, "mega_boss", None) if _g else None
    return jsonify({
        "online": len(players),
        "players": [getattr(p, "name", "") for p in players],
        "boss_alive": boss is not None and not getattr(boss, "dying", True),
        "boss_hp": getattr(boss, "health", 0) if boss else 0,
        "boss_phase2": getattr(boss, "phase2", False) if boss else False,
    })

@app.route("/api/bot/boss/spawn", methods=["POST"])
@api_key_required
def bot_boss_spawn():
    try:
        sys.path.insert(0, os.path.join(SERVER_ROOT, "modules", "entities"))
        from mega_boss import spawn_mega_boss
        result = spawn_mega_boss(100, 100, 0)
        return jsonify({"ok": result, "message": "Mega Boss spawned!" if result else "A Mega Boss is already alive."})
    except Exception as ex:
        return jsonify({"ok": False, "message": str(ex)}), 500

@app.route("/api/bot/motd", methods=["GET"])
@api_key_required
def bot_motd_get():
    return jsonify({"motd": _read_motd()})

@app.route("/api/bot/motd", methods=["POST"])
@api_key_required
def bot_motd_set():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"ok": False, "message": "No text provided"}), 400
    _write_motd(text)
    return jsonify({"ok": True, "message": "MOTD updated."})

@app.route("/api/bot/broadcast", methods=["POST"])
@api_key_required
def bot_broadcast():
    data = request.get_json(silent=True) or {}
    msg = data.get("message", "").strip()
    if not msg:
        return jsonify({"ok": False, "message": "No message provided"}), 400
    count = _broadcast_all(f"xmessage {msg}")
    return jsonify({"ok": True, "sent": count})

@app.route("/api/bot/online")
@api_key_required
def bot_online():
    players = _online_players()
    return jsonify([
        {"name": getattr(p, "name", ""), "map": getattr(p, "map", ""), "health": getattr(p, "health", 0)}
        for p in players
    ])

@app.route("/api/bot/kick/<name>", methods=["POST"])
@api_key_required
def bot_kick(name):
    ok = _kick_player(name)
    return jsonify({"ok": ok, "message": f"Kicked {name}." if ok else f"{name} is not online."})

@app.route("/api/bot/ban/<name>", methods=["POST"])
@api_key_required
def bot_ban(name):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason", "Banned by admin")
    try:
        sys.path.insert(0, os.path.join(SERVER_ROOT, "modules", "core"))
        import zh_auth as _auth
        _auth.ban_player(name, reason)
        _kick_player(name)
        return jsonify({"ok": True, "message": f"Banned {name}."})
    except Exception as ex:
        return jsonify({"ok": False, "message": str(ex)}), 500

@app.route("/api/bot/unban/<name>", methods=["POST"])
@api_key_required
def bot_unban(name):
    try:
        sys.path.insert(0, os.path.join(SERVER_ROOT, "modules", "core"))
        import zh_auth as _auth
        _auth.unban_player(name)
        return jsonify({"ok": True, "message": f"Unbanned {name}."})
    except Exception as ex:
        return jsonify({"ok": False, "message": str(ex)}), 500


# ── start ─────────────────────────────────────────────────────────────────────

def start_dashboard(globals_module, db_module, data_loader_module,
                    password: str = "admin", port: int = 8080,
                    api_key: str = "", motd_file: str = "") -> None:
    """
    Launch the Flask dashboard in a daemon thread.
    Call this from zhaserver.py after init_db().

        from dashboard.app import start_dashboard
        start_dashboard(g, db, data_loader, password=cfg_password, port=cfg_port,
                        api_key=cfg_api_key, motd_file=cfg_motd_file)
    """
    global _g, _db, _data_loader, _dashboard_password, _dashboard_port, _dashboard_api_key, _motd_file
    _g = globals_module
    _db = db_module
    _data_loader = data_loader_module
    _dashboard_password = password
    _dashboard_port = port
    _dashboard_api_key = api_key
    _motd_file = motd_file

    t = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False),
        daemon=True,
        name="ZHA-Dashboard"
    )
    t.start()
    print(f"[dashboard] Admin panel running at http://127.0.0.1:{port}")
