import json

import requests

from app import app
from main import CheapShark
from model import Deals, Games, Stores, db

activator = CheapShark()


def test_JSON_current_deals():
    data = requests.get("https://www.cheapshark.com/api/1.0/deals?")
    data = data.json()
    new_data = json.dumps(data, indent=3)
    activator.JSON("current_deals")
    with open("data.json", "r") as f:
        assert f.read() == new_data


def test_JSON_search_for_deals():
    data = requests.get("https://www.cheapshark.com/api/1.0/deals?title=Batman")
    data = data.json()
    new_data = json.dumps(data, indent=3)
    activator.JSON("search_for_deals", "Batman")
    with open("data.json", "r") as f:
        assert f.read() == new_data


def test_JSON_stores():
    data = requests.get("https://www.cheapshark.com/api/1.0/stores")
    data = data.json()
    new_data = json.dumps(data, indent=3)
    activator.JSON("stores")
    with open("data.json", "r") as f:
        assert f.read() == new_data


def test_populate_database_stores():
    array = '[{"storeID":"0","storeName":"TestStore","isActive":1}]'
    data = json.loads(array)
    json_object = json.dumps(data, indent=3)
    with open("data.json", "w") as out_file:
        out_file.write(json_object)

    with app.app_context():
        activator.Populate_Database("stores")

        stores = db.session.query(Stores).filter(
            Stores.ID == 0,
            Stores.store_name == "TestStore",
            Stores.store_is_active == True).first()

        assert stores is not None


def test_populate_database_deals():
    array = '[{"title":"Aquarist",\
            "metacriticLink":"/game/aquarist/",\
            "dealID":"KpCYBX4Jk4oZif6HYlYO3jW9zjhhbCPjUVugamIhTMg%3D",\
            "storeID":"1","gameID":"253211","salePrice":"15.73",\
            "normalPrice":"30.98","isOnSale":"1","savings":"49.225307","metacriticScore":"0",\
            "steamRatingText":"Very Positive","steamRatingPercent":"84",\
            "steamRatingCount":"566","steamAppID":"1430760","releaseDate":1711670400,\
            "lastChange":1713205095}]'
    data = json.loads(array)
    json_object = json.dumps(data, indent=3)
    with open("data.json", "w") as out_file:
        out_file.write(json_object)

    with app.app_context():
        activator.Populate_Database("current_deals")

        deals = db.session.query(Deals).filter(
            Deals.title == "Aquarist",
            Deals.game_id == 253211,
            Deals.deal_id == "KpCYBX4Jk4oZif6HYlYO3jW9zjhhbCPjUVugamIhTMg%3D",
            Deals.store_id == 1).first()

        assert deals is not None

        games = db.session.query(Games).filter(
            Games.ID == 253211,
            Games.title == "Aquarist",
            Games.steam_app_id == "1430760").first()

        assert games is not None


def test_delete_value_store():
    with app.app_context():
        activator.Delete_Value("stores")
        stores = db.session.query(Stores).all()

    assert stores == []


def test_delete_value_deals():
    with app.app_context():
        activator.Delete_Value("deals")
        deals = db.session.query(Deals).all()

    assert deals == []


def test_delete_value_games():
    with app.app_context():
        activator.Delete_Value("games")
        games = db.session.query(Games).all()

    assert games == []
