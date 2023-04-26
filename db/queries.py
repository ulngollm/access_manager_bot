import sqlite3
from access import AccessStatus

from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.getenv('DB_NAME')


def check_access(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.cursor().execute(
            'SELECT status from access_rights WHERE user_id=?', (user_id,)
        ).fetchone()[0]



def add_user(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        conn.cursor().execute(
            'INSERT or IGNORE INTO access_rights(user_id, status) VALUES(?,?)',
            (user_id, AccessStatus.DENIED)
        )


def deny_access(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE access_rights SET status = ? where user_id = ?',
        (AccessStatus.DENIED, user_id,)
    )
    conn.commit()


def allow_access(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE access_rights SET status = ? where user_id = ?',
        (AccessStatus.ALLOWED, user_id,)
    )
    conn.commit()