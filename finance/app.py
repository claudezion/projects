import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, ccv
from datetime import datetime, timezone
from query import sharen, sharens

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


def time_now():
    """HELPER: get current UTC date and time"""
    now_utc = datetime.now(timezone.utc)
    return str(now_utc.date()) + ' @time ' + now_utc.time().strftime("%H:%M:%S")


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
    try:
        current_price = {}
        total = {}
        query = db.execute("SELECT user_id,symbol,name,s_num FROM now WHERE user_id = ?;", session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
        ftotal = cash[0]["cash"]
        for i in query:
            total[i["symbol"]] = lookup(i["symbol"])["price"] * int(i["s_num"])
            current_price[i["symbol"]] = lookup(i["symbol"])["price"]
            ftotal = ftotal+total[i["symbol"]]
        return render_template("index.html", ftotal=ftotal, query=query, cash=cash[0]["cash"], total=total, current_price=current_price)
    except:
        return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        q = (lookup(request.form.get("symbol")))
        sh = request.form.get("shares")
        if sh.isnumeric() == False:
            return apology("Enter A Number")
        else:
            sh = int(sh)
            if q is None:
                return apology("Invalid Symbol")
            elif (sh < 1):
                return apology("You Can't Buy Negative Number Of Shares")
            else:
                sp = float(q["price"] * sh)
                c = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]['cash']
                remain = c - sp
                if (remain < 0):
                    return apology("cannot afford the number of shares at the current price")
                else:
                    n = q["name"]
                    p = float(q["price"])
                    pp = ("%.2f" % p)
                    s = q["symbol"]
                    uc = c - sp
                    answer = int(sharen(session["user_id"], n))
                    if (answer == -1):
                        db.execute("INSERT INTO now (user_id, symbol, name, s_num) VALUES(?, ?, ?, ?);",
                                   session["user_id"], s, n, sh)
                    else:
                        st = answer + sh
                        db.execute("UPDATE now SET s_num = ? WHERE user_id = ? AND name = ? ;", st, session["user_id"], n)
                    db.execute("INSERT INTO history (user_id, symbol, name, s_num, action, price, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?);",
                               session["user_id"], s, n, sh, "Bought", pp, time_now())
                    db.execute("UPDATE users SET cash = ? WHERE id = ? ;", uc, session["user_id"])
                    flash("Bought...!")
                    return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    raws = db.execute("SELECT symbol, name, s_num, action, price, timestamp FROM history WHERE user_id = ? ;", session["user_id"])
    return render_template("history.html", table=raws)


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
        q = (lookup(request.form.get("symbol")))
        if q is None:
            return apology("Invalid Symbol")
        else:
            n = q["name"]
            p = usd(float(q["price"]))
            s = q["symbol"]
            return render_template("quoted.html", name=n, price=p, symbol=s)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        rusername = request.form.get("username")
        rpassword = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?;", rusername)
        if (len(rusername) < 1):
            return apology("Enter A Username")
        elif (len(rpassword) < 1):
            return apology("Enter A Password")
        elif (len(confirmation) < 1):
            return apology("Re_Enter The Password")
        elif (rpassword != confirmation):
            return apology("Passwords Do Not Match")
        elif (len(rows) == 1):
            return apology("Username Already Exists")
        else:
            gpassword = generate_password_hash(rpassword, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?);", rusername, gpassword)
            return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        capital = db.execute("SELECT cash FROM users WHERE id = ? ", session["user_id"])
        quantity = db.execute("SELECT s_num FROM now WHERE user_id = ? AND symbol = ?",
                              session["user_id"], request.form.get("symbol"))

        if request.form.get("symbol") == None:
            return apology("Symbol required")

        elif lookup(request.form.get("symbol")) == None:
            return apology("Invalid symbol")

        elif request.form.get("shares") == None:
            return apology("Incomplete input")

        elif int(request.form.get("shares")) > quantity[0]["s_num"]:
            return apology("Not enough shares")

        else:
            name = lookup(request.form.get("symbol"))
            response = lookup(request.form.get("symbol"))
            amount = response["price"] * int(request.form.get("shares"))
            db.execute("INSERT INTO history (user_id, symbol, name, s_num, action, price, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?);",
                       session["user_id"], name["symbol"], name["name"], int(request.form.get("shares")), "Sold", name["price"], time_now())
            db.execute("UPDATE users SET cash = ? WHERE id = ? ", capital[0]["cash"]+amount, session["user_id"])
            if int(quantity[0]["s_num"])-int(request.form.get("shares")) == 0:
                db.execute("DELETE FROM now WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
            else:
                db.execute("UPDATE now SET s_num = ? WHERE user_id = ? AND symbol = ?",
                           int(quantity[0]["s_num"])-int(request.form.get("shares")), session["user_id"], request.form.get("symbol"))
            flash('Sold!')
            return redirect("/")
    else:
        raws = db.execute("SELECT DISTINCT(symbol) FROM now WHERE user_id = ?;", session["user_id"])
        return render_template("sell.html", shares=raws)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """Top-up cash"""
    if request.method == "POST":
        confirmation = request.form.get("confirm")
        if confirmation == "Yes":
            c = request.form.get("cc")
            ci = int(c)
            cn = ccv(ci)
            if (cn == "no"):
                return apology("Invalid Credit Card Number")
            elif (cn == "ok"):
                a = float(request.form.get("amount"))
                r = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]['cash']
                new = r + a
                db.execute("UPDATE users SET cash = ? WHERE id = ? ;", new, session["user_id"])
                message = "Your Account Has Been Topped-up Successfully...!"
                flash(message)
                return redirect("/")
            else:
                return apology("Bug...!")

        else:
            return apology("Select Yes If You Want To Top-up")
    else:
        return render_template("topup.html")
