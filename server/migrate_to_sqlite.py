#!/usr/bin/env python3
"""
migrate_to_sqlite.py — one-time migration from flat .usr files to SQLite.

Run ONCE from the server/ directory BEFORE starting the updated server:

    cd server
    python migrate_to_sqlite.py

What it does:
  1. Reads every directory under server/chars/<name>/
  2. For each <name>, creates a player row in zha_players.db
  3. For each <field>.usr file:
       - text files  → charwrite(name, field, content)
       - binary files → charwriteb(name, field, bytes)
  4. Prints a summary.

Safe to re-run: uses INSERT OR IGNORE so existing rows are not overwritten.
"""

import os
import sys
import pickle
import traceback

# Ensure modules/ subdirs are on path
HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = os.path.join(HERE, "modules")
for sub in ("utils", "core", "net", "entities"):
    p = os.path.join(MODULES, sub)
    if os.path.isdir(p):
        sys.path.insert(0, p)
sys.path.insert(0, MODULES)

import db

CHARS_DIR = os.path.join(HERE, "chars")
DB_PATH   = os.path.join(HERE, "zha_players.db")

# Fields that are stored as raw bytes (pickle / struct data)
BINARY_FIELDS = {
    "inventory", "storeinventory", "ammo", "current_char", "bought_chars",
    "friendlist", "pendingfriendlist", "blocks", "silenced", "tokenplayers",
    "task_data", "banned", "banenddate", "backpacktimer",
    "groupinvitations", "communityinvitations",
}


def migrate():
    if not os.path.isdir(CHARS_DIR):
        print(f"[!] chars/ directory not found at {CHARS_DIR}")
        print("    Nothing to migrate.")
        return

    db.init_db(DB_PATH)

    players = sorted(
        d for d in os.listdir(CHARS_DIR)
        if os.path.isdir(os.path.join(CHARS_DIR, d))
    )
    print(f"[migrate] Found {len(players)} player directories.")

    total_fields = 0
    total_errors = 0

    for name in players:
        player_dir = os.path.join(CHARS_DIR, name)
        db.create_player_row(name)

        for fname in os.listdir(player_dir):
            if not fname.endswith(".usr"):
                continue
            field = fname[:-4]   # strip .usr
            fpath = os.path.join(player_dir, fname)

            try:
                if field in BINARY_FIELDS:
                    with open(fpath, "rb") as f:
                        data = f.read()
                    if data:
                        db.charwriteb(name, field, data)
                else:
                    # Try text first, fall back to binary
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                            val = f.read().strip()
                        db.charwrite(name, field, val)
                    except Exception:
                        with open(fpath, "rb") as f:
                            data = f.read()
                        db.charwriteb(name, field, data)
                total_fields += 1
            except Exception as ex:
                print(f"  [!] {name}/{field}: {ex}")
                total_errors += 1

        print(f"  [ok] {name}")

    print()
    print("=" * 60)
    print(f"Migration complete.")
    print(f"  Players migrated : {len(players)}")
    print(f"  Fields migrated  : {total_fields}")
    print(f"  Errors           : {total_errors}")
    print(f"  Database         : {DB_PATH}")
    print("=" * 60)
    print()
    print("The original chars/ directory has NOT been deleted.")
    print("Once you've verified the server works, you may remove it.")


if __name__ == "__main__":
    os.chdir(HERE)
    migrate()
