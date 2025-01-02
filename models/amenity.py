#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.place import Place, place_amenity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class Amenity(BaseModel, Base):
    """ Amenity class to store information about the system amenities """
    __tablename__ = "amenities"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    place = relationship("Place", secondary=place_amenity, viewonly=True)
    # place_amenities = relationship("Place", secondary=place_amenity)
    # place_amenities: Mapped[list["Place"]] = relationship(
    #     "Place", secondary=place_amenity, backref="amenity"
    #     )
