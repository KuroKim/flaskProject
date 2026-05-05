import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock


_lock = Lock()
_db_path = None


def configure_usage_db(path):
    global _db_path
    _db_path = Path(path)
    _db_path.parent.mkdir(parents=True, exist_ok=True)
    init_usage_db()


def init_usage_db():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tool_usage (
                tool_slug TEXT PRIMARY KEY,
                views INTEGER NOT NULL DEFAULT 0,
                last_used_at TEXT
            )
            """
        )


def increment_tool_view(tool_slug):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _lock:
        with _connect() as connection:
            connection.execute(
                """
                INSERT INTO tool_usage (tool_slug, views, last_used_at)
                VALUES (?, 1, ?)
                ON CONFLICT(tool_slug) DO UPDATE SET
                    views = views + 1,
                    last_used_at = excluded.last_used_at
                """,
                (tool_slug, now),
            )


def get_usage_stats(tools):
    tool_names = {tool["slug"]: tool["name"] for tool in tools}
    stats = {
        slug: {"tool_slug": slug, "tool_name": name, "views": 0, "last_used_at": None}
        for slug, name in tool_names.items()
    }

    with _connect() as connection:
        rows = connection.execute(
            "SELECT tool_slug, views, last_used_at FROM tool_usage ORDER BY views DESC, tool_slug ASC"
        ).fetchall()

    for row in rows:
        slug = row["tool_slug"]
        if slug not in stats:
            stats[slug] = {
                "tool_slug": slug,
                "tool_name": slug,
                "views": row["views"],
                "last_used_at": row["last_used_at"],
            }
        else:
            stats[slug]["views"] = row["views"]
            stats[slug]["last_used_at"] = row["last_used_at"]

    return sorted(stats.values(), key=lambda item: (-item["views"], item["tool_name"]))


def _connect():
    if _db_path is None:
        raise RuntimeError("Usage database is not configured")
    connection = sqlite3.connect(_db_path)
    connection.row_factory = sqlite3.Row
    return connection
