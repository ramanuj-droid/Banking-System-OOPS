import streamlit as st
from account import SavingsAccount, CurrentAccount
from transaction import TransactionManager

st.set_page_config(page_title="Savitr Bank", page_icon="🏦")

# Initialize session state
if 'accounts' not in st.session_state:
    st.session_state['accounts'] = {}

# Sidebar menu
menu = st.sidebar.selectbox("Select Action", ["🏠 Home", "➕ Create Account", "💰 Deposit", "💸 Withdraw", "📊 View Balance"])

st.title("🏦 Savitr OOP Bank")

if menu == "🏠 Home":
    st.write("Welcome to the Savitr Bank built with OOP and Streamlit!")
    st.write("Use the sidebar to navigate.")

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

elif menu == "💰 Deposit":
    st.subheader("Deposit Money")
    name = st.text_input("Account Name")
    amount = st.number_input("Deposit Amount", min_value=0.0)

    if st.button("Deposit"):
        accs = st.session_state['accounts']
        if name in accs:
            tm = TransactionManager(accs[name])
            tm.deposit(amount)
            st.write(f"{amount} was deposited")
        else:
            st.error("Account not found.")

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
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Account not found.")

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
