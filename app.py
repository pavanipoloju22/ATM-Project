from flask import Flask, render_template, request
import atm_core

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/balance", methods=["POST"])
def balance():
    atm_no = request.form.get("atm_no")
    pin = request.form.get("pin")

    if not atm_no or not pin:
        return "ATM number and PIN are required"

    # Convert to string (safer, in case stored as VARCHAR in DB)
    data = atm_core.balance_inquiry(str(atm_no), str(pin))
    if data:
        return f"Account: {data[0]}, Name: {data[1]}, Balance: {data[2]}"
    return "Invalid ATM or PIN"


@app.route("/withdraw", methods=["POST"])
def withdraw():
    atm_no = request.form.get("atm_no")
    pin = request.form.get("pin")
    amount = request.form.get("amount")

    if not atm_no or not pin or not amount:
        return "ATM number, PIN, and amount are required"

    success, msg = atm_core.withdraw(str(atm_no), str(pin), float(amount))
    return msg


@app.route("/transaction", methods=["POST"])
def transaction_route():
    atm_no = request.form.get("atm_no")
    pin = request.form.get("pin")
    receiver = request.form.get("receiver")
    amount = request.form.get("amount")

    if not atm_no or not pin or not receiver or not amount:
        return "All fields are required"

    success, msg = atm_core.transaction(str(atm_no), str(pin), str(receiver), float(amount))
    return msg


if __name__ == "__main__":
    app.run(debug=True)
