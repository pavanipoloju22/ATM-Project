import pymysql

def db_connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="atm_data"
    )

def check_login(atm_no, pw):
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT password FROM atm WHERE atmNo=%s", (atm_no,))
    password = cur.fetchone()
    if password and password[0] == pw:
        cur.execute("SELECT accountNo, name, balance FROM atm WHERE atmNo=%s", (atm_no,))
        data = cur.fetchone()
        con.close()
        return data
    con.close()
    return None

def balance_inquiry(atm_no, pw):
    return check_login(atm_no, pw)

def withdraw(atm_no, pw, amount):
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT password FROM atm WHERE atmNo=%s", (atm_no,))
    password = cur.fetchone()
    if not password or password[0] != pw:
        con.close()
        return False, "Invalid credentials"

    cur.execute("SELECT balance FROM atm WHERE atmNo=%s", (atm_no,))
    bal = cur.fetchone()
    if bal and bal[0] >= amount:
        new_bal = bal[0] - amount
        cur.execute("UPDATE atm SET balance=%s WHERE atmNo=%s", (new_bal, atm_no))
        con.commit()
        con.close()
        return True, f"Withdraw successful, new balance: {new_bal}"
    con.close()
    return False, "Insufficient balance"

def transaction(atm_no, pw, receiver_ac, amount):
    con = db_connect()
    cur = con.cursor()

    # Check password
    cur.execute("SELECT password FROM atm WHERE atmNo=%s", (atm_no,))
    password = cur.fetchone()
    if not password or password[0] != pw:
        con.close()
        return False, "Invalid credentials"

    # Check sender balance
    cur.execute("SELECT balance, accountNo FROM atm WHERE atmNo=%s", (atm_no,))
    sender_data = cur.fetchone()
    if not sender_data:
        con.close()
        return False, "Sender account not found"

    sender_bal, sender_account = sender_data
    if sender_bal < amount:
        con.close()
        return False, "Insufficient balance"

    # Check receiver account
    cur.execute("SELECT balance FROM atm WHERE accountNo=%s", (receiver_ac,))
    receiver_bal = cur.fetchone()
    if not receiver_bal:
        con.close()
        return False, "Receiver account not found"

    # Update balances
    new_sender_bal = sender_bal - amount
    new_receiver_bal = receiver_bal[0] + amount

    try:
        # Deduct from sender
        cur.execute("UPDATE atm SET balance=%s WHERE atmNo=%s", (new_sender_bal, atm_no))
        # Add to receiver
        cur.execute("UPDATE atm SET balance=%s WHERE accountNo=%s", (new_receiver_bal, receiver_ac))
        con.commit()
        con.close()
        return True, f"Transaction successful! New balance: {new_sender_bal}"
    except Exception as e:
        con.rollback()
        con.close()
        return False, f"Transaction failed: {e}"
