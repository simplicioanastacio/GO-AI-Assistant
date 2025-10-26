# auth/auth.py
from db.db import get_connection
from utils.hashing import hash_password, verify_password
from mysql.connector import Error

def register_user(username: str, email: str, password: str) -> dict:
    if not (username and email and password):
        return {"ok": False, "error": "Missing fields", "user_id": None}
    hashed = hash_password(password)
    sql = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (username, email, hashed))
            conn.commit()
            user_id = cur.lastrowid
            cur.close()
        return {"ok": True, "error": None, "user_id": user_id}
    except Error as e:
        msg = str(e)
        if "Duplicate entry" in msg:
            if "users.username" in msg or "username" in msg:
                err = "Username already taken"
            else:
                err = "Email already registered"
        else:
            err = msg
        return {"ok": False, "error": err, "user_id": None}


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # <-- This ensures MySQL returns a dict instead of tuple
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and verify_password(password, user["password_hash"]):
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    return None
