#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base

import os
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, ForeignKey, Table, Column



place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), nullable=False, primary_key=True),
    Column("amenity_id", String(60), ForeignKey("amenities.id"), nullable=False, primary_key=True),
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("cities.id"), nullable=False
        )
    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False
        )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    number_rooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    number_bathrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_guest: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price_by_night: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews: Mapped[list["Review"]] = relationship(backref="place", cascade="all, delete-orphan")
        amenities: Mapped[list["Amenity"]] = relationship("Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def reviews(self):
            """ """
            from models import storage
            
            self.__reviews = []
            review_obj = list(storage.all("Review").values())
            for obj in review_obj:
                if self.id == obj.place_id:
                    self.__reviews.append(obj)
            return self.__reviews
        
        @property
        def amenities(self):
            """ """
            return Place.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            from models.amenity import Amenity
            """ Appends the ID of an Amenity object to amenity_id list  """
            if isinstance(obj, Amenity):
                Place.amenity_ids.append(obj.id)
