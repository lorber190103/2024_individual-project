from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Stores(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    store_name: Mapped[str] = mapped_column(nullable=False)


class Games(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    metacritic_score: Mapped[int]
    steam_rating_text: Mapped[str]
    steam_rating_percent: Mapped[float]
    steam_rating_count: Mapped[int]
    release_date: Mapped[str]


class Deals(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey(Games.ID), nullable=False)
    deal_id: Mapped[str] = mapped_column(nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey(Stores.ID), nullable=False)
    sale_price: Mapped[float] = mapped_column(nullable=False)
    normal_price: Mapped[float] = mapped_column(nullable=False)
    on_sale: Mapped[bool] = mapped_column(nullable=False)
    savings: Mapped[float] = mapped_column(nullable=False)
