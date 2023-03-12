#!/usr/bin/python3
""" This model inherits from the BaseModel """
from models.base_model import BaseModel


class User(BaseModel):
    """ Defines the User """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
