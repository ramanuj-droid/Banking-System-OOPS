import streamlit as st
from account import SavingsAccount, CurrentAccount
from transaction import TransactionManager
import Auth
import datetime

st.set_page_config(page_title="Savitr Bank", page_icon="🏦")

# ---------- Session Initialization ----------
if "user" not in st.session_state:
    st.session_state["user"] = None
if "accounts" not in st.session_state:
    st.session_state["accounts"] = {}
if "transaction" not in st.session_state:
    st.session_state["transaction"] = {}

# ---------- Auth System ----------
if st.session_state["user"] is None:
    st.title("🔐 Login to Savitr Bank")

    auth_mode = st.radio("Choose action", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_mode == "Signup":
        if st.button("Register"):
            success, message = Auth.signup(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)
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

# ---------- Transaction Logger ----------
def log_transaction(account_name, txn_type, amount, balance):
    txn = {
        "Date/Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Type": txn_type,
        "Amount": amount,
        "Balance": balance
    }
    if account_name not in st.session_state["transaction"]:
        st.session_state["transaction"][account_name] = []
    st.session_state["transaction"][account_name].append(txn)

# ---------- Sidebar Menu ----------
menu = st.sidebar.selectbox("Select Action", [
    "🏠 Home", "➕ Create Account", "💰 Deposit", "💸 Withdraw", 
    "📊 View Balance", "📜 Transaction History"
])

st.title("🏦 Savitr OOP Bank")

# ---------- Menu: Home ----------
if menu == "🏠 Home":
    st.write("Welcome to the Savitr Bank built with OOP and Streamlit!")
    st.write("Use the sidebar to navigate.")

# ---------- Menu: Create Account ----------
elif menu == "➕ Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Enter your name")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])
    balance = st.number_input("Initial Deposit", min_value=0.0)

    if st.button("Create Account"):
        if name in st.session_state['accounts']:
            st.warning("Account already exists!")
        else:
            if acc_type == "Savings":
                acc = SavingsAccount(name, balance)
            else:
                acc = CurrentAccount(name, balance)
            st.session_state['accounts'][name] = acc
            st.success(f"{acc_type} account created for {name}!")

# ---------- Menu: Deposit ----------
elif menu == "💰 Deposit":
    st.subheader("Deposit Money")
    name = st.text_input("Account Name")
    amount = st.number_input("Deposit Amount", min_value=0.0)

    if st.button("Deposit"):
        accs = st.session_state['accounts']
        if name in accs:
            tm = TransactionManager(accs[name])
            tm.deposit(amount)
            log_transaction(name, "Deposit", amount, accs[name].balance)
            st.success(f"{amount} was deposited")
        else:
            st.error("Account not found.")

# ---------- Menu: Withdraw ----------
elif menu == "💸 Withdraw":
    st.subheader("Withdraw Money")
    name = st.text_input("Account Name")
    amount = st.number_input("Withdrawal Amount", min_value=0.0)

    if st.button("Withdraw"):
        accs = st.session_state['accounts']
        if name in accs:
            tm = TransactionManager(accs[name])
            message = tm.withdraw(amount)
            if "✅" in message:
                log_transaction(name, "Withdraw", amount, accs[name].balance)
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Account not found.")

# ---------- Menu: View Balance ----------
elif menu == "📊 View Balance":
    st.subheader("Account Details")
    name = st.text_input("Enter account name")

    if st.button("Show Info"):
        accs = st.session_state['accounts']
        if name in accs:
            acc = accs[name]
            st.info(f"👤 Name: {acc.owner}")
            st.info(f"💰 Balance: ₹{acc.balance}")
            st.info(f"🏦 Type: {acc.account_type()}")
        else:
            st.error("Account not found.")

# ---------- Menu: Transaction History ----------
if st.button("View History"):
    txns = st.session_state["transaction"].get(name, [])
    if txns:
        import pandas as pd
        df = pd.DataFrame(txns)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Statement", csv, file_name="statement.csv", mime="text/csv")
    else:
        st.warning("No transactions found for this account.")

