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


class DBStorage:
    """ Stores objects of the AirBnB_clone system in a database """
    __engine = None
    __session = None

    def __init__(self):
        """ Creates a database connection """
        self.__engine = create_engine(url, pool_pre_ping=True, echo=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns all objects of a given class or objects of all classes """
        cls_obj = []
        clsname = {
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User,
        }
        if cls == None:
            for cls_name in clsname:
                print(clsname[cls_name])
                query = select(clsname[cls_name])
                print("\n", query, "\n")
                result = self.__session.scalars(query).all()
                cls_obj.extend(result)

        elif cls and cls in clsname:
            query = select(clsname[cls])
            result = self.__session.scalars(query).all()
            cls_obj.extend(result)
        
        self.__session.close()
        objects = {}
        for obj in cls_obj:
            key = f"{cls}.{obj.id}"
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
            self.__session.close()

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
        
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        scoped_sess = scoped_session(Session)
        self.__session = scoped_sess()



        # Session = sessionmaker()
        # self.__session = Session(bind=self.__engine)
        
        # if cls:
        #     cls_obj = self.__session.query(cls).all()
        # else:
        #     for cls in Base.registry._class_registry.values():
        #         if hasattr(cls, '__table__'):
        #             all_objects = self.__session.query(cls.__name__).all()

if __name__ == "__main__":
    storage = DBStorage()
    storage.reload()