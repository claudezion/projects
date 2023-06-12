import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, ccv


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def sharen(id, symbol):
    raws = db.execute("SELECT s_num FROM now WHERE user_id = ? AND name = ? ;", id, symbol)
    try:
        raw = raws[0]['s_num']
        return (raw)
    except:
        return ("-1")


def sharens(id, symbol):
    raws = db.execute("SELECT s_num FROM now WHERE user_id = ? AND symbol = ? ;", id, symbol)
    raw = raws[0]['s_num']
    return (raw)