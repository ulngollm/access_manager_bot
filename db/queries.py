import sqlite3
from access import AccessStatus

from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.getenv('DB_NAME')


def check_access(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    result = conn.cursor().execute(
        'SELECT status from access_rights WHERE user_id=?', (user_id,)
    ).fetchone()
    conn.close()
    return result


def add_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'INSERT or IGNORE INTO access_rights(user_id, status) VALUES(?,?)',
        (user_id, AccessStatus.DENIED)
    )
    conn.close()


def deny_access(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE access_rights SET status = ? where user_id = ?',
        (AccessStatus.DENIED, user_id,)
    )
    conn.commit()
    conn.close()


def allow_access(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE access_rights SET status = ? where user_id = ?',
        (AccessStatus.ALLOWED, user_id,)
    )
    conn.commit()
    conn.close()