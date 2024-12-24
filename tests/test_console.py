#!/usr/bin/python3

"""

"""


import os
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage




def reset_buffer(buffer):
    """
    Clears and resets the provided StringIO buffer.
    """
    buffer.truncate(0)  # clear the buffer
    buffer.seek(0)  # reset position to the beginning.


class TestCreate(unittest.TestCase):
    """
    Unit tests for the 'create' command in the HBNBCommand interpreter.
    """

    def setUp(self):
        """ Set up test environment """
        self.clsname = [
            "BaseModel", "User", "Amenity",
            "City", "Place", "State", "Review",
        ]

        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass
        
    def test_create_with_no_parameter(self):
        """
        Test that 'create <classname>' creates an object of the given class
        """
        with patch("sys.stdout", new=StringIO()) as f:
            for cls in self.clsname:
                HBNBCommand().onecmd(f"create {cls}")
                id = f.getvalue().strip() # removes trailing white spaces
                self.assertIn(f"{cls}.{id}", storage.all().keys())
                reset_buffer(f)

    def test_create_with_parameters(self):
        """
        Test creation of object with given parameters
        e.g create <Class name> <param 1> <param 2> <param 3>...
        """
        with patch("sys.stdout", new=StringIO()) as f:
            for cls in self.clsname:
                HBNBCommand().onecmd(
                    f'create {cls} city_id="0001" user_id="0001" name="My_little_house "'
                    'number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 '
                    'latitude=37.773972 longitude=-122.431297'
                    )
                key, obj = list(storage.all().items())[0]
                self.assertEqual(obj.user_id, "0001")
                del storage._FileStorage__objects[key]

    def test_parameters(self):
        """ Test that an object is created with only valid parameters """
        with patch("sys.stdout", new=StringIO()) as f:
            for cls in self.clsname:
                HBNBCommand().onecmd(
                    f'create {cls} '
                    's1="name" s2="My_little_star" s3="sister\"s_food" ' # valid parameters
                    's4="f11077c5-6992-4d0d-abe9-f41c3085809f" '
                    's5="gui@hbtn.io" s6="" s7="Glo.ria" '
                    's8=hi s9="My little star" s10="sister\"s food" ' # invalid parameters
                    's11="Gl\oria" s12=name "hello" s13="name "hello" '
                    )
                key, obj = list(storage.all().items())[0]
                del storage._FileStorage__objects[key]
                obj_dict = obj.to_dict()

                self.assertIn('s1', obj_dict)
                self.assertIn('s2', obj_dict)
                self.assertIn('s3', obj_dict)
                self.assertIn('s4', obj_dict)
                self.assertIn('s5', obj_dict)
                self.assertIn('s6', obj_dict)
                self.assertIn('s7', obj_dict)

                self.assertNotIn('s8', obj_dict)
                self.assertNotIn('s9', obj_dict)
                self.assertNotIn('s10', obj_dict)
                self.assertNotIn('s11', obj_dict)
                self.assertNotIn('s12', obj_dict)
                self.assertNotIn('s13', obj_dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
