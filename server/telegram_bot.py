"""
telegram_bot.py — Zero Hour Assault admin bot.

Run alongside the game server (or on any machine that can reach the dashboard):
    python telegram_bot.py

Configure in server.conf:
    telegram_bot_token  = <your bot token from @BotFather>
    telegram_admin_ids  = 7810113372,987654321   (comma-separated)
    dashboard_api_key   = <same key as in server.conf>

The bot communicates with the game via the dashboard API at DASHBOARD_URL.
Set DASHBOARD_URL below to wherever your dashboard is reachable.

Commands:
    /status          — online player count, boss state
    /online          — list online players
    /spawnboss       — spawn the Mega Boss
    /broadcast <msg> — send a message to all online players
    /kick <name>     — kick a player
    /ban <name> [reason] — ban a player
    /unban <name>    — unban a player
    /motd            — show current MOTD
    /setmotd <text>  — update the MOTD
    /help            — list commands
"""

import os
import sys
import time
import json
import logging
import requests

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
log = logging.getLogger("zha_bot")

# ── Configuration ─────────────────────────────────────────────────────────────

# Edit these, or set via environment variables / server.conf auto-load below.
BOT_TOKEN       = ""       # overridden from server.conf
ADMIN_IDS: list[int] = []  # overridden from server.conf
API_KEY         = ""       # overridden from server.conf
DASHBOARD_URL   = "http://127.0.0.1:8080"   # change if dashboard is on another machine
MOTD_URL        = "https://spacemangaming.vineyard.haus/zero/motd_update.php"
MOTD_SECRET     = "changeme_secret"   # must match SECRET_KEY in motd_update.php


