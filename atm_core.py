import pymysql
import os

def db_connect():
    """Connect to the database using environment variables (Render-ready)."""
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST","dbhost.render.com"),
            user=os.getenv("DB_USER","root"),
            password=os.getenv("DB_PASS","123456"),
            database=os.getenv("DB_NAME","atm_data"),
            port=int(os.getenv("DB_PORT", 3306))
        )
    except Exception as e:
        print("Database connection failed:", e)
        return None


def check_login(atm_no, pw):
    con = db_connect()
    if not con:
        return None
    cur = con.cursor()
    cur.execute("SELECT accountNo, name, balance, password FROM atm WHERE atmNo=%s", (atm_no,))
    row = cur.fetchone()
    if not row:
        cur.close()
        con.close()
        return None

    accountNo, name, balance, db_password = row
    if str(db_password) != str(pw):
        cur.close()
        con.close()
        return None

    cur.close()
    con.close()
    return (accountNo, name, balance)


def balance_inquiry(atm_no, pw):
    return check_login(atm_no, pw)


def withdraw(atm_no, pw, amount):
    user = check_login(atm_no, pw)
    if not user:
        return False, "Invalid credentials"

    con = db_connect()
    if not con:
        return False, "Database connection failed"
    cur = con.cursor()

    accountNo, name, balance = user
    if balance >= amount:
        new_bal = balance - amount
        cur.execute("UPDATE atm SET balance=%s WHERE atmNo=%s", (new_bal, atm_no))
        con.commit()
        cur.close()
        con.close()
        return True, f"Withdraw successful, new balance: {new_bal}"

    cur.close()
    con.close()
    return False, "Insufficient balance"


def transaction(atm_no, pw, receiver_ac, amount):
    user = check_login(atm_no, pw)
    if not user:
        return False, "Invalid credentials"

    con = db_connect()
    if not con:
        return False, "Database connection failed"
    cur = con.cursor()

    sender_account, sender_name, sender_bal = user
    if sender_bal < amount:
        cur.close()
        con.close()
        return False, "Insufficient balance"

    # Check receiver account
    cur.execute("SELECT balance FROM atm WHERE accountNo=%s", (receiver_ac,))
    receiver_bal = cur.fetchone()
    if not receiver_bal:
        cur.close()
        con.close()
        return False, "Receiver account not found"

    new_sender_bal = sender_bal - amount
    new_receiver_bal = receiver_bal[0] + amount

    try:
        cur.execute("UPDATE atm SET balance=%s WHERE atmNo=%s", (new_sender_bal, atm_no))
        cur.execute("UPDATE atm SET balance=%s WHERE accountNo=%s", (new_receiver_bal, receiver_ac))
        con.commit()
        cur.close()
        con.close()
        return True, f"Transaction successful! New balance: {new_sender_bal}"
    except Exception as e:
        con.rollback()
        cur.close()
        con.close()
        return False, f"Transaction failed: {e}"
