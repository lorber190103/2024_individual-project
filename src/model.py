from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Deals(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    deal_id: Mapped[int] = mapped_column(nullable=False)
    sale_price: Mapped[float] = mapped_column(nullable=False)
    normal_price: Mapped[float] = mapped_column(nullable=False)
    on_sale: Mapped[bool] = mapped_column(nullable=False)
    savings: Mapped[float] = mapped_column(nullable=False)
