#!/usr/bin/python3
import json
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns a dictionary of all objects stored
        in the file(file.json) as key,
        value pairs.
        """
        return FileStorage.__objects

    def reload(self):
        try:
            with open(FileStorage.__file_path, mode="r", encoding="utf-8") as f:
                FileStorage.__objects = json.load(f)
                for key, value in FileStorage.__objects.items():
                    cls_name = value['__class__']
                    cls = self.classes()[cls_name]
                    FileStorage.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass

    def classes(self):
        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Place': Place,
            'Amenity': Amenity,
            'Review': Review
        }
        return classes


# Test the reload method
storage = FileStorage()
storage.reload()
print(storage.all())  # Print all loaded objects