def _load_conf():
    """Load config from server.conf if present."""
    global BOT_TOKEN, ADMIN_IDS, API_KEY
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.conf")
    if not os.path.exists(conf_path):
        return
    with open(conf_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            key, val = k.strip().lower(), v.strip()
            if key == "telegram_bot_token" and val:
                BOT_TOKEN = val
            elif key == "telegram_admin_ids" and val:
                ADMIN_IDS = [int(x.strip()) for x in val.split(",") if x.strip().isdigit()]
            elif key == "dashboard_api_key" and val:
                API_KEY = val

_load_conf()

# ── Telegram helpers ──────────────────────────────────────────────────────────

TG_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def tg(method: str, **kwargs):
    try:
        r = requests.post(f"{TG_BASE}/{method}", json=kwargs, timeout=10)
        return r.json()
    except Exception as e:
        log.warning(f"Telegram {method} error: {e}")
        return {}

def send(chat_id: int, text: str):
    tg("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML")

def send_long(chat_id: int, text: str):
    """Split long messages into 4096-char chunks."""
    for i in range(0, len(text), 4096):
        send(chat_id, text[i:i+4096])

# ── Dashboard API helpers ─────────────────────────────────────────────────────

_HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

def api_get(path: str) -> dict:
    try:
        r = requests.get(f"{DASHBOARD_URL}{path}", headers=_HEADERS, timeout=8)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_post(path: str, data: dict = None) -> dict:
    try:
        r = requests.post(f"{DASHBOARD_URL}{path}", headers=_HEADERS,
                          json=data or {}, timeout=8)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# ── Command handlers ──────────────────────────────────────────────────────────

def cmd_help(chat_id: int, _args: str):
    send(chat_id, (
        "<b>ZHA Admin Bot — Commands</b>\n\n"
        "/status — server + boss status\n"
        "/online — list online players\n"
        "/spawnboss — spawn the Mega Boss\n"
        "/broadcast &lt;message&gt; — message all players\n"
        "/kick &lt;name&gt; — kick a player\n"
        "/ban &lt;name&gt; [reason] — ban a player\n"
        "/unban &lt;name&gt; — unban a player\n"
        "/motd — show current MOTD\n"
        "/setmotd &lt;text&gt; — update MOTD\n"
        "/help — this list"
    ))

def cmd_status(chat_id: int, _args: str):
    d = api_get("/api/bot/status")
    if "error" in d:
        send(chat_id, f"❌ Dashboard error: {d['error']}")
        return
    boss_line = ""
    if d.get("boss_alive"):
        hp = d.get("boss_hp", 0)
        phase = " (Phase 2 🔥)" if d.get("boss_phase2") else ""
        boss_line = f"\n👹 Mega Boss alive — {hp:,} HP{phase}"
    else:
        boss_line = "\n💀 Mega Boss not spawned"
    send(chat_id, f"🖥 <b>Server Status</b>\n👥 Online: {d.get('online', 0)}{boss_line}")

def cmd_online(chat_id: int, _args: str):
    d = api_get("/api/bot/online")
    if isinstance(d, dict) and "error" in d:
        send(chat_id, f"❌ {d['error']}")
        return
    if not d:
        send(chat_id, "Nobody online.")
        return
    lines = [f"• <b>{p['name']}</b> — {p['map']} ({p['health']} HP)" for p in d]
    send_long(chat_id, f"👥 <b>Online ({len(d)})</b>\n" + "\n".join(lines))

def cmd_spawnboss(chat_id: int, _args: str):
    d = api_post("/api/bot/boss/spawn")
    icon = "✅" if d.get("ok") else "⚠️"
    send(chat_id, f"{icon} {d.get('message', 'Unknown response')}")

def cmd_broadcast(chat_id: int, args: str):
    if not args.strip():
        send(chat_id, "Usage: /broadcast <message>")
        return
    d = api_post("/api/bot/broadcast", {"message": args.strip()})
    if d.get("ok"):
        send(chat_id, f"📢 Sent to {d.get('sent', 0)} player(s).")
    else:
        send(chat_id, f"❌ {d.get('message', 'Failed')}")

def cmd_kick(chat_id: int, args: str):
    name = args.strip()
    if not name:
        send(chat_id, "Usage: /kick <name>")
        return
    d = api_post(f"/api/bot/kick/{name}")
    icon = "✅" if d.get("ok") else "⚠️"
    send(chat_id, f"{icon} {d.get('message', '')}")

def cmd_ban(chat_id: int, args: str):
    parts = args.strip().split(None, 1)
    if not parts:
        send(chat_id, "Usage: /ban <name> [reason]")
        return
    name = parts[0]
    reason = parts[1] if len(parts) > 1 else "Banned by admin"
    d = api_post(f"/api/bot/ban/{name}", {"reason": reason})
    icon = "✅" if d.get("ok") else "⚠️"
    send(chat_id, f"{icon} {d.get('message', '')}")

def cmd_unban(chat_id: int, args: str):
    name = args.strip()
    if not name:
        send(chat_id, "Usage: /unban <name>")
        return
    d = api_post(f"/api/bot/unban/{name}")
    icon = "✅" if d.get("ok") else "⚠️"
    send(chat_id, f"{icon} {d.get('message', '')}")

def cmd_motd(chat_id: int, _args: str):
    try:
        r = requests.get(MOTD_URL, timeout=8)
        motd = r.text.strip()
        send(chat_id, f"📢 <b>Current MOTD:</b>\n{motd or '(empty)'}")
    except Exception as e:
        send(chat_id, f"❌ Could not fetch MOTD: {e}")

def cmd_setmotd(chat_id: int, args: str):
    text = args.strip()
    if not text:
        send(chat_id, "Usage: /setmotd <text>")
        return
    try:
        r = requests.post(MOTD_URL, data=text.encode("utf-8"),
                          headers={"X-Secret-Key": MOTD_SECRET}, timeout=8)
        if r.ok:
            send(chat_id, "✅ MOTD updated.")
        else:
            send(chat_id, f"❌ Server returned {r.status_code}: {r.text[:200]}")
    except Exception as e:
        send(chat_id, f"❌ Failed to update MOTD: {e}")

COMMANDS = {
    "help":      cmd_help,
    "start":     cmd_help,
    "status":    cmd_status,
    "online":    cmd_online,
    "spawnboss": cmd_spawnboss,
    "broadcast": cmd_broadcast,
    "kick":      cmd_kick,
    "ban":       cmd_ban,
    "unban":     cmd_unban,
    "motd":      cmd_motd,
    "setmotd":   cmd_setmotd,
}

# ── Notify admins (used by the rest of the server if imported) ────────────────

def notify_admins(text: str):
    for admin_id in ADMIN_IDS:
        send(admin_id, text)

# ── Polling loop ──────────────────────────────────────────────────────────────

def run():
    if not BOT_TOKEN:
        log.error("No telegram_bot_token set in server.conf — exiting.")
        sys.exit(1)
    if not API_KEY:
        log.warning("No dashboard_api_key set — bot API calls will fail.")

    log.info(f"Starting ZHA Telegram bot (admins: {ADMIN_IDS})")
    offset = 0

    while True:
        try:
            resp = requests.get(
                f"{TG_BASE}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=35,
            ).json()

            for update in resp.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                user_id = msg.get("from", {}).get("id")
                text = msg.get("text", "")

                if not chat_id or not text.startswith("/"):
                    continue

                if ADMIN_IDS and user_id not in ADMIN_IDS:
                    send(chat_id, "⛔ Unauthorized.")
                    continue

                # parse command and args (strip bot username suffix e.g. /cmd@BotName)
                parts = text.split(None, 1)
                cmd_raw = parts[0].lstrip("/").split("@")[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                handler = COMMANDS.get(cmd_raw)
                if handler:
                    try:
                        handler(chat_id, args)
                    except Exception as e:
                        log.exception(f"Handler {cmd_raw} error")
                        send(chat_id, f"❌ Error: {e}")
                else:
                    send(chat_id, f"Unknown command: /{cmd_raw}\nTry /help")

        except requests.exceptions.RequestException as e:
            log.warning(f"Network error: {e} — retrying in 5s")
            time.sleep(5)
        except Exception as e:
            log.exception("Unexpected error in polling loop")
            time.sleep(5)


if __name__ == "__main__":
    run()
