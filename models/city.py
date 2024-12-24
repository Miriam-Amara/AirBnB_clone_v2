#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state_id: Mapped[str] = mapped_column(
                                String(60), ForeignKey("states.id"),
                                nullable=False, index=True
                                )
    places: Mapped["Place"] = relationship(backref="cities", cascade="all, delete-orphan")
