#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """
    Handles long term storage of all class instances
    """
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
        }
    """
    CNC - this variable is a dictionary with:
    keys: Class Names
    values: Class type (used for instantiation)
    """
    __file_path = "./dev/file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls:
            objects_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        fname = FileStorage.__file_path
        d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            d[bm_id] = bm_obj.to_json()
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(d, f_io)

    def reload(self):
        """
        Deserializes the JSON file to __objects if file exists, else nothing
        """
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except Exception:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """
        Delete obj from __objects if it’s inside
        """
        try:
            del__objects[obj]
        except Exception:
            return

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves one objects
        """
        obj_dict = {}
        obj = None
        if cls:
            obj_dict = FileStorage.__objects.values()
            for item in obj_dict:
                if item.id == id:
                    obj = item
            return obj

    def count(self, cls=None):
        """
        Counts number of objs of a class in storage
        """
        if cls:
            obj_list = []
            obj_dict = FileStorage.__objects.values()
            for item in obj_dict:
                if type(item).__name__ == cls:
                    obj_list.append(item)
            return len(obj_list)
        else:
            obj_list = []
            for class_name in self.CNC:
                if class_name == 'BaseModel':
                    continue
                obj_class = FileStorage.__objects
                for item in obj_class:
                    obj_list.append(item)
            return len(obj_list)
