#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base, Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    places: Mapped["Place"] = relationship(backref="user", cascade="all, delete-orphan")
    reviews: Mapped["Review"] = relationship(backref="user", cascade="all, delete-orphan")