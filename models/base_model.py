#!/usr/bin/python3
""" This model defines all common attributes/methods for other classes """
import uuid
import datetime
from models import storage


class BaseModel:
    """ Class BaseModel """
    def __init__(self, *args, **kwargs):
        """ initializing """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.created_at = str(datetime.datetime.now())
                    self.updated_at = self.created_at
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """ string representation """
        return f'[{self.__class__.__name__}] {self.id} {self.__dict__}'

    def save(self):
        """ saves """
        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
        """ converts to dictionary """
        self.created_at = str(datetime.datetime.now().isoformat())
        self.updated_at = str(self.created_at)
        my_dict = self.__dict__
        my_dict["__class__"] = self.__class__.__name__
        return my_dict
