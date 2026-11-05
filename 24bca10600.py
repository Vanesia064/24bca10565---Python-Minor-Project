"""Habit Tracker with Streaks - a command-line mini project (standard library only)."""
import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = "habits.json"


def load_habits():
    """Load habits from the JSON file (empty dict if missing or damaged)."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def save_habits(habits):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(habits, f, indent=2)


def to_date(text):
    """Convert 'YYYY-MM-DD' text into a date object."""
    return datetime.strptime(text, "%Y-%m-%d").date()


def current_streak(done_dates, today=None):
    """Number of days in a row ending today (or yesterday if today is not done yet)."""
    today = today or date.today()
    days = {to_date(d) for d in done_dates}
    day = today if today in days else today - timedelta(days=1)
    streak = 0
    while day in days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def longest_streak(done_dates):
    """Longest run of consecutive days ever completed."""
    days = sorted({to_date(d) for d in done_dates})
    best = run = 0
    prev = None
    for d in days:
        run = run + 1 if prev and (d - prev).days == 1 else 1
        best = max(best, run)
        prev = d
    return best


def completion_rate(done_dates, window=7, today=None):
    """Percentage of the last window days on which the habit was done."""
    today = today or date.today()
    days = {to_date(d) for d in done_dates}
    hits = sum(1 for i in range(window) if today - timedelta(days=i) in days)
    return hits / window * 100


def add_habit(habits):
    name = input("Habit name (e.g. Drink water): ").strip()
    if not name:
        print("Habit name cannot be empty.")
        return
    if name.lower() in (h.lower() for h in habits):
        print("That habit already exists.")
        return
    habits[name] = {"created": str(date.today()), "done": []}
    save_habits(habits)
    print(f"Habit '{name}' added!")


def pick_habit(habits):
    """Show a numbered list and return the chosen habit name (or None)."""
    if not habits:
        print("No habits yet. Add one first.")
        return None
    names = sorted(habits)
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")
    try:
        n = int(input("Choose habit number: "))
        if n < 1:
            raise IndexError
        return names[n - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None


def check_in(habits):
    name = pick_habit(habits)
    if name is None:
        return
    text = input("Date YYYY-MM-DD (Enter for today): ").strip() or str(date.today())
    try:
        chosen = to_date(text)
    except ValueError:
        print("Invalid date format.")
        return
    if chosen > date.today():
        print("You cannot check in for a future date.")
        return
    day = str(chosen)
    if day in habits[name]["done"]:
        print("Already marked as done for that day.")
        return
    habits[name]["done"].append(day)
    habits[name]["done"].sort()
    save_habits(habits)
    print(f"Great job! Current streak: {current_streak(habits[name]['done'])} day(s)")


def view_habits(habits):
    if not habits:
        print("No habits yet. Add one first.")
        return
    print(f"\n{'Habit':<20}{'Streak':>7}{'Best':>6}{'7-day':>8}{'Today':>7}")
    print("-" * 48)
    today = str(date.today())
    for name in sorted(habits):
        done = habits[name]["done"]
        mark = "Yes" if today in done else "No"
        rate = completion_rate(done)
        print(f"{name[:19]:<20}{current_streak(done):>7}{longest_streak(done):>6}{rate:>7.0f}%{mark:>7}")


def weekly_report(habits):
    if not habits:
        print("No habits yet. Add one first.")
        return
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    print("\nLast 7 days (X = done, . = missed)")
    print(f"{'Habit':<20}" + " ".join(d.strftime("%a")[:2] for d in days))
    print("-" * 40)
    for name in sorted(habits):
        done = set(habits[name]["done"])
        row = "  ".join("X" if str(d) in done else "." for d in days)
        print(f"{name[:19]:<20}{row}")
    best = max(habits, key=lambda n: completion_rate(habits[n]["done"]))
    if completion_rate(habits[best]["done"]) > 0:
        print(f"\nMost consistent habit this week: {best}")


def delete_habit(habits):
    name = pick_habit(habits)
    if name is None:
        return
    if input(f"Delete '{name}' and all its history? (y/n): ").strip().lower() == "y":
        del habits[name]
        save_habits(habits)
        print("Deleted.")
    else:
        print("Cancelled.")


def main():
    habits = load_habits()
    actions = {"1": add_habit, "2": check_in, "3": view_habits,
               "4": weekly_report, "5": delete_habit}
    while True:
        print("\n=== HABIT TRACKER ===")
        print("1. Add habit\n2. Check in (mark done)\n3. View habits & streaks")
        print("4. Weekly report\n5. Delete habit\n6. Exit")
        choice = input("Choose: ").strip()
        if choice == "6":
            print("Keep going. See you tomorrow!")
            break
        action = actions.get(choice)
        if action:
            action(habits)
        else:
            print("Invalid choice.")


if _name_ == "_main_":
    main()
