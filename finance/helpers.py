import os
import requests
import urllib.parse
from cs50 import SQL

from flask import redirect, render_template, request, session
from functools import wraps


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    try:
        return str(f"${value:,.2f}")
    except TypeError:
        return ("")


def ccv(num):
    """Validating the Credit card number"""
    digit1 = 0
    digit2 = 0
    num_digits = 0
    sum_of_double_odds = 0
    sum_of_evens = 0

    while num > 0:
        digit2 = digit1
        digit1 = num % 10

        if num_digits % 2 == 0:
            sum_of_evens += digit1
        else:
            multiple = 2 * digit1
            sum_of_double_odds += (multiple // 10) + (multiple % 10)

        num //= 10
        num_digits += 1

    is_valid = (sum_of_evens + sum_of_double_odds) % 10 == 0
    first_two_digits = (digit1 * 10) + digit2

    if digit1 == 4 and num_digits >= 13 and num_digits <= 16 and is_valid:
        return ("ok")
    elif first_two_digits >= 51 and first_two_digits <= 55 and num_digits == 16 and is_valid:
        return ("ok")
    elif (first_two_digits == 34 or first_two_digits == 37) and num_digits == 15 and is_valid:
        return ("ok")
    else:
        return ("no")

