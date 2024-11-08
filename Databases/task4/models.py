from datetime import date
from decimal import Decimal

from db import Base, engine
from sqlalchemy import DECIMAL, CheckConstraint, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_author: Mapped[str] = mapped_column(nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Genre(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_genre: Mapped[str] = mapped_column(nullable=False)

    books: Mapped[list["Genre"]] = relationship("Genre", back_populates="genre")


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.author_id", ondelete="CASCADE"), nullable=False
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.genre_id", ondelete="CASCADE"), nullable=False
    )
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    amount: Mapped[int] = mapped_column(
        Integer, CheckConstraint("amount >= 0"), nullable=False
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    buy_books: Mapped[list["BuyBook"]] = relationship("BuyBook", back_populates="book")


class City(Base):
    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_city: Mapped[str] = mapped_column(nullable=False)
    days_delivery: Mapped[int] = mapped_column(nullable=False)

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="city")


class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_client: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.city_id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(nullable=False)

    city: Mapped["City"] = relationship("City", back_populates="clients")
    buys: Mapped[list["Buy"]] = relationship("Buy", back_populates="client")


class Buy(Base):
    __tablename__ = "buys"

    buy_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    buy_description: Mapped[str] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.client_id", ondelete="CASCADE"), nullable=False
    )

    client: Mapped["Client"] = relationship("Client", back_populates="buys")
    buy_books: Mapped[list["BuyBook"]] = relationship("BuyBook", back_populates="buy")
    buy_steps: Mapped[list["BuyStep"]] = relationship("BuyStep", back_populates="buy")


class BuyBook(Base):
    __tablename__ = "buy_books"

    buy_book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buys.buy_id", ondelete="CASCADE"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, CheckConstraint("amount >= 0"), nullable=False
    )

    buy: Mapped["Buy"] = relationship("Buy", back_populates="buy_books")
    book: Mapped["Book"] = relationship("Book", back_populates="buy_books")


class Step(Base):
    __tablename__ = "steps"

    step_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_step: Mapped[str] = mapped_column(nullable=False)

    buy_steps: Mapped[list["BuyStep"]] = relationship("BuyStep", back_populates="buy")


class BuyStep(Base):
    __tablename__ = "buy_steps"

    buy_step_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buys.buy_id", ondelete="CASCADE"), nullable=False
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey("steps.step_id", ondelete="CASCADE"), nullable=False
    )
    date_step_beg: Mapped[date] = mapped_column(Date, nullable=False)
    date_step_end: Mapped[date] = mapped_column(Date, nullable=False)

    buy: Mapped["Buy"] = relationship("Buy", back_populates="buy_steps")
    step: Mapped["Step"] = relationship("Step", back_populates="buy_steps")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
