#!/usr/bin/python3
"""User Module"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class"""

    name = ""

    def __init__(self, *args, **kwargs):
        """Amenity constructor"""
        super().__init__(*args, **kwargs)
