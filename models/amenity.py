#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
# from models.place import Place
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class Amenity(BaseModel, Base):
    """ Amenity class to store information about the system amenities """
    __tablename__ = "amenities"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    place_amenity: Mapped[list["Place"]] = relationship(
        secondary="place_amenity", backref="amenity"
        )
