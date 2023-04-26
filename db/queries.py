import sqlite3


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
        'INSERT INTO access_rights(user_id) VALUES(?)',
        (user_id,)
    )
    conn.commit()
    conn.close()


def set_access(user_id: int, status_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute(
        'UPDATE access_rights SET status = ? where user_id = ?',
        (status_id, user_id,)
    )
    conn.commit()
    conn.close()