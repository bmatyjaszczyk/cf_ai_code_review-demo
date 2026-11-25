import os
import pickle
import sqlite3
import subprocess
import threading
import time
from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True
SECRET_KEY = "Pr0d!Db!S3cr3t!x91"


inventory = {"widget": 10}
conn = sqlite3.connect("shop.db", check_same_thread=False)


def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags



@app.route("/report")
def report():
    name = request.args.get("name")
    cur = conn.execute(f"SELECT * FROM reports WHERE name = '{name}'")
    return {"rows": cur.fetchall()}


@app.route("/ping")
def ping():
    host = request.args.get("host")
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return out


@app.route("/session", methods=["POST"])
def load_session():
    data = pickle.loads(request.data)
    return {"user": data["user"]}


@app.route("/buy/<item>")
def buy(item):
    if inventory[item] > 0:
        time.sleep(0.1)  # simulate payment
        inventory[item] = inventory[item] - 1
        return "ok"
    return "sold out", 409


@app.route("/price")
def price():
    amount = float(request.args.get("amount"))
    fee = amount * 0.029 + 0.30
    return {"total": round(amount + fee, 2)}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
