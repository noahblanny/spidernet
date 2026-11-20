"""SQLite inventory persistence."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def db_path():
    return Path(os.environ.get("SPIDERNET_DB", "spidernet.db"))

def connect():
    db = sqlite3.connect(db_path())
    db.row_factory = sqlite3.Row
    return db

def initialize():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS devices (
            ip TEXT PRIMARY KEY,
            hostname TEXT,
            mac TEXT,
            friendly_name TEXT,
            known INTEGER NOT NULL DEFAULT 0,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            target TEXT NOT NULL,
            addresses_checked INTEGER NOT NULL,
            responsive_hosts INTEGER NOT NULL
        );
        """)

def record_device(ip, hostname=None):
    now = datetime.now(timezone.utc).isoformat()
    with connect() as db:
        db.execute("""
        INSERT INTO devices (ip, hostname, first_seen, last_seen)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(ip) DO UPDATE SET
            hostname=COALESCE(excluded.hostname, devices.hostname),
            last_seen=excluded.last_seen
        """, (ip, hostname, now, now))

def record_scan(target, checked, responsive):
    with connect() as db:
        db.execute("INSERT INTO scans (started_at, target, addresses_checked, responsive_hosts) VALUES (?, ?, ?, ?)",
                   (datetime.now(timezone.utc).isoformat(), target, checked, responsive))

def list_devices():
    with connect() as db:
        return [dict(row) for row in db.execute("SELECT * FROM devices ORDER BY last_seen DESC")]

def list_scans():
    with connect() as db:
        return [dict(row) for row in db.execute("SELECT * FROM scans ORDER BY id DESC LIMIT 15")]

def label_device(ip, name, known, mac=None):
    with connect() as db:
        result = db.execute("UPDATE devices SET friendly_name=?, known=?, mac=COALESCE(?,mac) WHERE ip=?",
                            (name, int(known), mac, ip))
        return result.rowcount > 0
