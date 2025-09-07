from flask import Flask, render_template, request
import atm_core

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/balance", methods=["POST"])
def balance():
    atm_no = request.form.get("atm_no", "").strip()
    pin = request.form.get("pin", "").strip()

    if not atm_no or not pin:
        return "ATM number and PIN are required"

    data = atm_core.balance_inquiry(atm_no, pin)
    if data:
        account_no, name, balance = data
        return f"Account: {account_no}, Name: {name}, Balance: {balance}"
    return "Invalid ATM or PIN"

@app.route("/withdraw", methods=["POST"])
def withdraw():
    atm_no = request.form.get("atm_no", "").strip()
    pin = request.form.get("pin", "").strip()
    amount = request.form.get("amount", "").strip()

    if not atm_no or not pin or not amount:
        return "ATM number, PIN, and amount are required"

    try:
        amount = float(amount)
    except ValueError:
        return "Amount must be a number"

    success, msg = atm_core.withdraw(atm_no, pin, amount)
    return msg

@app.route("/transaction", methods=["POST"])
def transaction_route():
    atm_no = request.form.get("atm_no", "").strip()
    pin = request.form.get("pin", "").strip()
    receiver = request.form.get("receiver", "").strip()
    amount = request.form.get("amount", "").strip()

    if not atm_no or not pin or not receiver or not amount:
        return "All fields are required"

    try:
        amount = float(amount)
    except ValueError:
        return "Amount must be a number"

    success, msg = atm_core.transaction(atm_no, pin, receiver, amount)
    return msg

if __name__ == "__main__":
    app.run(debug=True)
