import streamlit as st
import random

# ------------------------------------------
# initialize all_accounts session
# ------------------------------------------
if "all_accounts" not in st.session_state:
    st.session_state.all_accounts = []


# ------------------------------------------
# Open Account
# ------------------------------------------
def open_account(account_title, account_number, account_pin, initiale_deposit=0):
    account_id = random.randint(1000, 9999)

    account = {
        "account_id": account_id,
        "account_title": account_title,
        "account_number": account_number,
        "account_pin": account_pin,
        "account_balance": initiale_deposit,
    }

    st.session_state.all_accounts.append(account)
    return account


# ------------------------------------------
# Check Account Balance
# ------------------------------------------
def check_balance(account_number, account_pin):
    for acc in st.session_state.all_accounts:
        if acc["account_number"] == account_number:
            if acc["account_pin"] == account_pin:
                return acc["account_balance"]
            else:
                return "Invalid Pin"

    return f"{account_number} is invalid account"


# ------------------------------------------
# Withdraw Balance
# ------------------------------------------
def cash_withdrawl(account_number, account_pin, amount):
    for acc in st.session_state.all_accounts:
        if acc["account_number"] == account_number:
            if acc["account_pin"] == account_pin:
                if acc["account_balance"] >= amount:
                    acc["account_balance"] -= amount
                    return acc["account_balance"]
                else:
                    return "Insufficient Balance!"
            else:
                return "Invalid Pin"

    return f"{account_number} is invalid account"


# ------------------------------------------
# Cash Deposit
# ------------------------------------------
def cash_deposit(user_account, amount):
    for acc in st.session_state.all_accounts:
        if acc["account_number"] == user_account:
            acc["account_balance"] += amount
            return acc["account_balance"]

    return f"{user_account} is invalid account"


# ------------------------------------------
# Transfer Amount
# ------------------------------------------
def transfer_amount(user_account, user_pin, amount, beneficiary_account):
    for acc in st.session_state.all_accounts:
        if acc["account_number"] == user_account:
            if acc["account_pin"] == user_pin:
                if acc["account_balance"] >= amount:
                    for bacc in st.session_state.all_accounts:
                        if bacc["account_number"] == beneficiary_account:
                            acc["account_balance"] -= amount
                            bacc["account_balance"] += amount
                            return acc["account_balance"]

                    return f"{beneficiary_account} is invalid account"

                return "Insufficient Balance!"

            return "Invalid Pin"

    return f"{user_account} is invalid account"


# ------------------------------------------
# Delete Account
# ------------------------------------------
def close_account(user_account, user_pin):
    for i, acc in enumerate(st.session_state.all_accounts):
        if acc["account_number"] == user_account:
            if acc["account_pin"] == user_pin:
                remaining_amount = acc["account_balance"]
                account_number = acc["account_number"]

                acc["account_balance"] = 0
                del st.session_state.all_accounts[i]

                return f"Collect your amount {remaining_amount}. Account {account_number} closed successfully!"

            return "Invalid Pin"

    return f"{user_account} is invalid account"


# ------------------------------------------
# Streamlit UI
# ------------------------------------------
st.title("Banking System | Streamlit UI")

menu = st.sidebar.selectbox(
    label="Menu",
    options=[
        "Open Account",
        "Check Balance",
        "Cash Withdraw",
        "Cash Deposit",
        "Transfer Amount",
        "Close Account",
    ],
)


# ---------------------------------------------
# Open Account
# ---------------------------------------------
if menu == "Open Account":
    st.header("➕ Open a New Account")

    title = st.text_input(label="Enter your account title")
    pin = st.number_input(
        label="Enter your account PIN",
        min_value=1000,
        max_value=9999,
        step=1,
    )
    cnic = st.text_input("Enter CNIC")
    deposit = st.number_input("Initial Deposit", min_value=0, step=1)

    if st.button("Create Account"):
        account_number = random.randint(1000, 9999)

        acc = open_account(
            cnic,
            account_number,
            pin,
            deposit,
        )

        st.success("🎉 Account Created Successfully!")
        st.write(f"**Account Number:** `{acc['account_number']}`")
        st.write(f"**PIN:** `{acc['account_pin']}` (Save this!)")


# ---------------------------------------------
# Check Balance
# ---------------------------------------------
elif menu == "Check Balance":
    st.header("💰 Check Balance")

    acc_no = st.number_input(
        "Account Number",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    pin = st.number_input(
        "PIN",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    if st.button("Show Balance"):
        result = check_balance(acc_no, pin)

        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Your Current Balance is: **Rs {result}**")


# ---------------------------------------------
# Cash Deposit
# ---------------------------------------------
elif menu == "Cash Deposit":
    st.header("📥 Deposit Amount")

    acc_no = st.number_input(
        "Account Number",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    amt = st.number_input(
        "Amount",
        min_value=1,
        step=1,
    )

    if st.button("Deposit"):
        result = cash_deposit(acc_no, amt)

        if isinstance(result, str):
            st.error(result)
        else:
            st.success(
                f"Amount Deposited Rs: {amt}! "
                f"New Balance: **Rs {result}**"
            )


# ---------------------------------------------
# Cash Withdraw
# ---------------------------------------------
elif menu == "Cash Withdraw":
    st.header("📤 Withdraw Amount")

    acc_no = st.number_input(
        "Account Number",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    pin = st.number_input(
        "PIN",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    amt = st.number_input(
        "Amount",
        min_value=1,
        step=1,
    )

    if st.button("Withdraw"):
        result = cash_withdrawl(acc_no, pin, amt)

        if isinstance(result, str):
            st.error(result)
        else:
            st.success(
                f"Withdrawal Successful! "
                f"New Balance: **Rs {result}**"
            )


# ---------------------------------------------
# Transfer
# ---------------------------------------------
elif menu == "Transfer Amount":
    st.header("💸 Transfer Amount")

    acc_no = st.number_input(
        "Your Account Number",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    pin = st.number_input(
        "Your PIN",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    amt = st.number_input(
        "Amount",
        min_value=1,
        step=1,
    )

    ben = st.number_input(
        "Beneficiary Account Number",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    if st.button("Transfer"):
        result = transfer_amount(
            acc_no,
            pin,
            amt,
            ben,
        )

        if isinstance(result, str):
            st.error(result)
        else:
            st.success(
                f"Transfer Successful! "
                f"Remaining Balance: **Rs {result}**"
            )


# ---------------------------------------------
# Close Account
# ---------------------------------------------
elif menu == "Close Account":
    st.header("❌ Close Account")

    acc_no = st.number_input(
        "Account Number",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    pin = st.number_input(
        "PIN",
        min_value=1000,
        max_value=9999,
        step=1,
    )

    if st.button("Close Account"):
        msg = close_account(acc_no, pin)

        if "closed successfully" in msg:
            st.success(msg)
        else:
            st.error(msg)
