from flask import Flask, render_template, request
import atm_core

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/balance", methods=["POST"])
def balance():
    atm_no = int(request.form["atm_no"])
    pin = int(request.form["pin"])
    data = atm_core.balance_inquiry(atm_no, pin)
    if data:
        return f"Account: {data[0]}, Name: {data[1]}, Balance: {data[2]}"
    return "Invalid ATM or PIN"

@app.route("/withdraw", methods=["POST"])
def withdraw():
    atm_no = int(request.form["atm_no"])
    pin = int(request.form["pin"])
    amount = int(request.form["amount"])
    success, msg = atm_core.withdraw(atm_no, pin, amount)
    return msg

@app.route("/transaction", methods=["POST"])
def transaction_route():
    atm_no = int(request.form["atm_no"])
    pin = int(request.form["pin"])
    receiver = int(request.form["receiver"])
    amount = int(request.form["amount"])
    success, msg = atm_core.transaction(atm_no, pin, receiver, amount)
    return msg

if __name__ == "__main__":
    app.run(debug=True)
