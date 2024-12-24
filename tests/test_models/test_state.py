#!/usr/bin/python3
""" This module provides test for State class"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.city import City
from models import storage


class test_state(test_basemodel):
    """ Defines test cases for State class"""

    def __init__(self, *args, **kwargs):
        """ Initializes unittest attributes """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def setUp(self):
        """ """
        self.new_state = State()
        self.city1 = City()
        self.city2 = City()
        self.city3 = City()
        self.city2.__dict__.update({"name": "Texas", "state_id": self.new_state.id})
        self.city3.__dict__.update({"name": "New_York", "state_id": self.new_state.id})

        storage.new(self.new_state)
        storage.new(self.city1)
        storage.new(self.city2)
        storage.new(self.city3)

    # def test_name3(self):
    #     """ """
    #     new = self.value()
    #     self.assertEqual(type(new.name), str)

    def test_name(self):
        """ Tests the type of name class attribute """
        self.new_state.name = "California"
        self.assertEqual(type(self.new_state.name), str)

    def test_cities_getter_method(self):
        """ """
        self.new_state.cities.clear()
        city_list = []

        for key, city_obj in storage.all("City").items():
            if city_obj.state_id == self.new_state.id:
                city_list.append(city_obj)
        self.assertEqual(city_list, self.new_state.cities)
        


        
