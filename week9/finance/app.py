import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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

    # Select balance from users db
    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # Select purchases from purchases db
    purchases = db.execute(
        "SELECT name, symbol, SUM(shares) as total_shares, price FROM purchases WHERE user_id = ? GROUP BY symbol", session["user_id"])

    total = balance[0]["cash"]

    for purchase in purchases:
        price = purchases[0]["price"]
        total_price = purchases[0]["price"] * purchases[0]["total_shares"]
        total += total_price
        purchase["price"] = price
        purchase["total_price"] = total_price

    balance = balance[0]["cash"]

    return render_template("index.html", balance=balance, purchases=purchases, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Lookup For Symbol
        symbol = lookup(request.form.get("symbol"))

        # Ensure symbol exists
        if symbol == None:
            return apology("symbol doesn't exist", 400)

        # Check whether user submitted number
        if not shares.isnumeric():
            return apology("must provide positive integer for shares", 400)

        shares = int(shares)
        # Ensure user only submitted positive integer
        if shares <= 0:
            return apology("must provide positive integer for shares", 400)

        # Select how much cash the user currently has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Check whether user can afford the number of shares at the current price
        if (symbol["price"] * shares) > cash[0]["cash"]:
            return apology("canot afford the number of shares", 400)

        # Insert purchase details into purchases database
        db.execute("INSERT INTO purchases (user_id, name, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol["name"], symbol["symbol"], shares, symbol["price"])

        # Update user's cash after purchasing
        balance = cash[0]["cash"] - (symbol["price"] * shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM purchases WHERE user_id = ?", session["user_id"])

    if not history:
        return apology("no history", 400)

    for h in history:
        if h["shares"] > 0:
            h["status"] = "Bought"
        else:
            h["status"] = "Sold"

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Lookup For Symbol
        symbol = lookup(symbol)

        # Ensure symbol exists
        if symbol == None:
            return apology("symbol doesn't exist", 400)

        return render_template("quoted.html", symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        if not password_confirm:
            return apology("must confirm password", 400)

        # Ensure password and confirmation is the same
        if password != password_confirm:
            return apology("passwords are not matching", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check whether user already exists in the database
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Hashed password
        hashed_password = generate_password_hash(password)

        # Insert data into users database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Redirect user to login page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure user chose a symbol
        if not symbol:
            return apology("must provide symbol", 400)

        # Lookup For Symbol
        symbol = lookup(symbol)

        # Ensure symbol exists
        if symbol == None:
            return apology("symbol doesn't exist", 400)

        # Ensure user submitted shares
        if not shares:
            return apology("must provide shares", 400)

        shares = int(shares)

        # Ensure user only submitted positive integer
        if shares <= 0:
            return apology("must provide positive integer for shares", 400)

        total_shares = db.execute(
            "SELECT name, symbol, price, SUM(shares) AS total_shares FROM purchases WHERE user_id = ? AND symbol = ?", session["user_id"], symbol["symbol"])

        # Ensure user has enough shares
        if shares > total_shares[0]["total_shares"]:
            return apology("you don't have enough shares", 400)

        # Keep a sell record
        db.execute("INSERT INTO purchases (user_id, name, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], total_shares[0]["name"], symbol["symbol"], -shares, total_shares[0]["price"])

        # Stocks sold
        sold = shares * total_shares[0]["price"]

        # Select cash from users database
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Update users cash after stocks have been sold
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + sold, session["user_id"])

        # Redirect user to home page
        return redirect("/")
    else:
        # Select symbols from purchases
        symbols = db.execute("SELECT symbol FROM purchases WHERE user_id = ? GROUP BY symbol", session["user_id"])

        return render_template("sell.html", symbols=symbols)
