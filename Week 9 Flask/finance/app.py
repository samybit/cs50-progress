import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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

    # Get user's stocks
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

    # Get user's cash balance
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    # Calculate totals
    portfolio_total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        portfolio_total += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, portfolio_total=portfolio_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        quote = lookup(symbol)
        if not quote:
            return apology("symbol not found")

        try:
            shares = int(shares)
            if shares < 1:
                return apology("shares must be a positive integer")
        except ValueError:
            return apology("shares must be a positive integer")

        user_id = session["user_id"]
        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_db[0]["cash"]

        item_price = quote["price"]
        total_cost = shares * item_price

        if cash < total_cost:
            return apology("can't afford")

        # Update user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)

        # Add transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol.upper(), shares, item_price)

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY transacted_timestamp DESC", user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        quote = lookup(symbol)

        if not quote:
            return apology("symbol not found")

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if not confirmation:
            return apology("must provide confirmation")
        if password != confirmation:
            return apology("passwords do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except ValueError:
            return apology("username already exists")

        session["user_id"] = new_user
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
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        try:
            shares = int(shares)
            if shares < 1:
                return apology("shares must be a positive integer")
        except ValueError:
            return apology("shares must be a positive integer")

        # Check ownership
        stocks = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)

        if len(stocks) != 1 or stocks[0]["total_shares"] < shares:
            return apology("not enough shares")

        quote = lookup(symbol)
        if not quote:
            return apology("symbol not found")

        price = quote["price"]
        total_sale_value = shares * price

        # Update user cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale_value, user_id)

        # Add transaction (negative shares for sell)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, price)

        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Personal Touch: Allow user to add cash"""
    if request.method == "POST":
        try:
            amount = int(request.form.get("amount"))
            if amount < 1:
                return apology("amount must be positive")
        except ValueError:
            return apology("amount must be positive")

        user_id = session["user_id"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, user_id)

        flash("Cash Added!")
        return redirect("/")
    else:
        return render_template("add_cash.html")
