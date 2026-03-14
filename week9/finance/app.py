import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    holdings = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = rows[0]["cash"]

    portfolio = []
    stocks_total = 0
    for h in holdings:
        quote = lookup(h["symbol"])
        if quote:
            total = quote["price"] * h["total_shares"]
            stocks_total += total
            portfolio.append({
                "symbol": h["symbol"],
                "name": quote["name"],
                "shares": h["total_shares"],
                "price": quote["price"],
                "total": total
            })

    grand_total = cash + stocks_total
    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]
        cost = quote["price"] * shares

        if cash < cost:
            return apology("can't afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                   cost, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, quote["symbol"], shares, quote["price"]
        )

        flash(f"Bought {shares} share(s) of {quote['symbol']}!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        user_id
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords do not match", 400)

        hash = generate_password_hash(password)

        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )
        except ValueError:
            return apology("username already exists", 400)

        session["user_id"] = user_id
        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must select a stock", 400)

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        rows = db.execute(
            "SELECT SUM(shares) AS total FROM transactions WHERE user_id = ? AND symbol = ?",
            user_id, symbol
        )
        owned = rows[0]["total"] or 0
        if shares > owned:
            return apology("too many shares", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        proceeds = quote["price"] * shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   proceeds, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, symbol, -shares, quote["price"]
        )

        flash(f"Sold {shares} share(s) of {symbol}!")
        return redirect("/")

    else:
        holdings = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id
        )
        return render_template("sell.html", holdings=holdings)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password (personal touch)"""
    user_id = session["user_id"]

    if request.method == "POST":
        current = request.form.get("current")
        if not current:
            return apology("must provide current password", 400)

        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not check_password_hash(rows[0]["hash"], current):
            return apology("current password is incorrect", 400)

        new = request.form.get("new")
        if not new:
            return apology("must provide new password", 400)

        confirmation = request.form.get("confirmation")
        if new != confirmation:
            return apology("passwords do not match", 400)

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new), user_id
        )

        flash("Password changed!")
        return redirect("/")

    else:
        return render_template("password.html")
