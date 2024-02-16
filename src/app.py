from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from src.model import Deals, db, Games, Stores
from src.main import CheapShark

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CheapShark.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Current_Deals")
def current_deals():
    choice = "current_deals"
    activator = CheapShark()
    activator.JSON(choice)
    activator.Populate_Database(choice)
    deals = db.session.execute(db.select(Deals)).scalars()
    return render_template("home.html", deals=deals)


@app.route("/Search_for_Deal", methods=["GET", "POST"])
def search_for_deals():
    search = ""
    if request.method == "POST":
        search = request.form.get("deal")
    choice = "search_for_deals"
    activator = CheapShark()
    activator.JSON(choice, search)
    activator.Populate_Database(choice)
    deals = db.session.query(Deals.title.like(f'%{search}%'))
    return render_template("search_for_deal.html", deals=deals)


@app.route("/Stores")
def games():
    choice = "stores"
    activator = CheapShark()
    activator.JSON(choice)
    activator.Populate_Database(choice)
    stores = db.session.execute(db.select(Stores)).scalars()
    return render_template("stores.html", stores=stores)


@app.errorhandler(Exception)
def handle_exception(exception):
    if isinstance(exception, HTTPException):
        return exception

    return render_template("error.html", exception=exception), 500
