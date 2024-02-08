from flask import Flask, render_template

from src.model import Deals, db, Games
from src.main import CRUD

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CheapShark.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    activator = CRUD()
    activator.Populate_Database()
    return render_template("home.html")


@app.route("/Current_Deals")
def current_deals():
    return render_template("home.html")


@app.route("/Search_for_Deal")
def search_for_deals():
    return render_template("home.html")


@app.route("/Game")
def games():
    return render_template("home.html")
