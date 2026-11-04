import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰"
)

st.title("💰 Personal Expense Tracker")
st.write("Track and manage your daily expenses easily.")

# Initialize expense records
if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.header("Add New Expense")

expense_name = st.text_input("Expense Name")

amount = st.number_input(
    "Amount",
    min_value=0.0,
    step=1.0
)

category = st.selectbox(
    "Category",
    ["Food", "Transport", "Shopping", "Education",
     "Bills", "Entertainment", "Other"]
)

expense_date = st.date_input("Expense Date", date.today())

if st.button("Add Expense"):
    if expense_name and amount > 0:
        st.session_state.expenses.append({
            "Expense": expense_name,
            "Amount": amount,
            "Category": category,
            "Date": expense_date
        })
        st.success("Expense added successfully!")
    else:
        st.error("Please enter an expense name and amount.")

# Display expenses
st.header("Expense History")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    st.dataframe(df, use_container_width=True)

    total = df["Amount"].sum()

    st.subheader("Total Expenses")
    st.metric("Total Spent", f"₹{total:.2f}")

    st.subheader("Expenses by Category")
    category_total = df.groupby("Category")["Amount"].sum()

    st.bar_chart(category_total)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Expense Report",
        csv,
        "expenses.csv",
        "text/csv"
    )

else:
    st.info("No expenses added yet. Start tracking your expenses!")

st.caption("Personal Expense Tracker - Python Project")
