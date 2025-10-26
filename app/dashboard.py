# app/dashboard.py
import streamlit as st
from auth.session import current_user, logout_session
from db.db import get_connection
from llama.llama_runner import ask_go
from app.voice_assistant import speak, listen
import datetime

PRIMARY = "#1fb6ff"

# ----------- Reminders CRUD -----------
def add_reminder_db(user_id, text, remind_at, is_recurring=False):
    sql = """
    INSERT INTO reminders (user_id, reminder_txt, reminder_time, is_recurring, is_done, created_at)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, (user_id, text, remind_at, int(is_recurring), 0))
        conn.commit()
        cur.close()

def get_reminders_db(user_id):
    sql = """
    SELECT id, reminder_txt, reminder_time, is_recurring, is_done
    FROM reminders
    WHERE user_id = %s
    ORDER BY reminder_time DESC
    """
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()
        cur.close()
    return rows

def delete_reminder_db(reminder_id, user_id):
    sql = "DELETE FROM reminders WHERE id = %s AND user_id = %s"
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, (reminder_id, user_id))
        conn.commit()
        cur.close()

def edit_reminder(reminder_id):
    from db.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reminders WHERE id=%s", (reminder_id,))
    reminder = cursor.fetchone()

    st.subheader("Edit Reminder")
    new_text = st.text_input("Reminder text", value=reminder["reminder_txt"])
    new_time = st.text_input("Reminder time", value=str(reminder["reminder_time"]))
    is_recurring = st.checkbox("Recurring?", value=bool(reminder["is_recurring"]))

    if st.button("Save Changes"):
        cursor.execute(
            "UPDATE reminders SET reminder_txt=%s, reminder_time=%s, is_recurring=%s WHERE id=%s",
            (new_text, new_time, int(is_recurring), reminder_id)
        )
        conn.commit()
        st.success("Reminder updated successfully!")
        st.rerun()

    cursor.close()
    conn.close()

# ----------- Marathon Goals -----------
def save_training_goal_db(user_id, distance_km, target_date, fitness_level, goal_description=""):
    sql = """
    INSERT INTO training_goals
    (user_id, race_distance_km, target_race_date, current_fitness_level, goal_description, created_at)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, (user_id, distance_km, target_date, fitness_level, goal_description))
        conn.commit()
        cur.close()

def get_training_goals_db(user_id):
    sql = """
    SELECT id, race_distance_km, target_race_date, current_fitness_level, goal_description
    FROM training_goals
    WHERE user_id = %s
    ORDER BY target_race_date DESC
    """
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()
        cur.close()
    return rows

def generate_training_plan_prompt(distance_km, target_date, fitness_level, days_per_week):
    return (
        f"Create a {days_per_week}-day-per-week progressive {fitness_level} marathon training plan "
        f"targeting {distance_km} km by {target_date}. Provide weekly structure "
        f"(easy runs, long runs, tempo, intervals, rest, cross-training) and weekly mileage."
    )

# ----------- Dashboard UI -----------
def dashboard():
    user = current_user()
    if not user:
        st.error("Please log in.")
        return

    st.title("GO — Dashboard")
    st.subheader(f"Welcome, {user['username']}")

    tabs = st.tabs(["Ask GO", "Reminders", "Marathon"])

    # Ask GO tab
    with tabs[0]:
        st.markdown("### Ask GO (voice or text)")
        if st.button("🎙️ Ask by voice", key="dash_voice"):
            q = listen()
            if not q:
                st.error("Couldn't capture your voice. Try again.")
            else:
                st.markdown(f"**You asked:** {q}")
                ans = ask_go(q)
                st.success(ans)
                speak(ans)
        typed = st.text_input("Type your question (text only)")
        if st.button("Ask (text)"):
            if typed.strip():
                ans = ask_go(typed.strip())
                st.success(ans)
            else:
                st.warning("Type a question first.")

    # Reminders tab
    with tabs[1]:
        st.markdown("### Reminders")
        with st.form("add_reminder_form", clear_on_submit=True):
            text = st.text_input("Reminder text")
            date = st.date_input("Date", value=datetime.date.today())
            time = st.time_input("Time", value=datetime.datetime.now().time().replace(second=0, microsecond=0))
            recurring = st.checkbox("Recurring", value=False)
            if st.form_submit_button("Add reminder"):
                dt = datetime.datetime.combine(date, time)
                add_reminder_db(user["id"], text, dt, recurring)
                st.success("Reminder added.")
                st.rerun()

        reminders = get_reminders_db(user["id"])
        if not reminders:
            st.info("No reminders yet.")
        for r in reminders:
            st.write(f"• **{r['reminder_txt']}** — {r['reminder_time']}")
            col1, col2 = st.columns(2)
            if col1.button(f"Edit {r['id']}"):
                new_text = st.text_input("Text", value=r['reminder_txt'], key=f"newtxt_{r['id']}")
                new_date = st.date_input("Date", value=r['reminder_time'].date(), key=f"newdate_{r['id']}")
                new_time = st.time_input("Time", value=r['reminder_time'].time(), key=f"newtime_{r['id']}")
                new_rec = st.checkbox("Recurring", value=bool(r['is_recurring']), key=f"newrec_{r['id']}")
                if st.button("Save", key=f"save_{r['id']}"):
                    dt = datetime.datetime.combine(new_date, new_time)
                    edit_reminder(r['id'], user['id'], new_text, dt, new_rec)
                    st.success("Updated.")
                    st.rerun()
            if col2.button(f"Delete {r['id']}"):
                delete_reminder_db(r['id'], user['id'])
                st.success("Deleted.")
                st.rerun()

    # Marathon tab
    with tabs[2]:
        st.markdown("### Marathon Planner")
        with st.form("start_marathon", clear_on_submit=False):
            dist = st.number_input("Goal distance (km)", min_value=1.0, value=42.195, step=0.1)
            target_date = st.date_input("Target race date")
            fitness = st.selectbox("Fitness level", ["Beginner", "Intermediate", "Advanced"])
            days_per_week = st.slider("Training days per week", 3, 7, 5)
            if st.form_submit_button("Save goal & generate plan"):
                save_training_goal_db(
                    user["id"], dist, target_date, fitness, f"Target {dist}km by {target_date}"
                )
                plan = ask_go(generate_training_plan_prompt(dist, target_date, fitness, days_per_week))
                st.subheader("AI-generated training plan")
                st.text(plan)
