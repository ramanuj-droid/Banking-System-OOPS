import streamlit as st
from account import SavingsAccount, CurrentAccount
from transaction import TransactionManager, log_transaction
import Auth
import pandas as pd

st.set_page_config(page_title="Savitr Bank", page_icon="🏦")

# ---------- Session Initialization ----------
if "user" not in st.session_state:
    st.session_state["user"] = None
if "accounts" not in st.session_state:
    st.session_state["accounts"] = {}
if "transactions" not in st.session_state:
    st.session_state["transactions"] = {}

# ---------- Auth ----------
if st.session_state["user"] is None:
    st.title("🔐 Login to Savitr Bank")

    auth_mode = st.radio("Choose action", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_mode == "Signup":
        if st.button("Register"):
            success, message = Auth.signup(username, password)
            st.success(message) if success else st.error(message)

    else:
        if st.button("Login"):
            success, message = Auth.login(username, password)
            if success:
                st.session_state["user"] = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error(message)
    st.stop()

# ---------- Sidebar ----------
menu = st.sidebar.selectbox("Select Action", [
    "🏠 Home", "➕ Create Account", "💰 Deposit", "💸 Withdraw",
    "📊 View Balance", "📜 Transaction History"
])

st.title("🏦 Savitr OOP Bank")
user = st.session_state["user"]

# ---------- Home ----------
if menu == "🏠 Home":
    st.write("Welcome to the Savitr Bank built with OOP and Streamlit!")

# ---------- Create Account ----------
elif menu == "➕ Create Account":
    st.subheader("Create New Account")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])
    balance = st.number_input("Initial Deposit", min_value=0.0)

    if st.button("Create Account"):
        if user in st.session_state["accounts"]:
            st.warning("Account already exists!")
        else:
            if acc_type == "Savings":
                acc = SavingsAccount(user, balance)
            else:
                acc = CurrentAccount(user, balance)
            st.session_state["accounts"][user] = acc
            st.success(f"{acc_type} account created!")

# ---------- Deposit ----------
elif menu == "💰 Deposit":
    st.subheader("Deposit Money")
    amount = st.number_input("Amount to Deposit", min_value=0.0)

    if st.button("Deposit"):
        if user in st.session_state["accounts"]:
            acc = st.session_state["accounts"][user]
            tm = TransactionManager(acc)
            msg = tm.deposit(amount)
            log_transaction(user, "Deposit", amount, acc.balance, st.session_state)
            st.success(msg)
        else:
            st.error("Account not found. Please create one.")

# ---------- Withdraw ----------
elif menu == "💸 Withdraw":
    st.subheader("Withdraw Money")
    amount = st.number_input("Amount to Withdraw", min_value=0.0)

    if st.button("Withdraw"):
        if user in st.session_state["accounts"]:
            acc = st.session_state["accounts"][user]
            tm = TransactionManager(acc)
            msg = tm.withdraw(amount)
            if "✅" in msg:
                log_transaction(user, "Withdraw", amount, acc.balance, st.session_state)
                st.success(msg)
            else:
                st.error(msg)
        else:
            st.error("Account not found. Please create one.")

# ---------- View Balance ----------
elif menu == "📊 View Balance":
    st.subheader("Account Info")

    if user in st.session_state["accounts"]:
        acc = st.session_state["accounts"][user]
        st.info(f"👤 Name: {acc.owner}")
        st.info(f"💰 Balance: ₹{acc.balance}")
        st.info(f"🏦 Type: {acc.account_type()}")
    else:
        st.error("No account found.")

# ---------- Transaction History ----------
elif menu == "📜 Transaction History":
    st.subheader("📜 Transaction History")

    txns = st.session_state["transactions"].get(user, [])
    if txns:
        df = pd.DataFrame(txns)
        st.dataframe(df, use_container_width=True)

        # Export to CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Statement", csv, "statement.csv", "text/csv")
    else:
        st.warning("No transactions yet.")
