import streamlit as st
import json
import os
from datetime import date, timedelta

DATA_FILE = "habits.json"

st.set_page_config(
    page_title="Habit Tracker with Streaks",
    page_icon="🎯",
    layout="wide"
)

def load_habits():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}

def save_habits(habits):
    with open(DATA_FILE, "w") as file:
        json.dump(habits, file, indent=2)

def current_streak(done_dates):
    days = set(done_dates)
    today = date.today()
    day = today if str(today) in days else today - timedelta(days=1)
    streak = 0
    while str(day) in days:
        streak += 1
        day -= timedelta(days=1)
    return streak

def longest_streak(done_dates):
    days = sorted(date.fromisoformat(d) for d in set(done_dates))
    best = run = 0
    previous = None

    for day in days:
        if previous and (day - previous).days == 1:
            run += 1
        else:
            run = 1
        best = max(best, run)
        previous = day

    return best

def completion_rate(done_dates):
    today = date.today()
    days = set(done_dates)
    completed = sum(
        str(today - timedelta(days=i)) in days
        for i in range(7)
    )
    return round(completed / 7 * 100)

habits = load_habits()

st.title("🎯 Habit Tracker with Streaks")
st.write("Build good habits, track your progress and stay consistent!")

st.divider()

st.subheader("➕ Add a New Habit")

with st.form("add_habit_form"):
    new_habit = st.text_input("Enter habit name")
    add_button = st.form_submit_button("Add Habit")

if add_button:
    name = new_habit.strip()
    if not name:
        st.warning("Please enter a habit name.")
    elif any(name.lower() == h.lower() for h in habits):
        st.warning("This habit already exists.")
    else:
        habits[name] = {
            "created": str(date.today()),
            "done": []
        }
        save_habits(habits)
        st.success(f"{name} added successfully!")
        st.rerun()

st.divider()

if habits:
    st.subheader("📊 Your Habit Dashboard")

    total = len(habits)
    completed_today = sum(
        str(date.today()) in data["done"]
        for data in habits.values()
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Habits", total)
    col2.metric("Completed Today", completed_today)
    col3.metric("Remaining Today", total - completed_today)

    st.divider()

    st.subheader("✅ Mark a Habit as Completed")

    selected = st.selectbox(
        "Choose a habit",
        sorted(habits.keys())
    )

    if st.button("Mark as Done"):
        today = str(date.today())

        if today in habits[selected]["done"]:
            st.info("This habit is already completed today.")
        else:
            habits[selected]["done"].append(today)
            habits[selected]["done"].sort()
            save_habits(habits)
            st.success("Great job! Habit completed!")
            st.rerun()

    st.divider()

    st.subheader("🔥 Your Habits and Streaks")

    for name, data in sorted(habits.items()):
        done = data["done"]
        today_done = str(date.today()) in done

        with st.container(border=True):
            st.write(f"*{name}*")

            a, b, c = st.columns(3)
            a.metric("Current Streak", f"{current_streak(done)} days")
            b.metric("Longest Streak", f"{longest_streak(done)} days")
            c.metric("7-Day Completion", f"{completion_rate(done)}%")

            if today_done:
                st.success("Completed today ✓")
            else:
                st.caption("Not completed today")

    st.divider()

    st.subheader("📅 Weekly Progress Report")

    week_days = [
        date.today() - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    st.write("Your habit completion over the last 7 days:")

    for name, data in sorted(habits.items()):
        st.write(f"*{name}*")
        columns = st.columns(7)

        for col, day in zip(columns, week_days):
            if str(day) in data["done"]:
                col.success(day.strftime("%a") + "\n✓")
            else:
                col.write(day.strftime("%a") + "\n·")

    st.divider()

    st.subheader("🗑️ Delete a Habit")

    delete_name = st.selectbox(
        "Select a habit to delete",
        sorted(habits.keys()),
        key="delete_habit"
    )

    if st.button("Delete Selected Habit"):
        del habits[delete_name]
        save_habits(habits)
        st.success("Habit deleted successfully.")
        st.rerun()

else:
    st.info("No habits added yet. Start by adding your first habit above!")

st.divider()
st.caption("Habit Tracker with Streaks | Python Mini Project")
