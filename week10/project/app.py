import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create tables if they don't exist
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show recent expenses and total spent"""
    expenses = db.execute("""
        SELECT amount, category, description, date
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 10
    """, session["user_id"])

    total = db.execute("""
        SELECT SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
    """, session["user_id"])[0]["total"] or 0.0

    return render_template("index.html", expenses=expenses, total=total)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a new expense"""
    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")

        if not amount or float(amount) <= 0:
            return apology("Please enter a valid amount (greater than 0)")

        if not category:
            return apology("Please select a category")

        db.execute("""
            INSERT INTO expenses (user_id, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, session["user_id"], float(amount), category, description, date)

        flash("Expense added successfully!")
        return redirect("/")

    else:
        return render_template("add.html")


@app.route("/history")
@login_required
def history():
    """Show full history of expenses"""
    expenses = db.execute("""
        SELECT amount, category, description, date
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, session["user_id"])

    return render_template("history.html", expenses=expenses)


@app.route("/summary")
@login_required
def summary():
    """Show summary by category and by month"""
    categories = db.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
    """, session["user_id"])

    monthly = db.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """, session["user_id"])

    return render_template("summary.html", categories=categories, monthly=monthly)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide username")

        if not password or password != confirmation:
            return apology("Passwords do not match or are empty")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Username already taken")

        hash = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        flash("Registered successfully! Please log in.")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Must provide username and password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
