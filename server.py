from flask import Flask, render_template, request, redirect, url_for, session
from core.db import init_db, get_credentials
from core.campaign import list_campaigns
import yaml
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form["username"] == config["admin"]["username"] and
                request.form["password"] == config["admin"]["password"]):
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    campaigns = list_campaigns()
    return render_template("dashboard.html", campaigns=campaigns)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/credentials")
def credentials():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    creds = get_credentials()
    return render_template("view_credentials.html", credentials=creds)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
