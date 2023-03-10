#!/usr/bin/python3
""" This model serializes instances to a JSON file
and deserializes JSON file to instances """
import json
import os


class FileStorage:
    """ stores the file """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary _objects """
        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        temp_dict = {}
        for key, value in FileStorage.__objects.items():
            temp_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp_dict, f)

    def reload(self):
        """ deserializes the JSON file to __objects """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        dct = {"BaseModel": BaseModel,
               "User": User,
               "State": State,
               "City": City,
               "Amenity": Amenity,
               "Place": Place,
               "Review": Review}
        if os.path.exists(FileStorage.__file_path) is True:
            with open(FileStorage.__file_path, 'r') as f:
                for key, value in json.load(f).items():
                    self.new(dct[value["__class__"]](**value))
