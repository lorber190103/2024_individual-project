import json
import time

import requests

from src.model import Deals, Games, db

url = "https://www.cheapshark.com/api/1.0/deals?"

payload = {}
headers = {}

r = requests.get(url)
data = r.json()
json_object = json.dumps(data, indent=3)
with open("data.json", "w") as outfile:
    outfile.write(json_object)


class CRUD:
    def __init__(self):
        self.filename = "data.json"

    def Populate_Database(self):
        data = json.load(open(self.filename))
        for entry in data:
            _deal_id = entry.get("dealID")
            _game_id = entry.get("gameID")
            _title = entry.get("title")
            _sale_price = entry.get("salePrice")
            _normal_price = entry.get("normalPrice")
            _on_sale = entry.get("isOnSale")
            _savings = entry.get("savings")
            _metacritic_score = entry.get("metacriticScore")
            _steam_rating_text = entry.get("steamRatingText")
            _steam_rating_percent = entry.get("steamRatingPercent")
            _steam_rating_count = entry.get("steamRatingCount")
            _release_date = entry.get("releaseDate")

            existing_games_1 = Deals.query.filter_by(ID=_game_id).first()
            if not existing_games_1:
                db.session.add(Deals(
                    ID=int(_game_id),
                    title=str(_title),
                    deal_id=str(_deal_id),
                    sale_price=float(_sale_price),
                    normal_price=float(_normal_price),
                    on_sale=bool(_on_sale),
                    savings=float(_savings)
                ))

            existing_games_2 = Games.query.filter_by(ID=_game_id).first()
            if not existing_games_2:
                db.session.add(Games(
                    ID=int(_game_id),
                    metacritic_score=int(_metacritic_score),
                    steam_rating_text=str(_steam_rating_text),
                    steam_rating_percent=float(_steam_rating_percent),
                    steam_rating_count=int(_steam_rating_count),
                    release_date=str(time.ctime(_release_date))
                ))
        db.session.commit()
