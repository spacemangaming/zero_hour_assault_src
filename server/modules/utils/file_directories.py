# directory functions written by nbm studios
import os
import shutil

# ── SQLite shim ────────────────────────────────────────────────────────────────
# All paths matching  chars/<name>/<field>.usr  (or  chars/<name>  for dirs)
# are transparently routed to the SQLite DB layer instead of the filesystem.
# This lets the entire codebase use the old file API without modification.

def _is_chars_file(path: str):
    """If path is chars/<name>/<field>.usr return (name, field), else None."""
    p = path.replace("\\", "/")
    parts = p.split("/")
    if len(parts) == 3 and parts[0] == "chars" and parts[2].endswith(".usr"):
        name = parts[1]
        field = parts[2][:-4]   # strip .usr
        return name, field
    return None


def _is_chars_dir(path: str):
    """If path is chars/<name> return name, else None."""
    p = path.replace("\\", "/").rstrip("/")
    parts = p.split("/")
    if len(parts) == 2 and parts[0] == "chars" and parts[1]:
        return parts[1]
    return None


def _db():
    """Lazy import of db module (avoids circular imports at module load time)."""
    import db
    return db

# ── Server-state text file shim ───────────────────────────────────────────────
# Files written/read by server code (not hand-edited content) are also routed
# to the server_state table in SQLite so nothing lives on the filesystem.
_SERVER_STATE_FILES = {
    "adminlog.txt", "chats.log", "errors.log", "error.log",
    "grouphistory.txt", "zitemdata.txt", "ioszitemdata.txt",
    "changes.txt", "frozen.txt", "suggest.txt", "razeon.txt",
    "data_edits.log", "motd.txt", "store.txt", "event_store.txt",
}

def _is_sv_file(path: str) -> bool:
    """True if path (basename) is a known server-state file stored in DB."""
    import os
    return os.path.basename(path.replace("\\", "/")) in _SERVER_STATE_FILES



# ── directory API ─────────────────────────────────────────────────────────────

def directory_create(path):
    name = _is_chars_dir(path)
    if name is not None:
        _db().create_player_row(name)
        return True
    try:
        os.mkdir(path)
        return True
    except:
        return False


def directory_delete(path):
    name = _is_chars_dir(path)
    if name is not None:
        _db().delete_player_row(name)
        return True
    try:
        shutil.rmtree(path)
        return True
    except:
        return False


def directory_exists2(path):
    name = _is_chars_dir(path)
    if name is not None:
        return _db().player_exists_icase(name)
    # Fallback: case-insensitive filesystem check
    path = os.path.normpath(path)
    parent_dir, target_dir = os.path.split(path)
    if not os.path.isdir(parent_dir):
        return False
    for entry in os.listdir(parent_dir):
        if entry.lower() == target_dir.lower() and os.path.isdir(os.path.join(parent_dir, entry)):
            return True
    return False


def directory_exists(path):
    name = _is_chars_dir(path)
    if name is not None:
        return _db().player_exists(name)
    return os.path.isdir(path)


# ── file API ──────────────────────────────────────────────────────────────────

def file_exists(path):
    cf = _is_chars_file(path)
    if cf is not None:
        name, field = cf
        return _db().charexists(name, field)
    if _is_sv_file(path):
        return _db().sv_exists(path)
    return os.path.isfile(path)


def find_files(path):
    l = []
    if not os.path.exists(path):
        return l
    for each in os.listdir(path):
        if os.path.isfile(path + "/" + each):
            l.append(each)
    return l


def find_directories(path):
    # Special case: listing the chars/ directory returns DB player names
    if path == "chars":
        try:
            d = _db()
            if d._DB_PATH is not None:
                rows = d._fetchall("SELECT name FROM players ORDER BY LOWER(name)")
                return [r[0] for r in rows]
        except Exception:
            pass
    l = []
    if not os.path.exists(path):
        return l
    for each in os.listdir(path):
        if os.path.isdir(path + "/" + each):
            l.append(each)
    return l


def file_copy(path, dest, overwrite=False):
    if overwrite == False and os.path.isfile(path):
        return False
    else:
        shutil.copy(path, dest)
        return True


def file_delete(path):
    cf = _is_chars_file(path)
    if cf is not None:
        name, field = cf
        _db().chardelete(name, field)
        return True
    if _is_sv_file(path):
        _db().sv_delete(path)
        return True
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False


def find_recursive(path, wildcard="*.*"):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if wildcard in file or wildcard == "*.*":
                files.append(os.path.join(r, file))
    return files


def file_put_contents(filename, content, mode="w"):
    cf = _is_chars_file(filename)
    if cf is not None:
        name, field = cf
        if mode in ("wb", "ab"):
            if isinstance(content, (bytes, bytearray)):
                if mode == "ab":
                    # append: read existing + concatenate
                    existing = _db().charreadb(name, field)
                    _db().charwriteb(name, field, existing + bytes(content))
                else:
                    _db().charwriteb(name, field, bytes(content))
            else:
                _db().charwriteb(name, field, str(content).encode())
        else:
            if mode == "a":
                # append: read existing text + append
                existing = _db().charread(name, field, "")
                _db().charwrite(name, field, existing + str(content))
            else:
                _db().charwrite(name, field, str(content))
        return True
    if _is_sv_file(filename):
        if mode in ("wb", "ab"):
            data = bytes(content) if isinstance(content, (bytes, bytearray)) else str(content).encode()
            if mode == "ab":
                existing = _db().sv_read(filename) or b""
                _db().sv_write(filename, existing + data)
            else:
                _db().sv_write(filename, data)
        else:
            text = str(content)
            if mode == "a":
                existing = _db().sv_read_text(filename, "")
                _db().sv_write_text(filename, existing + text)
            else:
                _db().sv_write_text(filename, text)
        return True
    try:
        f = open(filename, mode)
    except:
        return False
    f.write(content)
    f.close()


def file_get_contents(filename, mode="r"):
    cf = _is_chars_file(filename)
    if cf is not None:
        name, field = cf
        if mode == "rb":
            return _db().charreadb(name, field)
        return _db().charread(name, field, "")
    if _is_sv_file(filename):
        data = _db().sv_read(filename)
        if mode == "rb":
            return data if data else b""
        return data.decode("utf-8", errors="ignore") if data else ""
    if not os.path.isfile(filename):
        return ""
    f = open(filename, mode)
    ret = f.read()
    f.close()
    return ret
