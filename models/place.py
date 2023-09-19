#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table("place_amenity", Base.metadata,    Column("place_id",           String(60),           ForeignKey("places.id"),           primary_key=True,           nullable=False),    Column("amenity_id",           String(60),           ForeignKey("amenities.id"),           primary_key=True,           nullable=False))


class Place(BaseModel, Base):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        Base (_type_): _description_

    Returns:
        _type_: _description_
    """
    __tablename__ = "places"
    city_id = Column(String(60),ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0,nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            cascade="all,delete",
            backref=backref("place", cascade="all,delete"),
            passive_deletes=True)

        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities")

    else:
        @property
        def reviews(self):
            """Return list of review instances for file storage
            matching place_id
            """
            from models import storage
            return {k: v for k, v in storage.all().items()   if v.place_id == self.id}

        @property
        def amenities(self):
            """returns list of amenity ids"""
            from models import storage
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """appends amenity id to amenity_ids"""
            # from models import Amenity
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
