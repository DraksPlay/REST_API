from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Integer,
    ForeignKey,
    String,
    DateTime,
    Text
    )
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_book = relationship("UserBook", cascade="all, delete", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))

    user_book = relationship("UserBook", cascade="all, delete", back_populates="book")


class UserBook(Base):
    __tablename__ = "user_books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    friend_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_book")
    book = relationship("Book", back_populates="user_book")
