#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    cities: Mapped["City"] = relationship(backref="state", cascade='all, delete-orphan')
    __cities = []

    @property
    def cities(self):
        """ """
        from models import storage
        
        city_obj = list(storage.all("City").values())
        for obj in city_obj:
            if self.id == obj.state_id:
                State.__cities.append(obj)
        return self.__cities
