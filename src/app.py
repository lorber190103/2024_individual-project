from flask import Flask, render_template

from src.model import Deals, db, Games

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CheapShark.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")
