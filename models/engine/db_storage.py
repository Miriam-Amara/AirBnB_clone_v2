#!/usr/bin/python3
"""
This module provides DBStorage class for storing
objects of AirBnB_clone system to a database.
"""

import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, select
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


user = os.getenv("HBNB_MYSQL_USER")
password = os.getenv("HBNB_MYSQL_PWD")
host = os.getenv("HBNB_MYSQL_HOST")
database = os.getenv("HBNB_MYSQL_DB")
url = f"mysql+mysqldb://{user}:{password}@{host}/{database}"



# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class DBStorage:
    """ Stores objects of the AirBnB_clone system in a database """
    __engine = None
    __session = None

    def __init__(self):
        """ Creates a database connection """
        self.__engine = create_engine(url, pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns all objects of the given class or objects of all classes """
        objects = {}
        clsname = {
            Amenity: "Amenity",
            City: "City",
            Place: "Place",
            Review: "Review",
            State: "State",
            User: "User"
        }
        if cls == None:
            for cls in clsname:
                query = select(cls)
                # print("\n", query, "\n")
                cls_objects = self.__session.scalars(query).all()
                for obj in cls_objects:
                    key = f"{clsname[cls]}.{obj.id}"
                    objects[key] = obj

        elif cls in clsname:
            query = select(cls)
            cls_objects = self.__session.scalars(query).all()
            for obj in cls_objects:
                key = f"{clsname[cls]}.{obj.id}"
                objects[key] = obj

        return objects

    def new(self, obj):
        """ Add object to staging area and prepares to save it to database """
        self.__session.add(obj)

    def save(self):
        """ Save object to database """
        try:
            self.__session.commit()
        except Exception as e:
            print(f"Failed to commit: {e}")
            self.__session.rollback()

    def delete(self, obj=None):
        """ Deletes an object from database """
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        """ Creates all tables in the database"""
        try:

            Base.metadata.create_all(self.__engine)
        except Exception as e:
            print(e)
            return
        
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def close(self):
        """ closes the session """
        self.__session.remove()



if __name__ == "__main__":
    storage = DBStorage()
    storage.reload()
