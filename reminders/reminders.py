# reminders/reminders.py
import mysql.connector
from db.db import get_db_connection

def add_reminder(user_id, title, date, time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reminders (user_id, title, date, time)
        VALUES (%s, %s, %s, %s)
    """, (user_id, title, date, time))
    conn.commit()
    cursor.close()
    conn.close()

def get_reminders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reminders WHERE user_id = %s ORDER BY date, time", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def delete_reminder(reminder_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = %s AND user_id = %s", (reminder_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_reminder(reminder_id, user_id, title, date, time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reminders SET title=%s, date=%s, time=%s
        WHERE id=%s AND user_id=%s
    """, (title, date, time, reminder_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
