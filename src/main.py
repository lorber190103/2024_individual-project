import json
import time

import requests

from src.model import Deals, Games, Stores, db


class CheapShark:
    def __init__(self):
        self.filename = "data.json"

    def JSON(self, choice, search=""):
        function_dict = {'current_deals': "deals?",
                         'search_for_deals': "deals?title=",
                         'stores': "stores"}

        url = "https://www.cheapshark.com/api/1.0/" + \
              f"{function_dict[choice.lower()]}" + \
              f"{search}"

        get_data = requests.get(url)
        data = get_data.json()
        json_object = json.dumps(data, indent=3)
        with open(self.filename, "w") as out_file:
            out_file.write(json_object)

    def Populate_Database(self, choice):
        data = json.load(open(self.filename))
        if data == []:
            return 500
        else:
            if choice == "current_deals" or choice == "search_for_deals":
                for entry in data:
                    _deal_id = entry.get("dealID")
                    _game_id = entry.get("gameID")
                    _title = entry.get("title")
                    _store_id = entry.get("storeID")
                    _sale_price = entry.get("salePrice")
                    _normal_price = entry.get("normalPrice")
                    _on_sale = entry.get("isOnSale")
                    _savings = entry.get("savings")
                    _metacritic_score = entry.get("metacriticScore")
                    _metacritic_link = entry.get("metacriticLink")
                    _steam_app_id = entry.get("steamAppID")
                    _steam_rating_text = entry.get("steamRatingText")
                    _steam_rating_percent = entry.get("steamRatingPercent")
                    _steam_rating_count = entry.get("steamRatingCount")
                    _release_date = entry.get("releaseDate")
                    _last_change = entry.get("lastChange")

                    existing_deal_id = Deals.query.filter_by(deal_id=_deal_id).first()
                    if not existing_deal_id:
                        db.session.add(Deals(
                            title=str(_title),
                            sale_price=float(_sale_price),
                            store_id=int(_store_id),
                            normal_price=float(_normal_price),
                            on_sale=bool(int(_on_sale)),
                            savings=round(float(_savings), 2),
                            game_id=int(_game_id),
                            deal_id=str(_deal_id),
                            timestamp=int(time.time())
                        ))
                    else:
                        existing_deal_id.title = str(_title)
                        existing_deal_id.sale_price = float(_sale_price)
                        existing_deal_id.store_id = int(_store_id)
                        existing_deal_id.normal_price = float(_normal_price)
                        existing_deal_id.on_sale = bool(int(_on_sale))
                        existing_deal_id.savings = round(float(_savings), 2)
                        existing_deal_id.timestamp = int(time.time())

                    existing_games = Games.query.filter_by(ID=_game_id).first()
                    if not existing_games:
                        db.session.add(Games(
                            ID=int(_game_id),
                            title=str(_title),
                            metacritic_score=int(_metacritic_score),
                            metacritic_link=str(_metacritic_link),
                            steam_app_id=str(_steam_app_id),
                            steam_rating_text=str(_steam_rating_text),
                            steam_rating_percent=int(_steam_rating_percent),
                            steam_rating_count=int(_steam_rating_count),
                            release_date=str(time.ctime(_release_date)),
                            last_change=str(time.ctime(_last_change))
                        ))
                    else:
                        existing_games.title = str(_title)
                        existing_games.metacritic_score = int(_metacritic_score)
                        existing_games.metacritic_link = str(_metacritic_link)
                        existing_games.steam_app_id = str(_steam_app_id)
                        existing_games.steam_rating_text = str(_steam_rating_text)
                        existing_games.steam_rating_percent = int(_steam_rating_percent)
                        existing_games.steam_rating_count = int(_steam_rating_count)
                        existing_games.release_date = str(time.ctime(_release_date))
                        existing_games.last_change = str(time.ctime(_last_change))

            if choice == "stores":
                for entry in data:
                    _store_id = entry.get("storeID")
                    _store_name = entry.get("storeName")
                    _store_is_active = entry.get("isActive")

                    existing_store = Stores.query.filter_by(ID=_store_id).first()
                    if not existing_store:
                        db.session.add(Stores(
                            ID=int(_store_id),
                            store_name=str(_store_name),
                            store_is_active=bool(_store_is_active)
                        ))
                    else:
                        existing_store.store_name = str(_store_name)
                        existing_store.store_is_active = bool(_store_is_active)

            db.session.commit()
