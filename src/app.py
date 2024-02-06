from flask import Flask, render_template

from src.model import CheapShark, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.db"

db.init_app(app)

with app.app_context():
    db.create_all()

