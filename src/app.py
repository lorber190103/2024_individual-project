from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from src.model import Deals, db, Games, Stores
from src.main import CheapShark

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CheapShark.db"

db.init_app(app)

activator = CheapShark()

with app.app_context():
    db.create_all()
    activator.JSON("stores")
    activator.Populate_Database("stores")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Current_Deals")
def current_deals():
    choice = "current_deals"
    activator.JSON(choice)
    activator.Populate_Database(choice)
    deals = db.session.query(Deals).filter(Deals.savings >= 0.1
                                           ).join(Stores, Deals.store_id == Stores.ID
                                                  ).order_by(Deals.timestamp.desc()
                                                             ).all()
    return render_template("current_deals.html", deals=deals)


@app.route("/Search_for_Deal", methods=["GET", "POST"])
def search_for_deals():
    search = ""
    if request.method == "POST":
        search = request.form.get("deal")
        choice = "search_for_deals"
        activator.JSON(choice, search)
        activator.Populate_Database(choice)
    deals = db.session.query(Deals).filter(Deals.title.like(f'%{search}%')
                                           ).join(Stores, Deals.store_id == Stores.ID
                                                  ).all()
    return render_template("search_for_deal.html", deals=deals)


@app.route("/Game_Info/<int:game_id>")
def game_info(game_id):
    game_info = db.session.query(Games).filter(Games.ID == game_id).all()
    return render_template("game_info.html", game_info=game_info)


@app.route("/Stores")
def games():
    stores = db.session.execute(db.select(Stores)).scalars()
    return render_template("stores.html", stores=stores)


@app.errorhandler(Exception)
def handle_exception(exception):
    if isinstance(exception, HTTPException):
        return exception

    return render_template("error.html", exception=exception), 500
