import datetime
import json
from enum import Enum
import copy

import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import IntegrityError, DataError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy import inspect
import collections

db = SQLAlchemy()


class SharedModel(db.Model):
    """`SharedModel` is a common subclass of `db.model` which provides common required fields and shared functionality
    that is needed in all model classes """

    __abstract__ = True

    # Hooks for on_create and on_update
    # https://stackoverflow.com/questions/4309607/whats-the-preferred-way-to-implement-a-hook-or-callback-in-python
    # Since this is a shared class, the hooks are registered in a dictionary on the form {'class_name': [...hooks]},
    # because all sub-classes of this class will have access to all hooks.
    _on_create = {}
    _on_update = {}

    @classmethod
    def on_create(cls, func):
        class_name = cls.__name__
        if cls._on_create.get(class_name) is None:
            cls._on_create[class_name] = []

        cls._on_create[class_name].append(func)

    @classmethod
    def _execute_on_create(cls, instance):
        class_name = cls.__name__
        for func in cls._on_create.get(class_name, []):
            func(instance)

    @classmethod
    def on_update(cls, func):
        class_name = cls.__name__
        if cls._on_update.get(class_name) is None:
            cls._on_update[class_name] = []

        cls._on_update[class_name].append(func)

    @classmethod
    def _execute_on_update(cls, instance, previous_state=None):
        class_name = cls.__name__
        for func in cls._on_update.get(class_name, []):
            func(instance, previous_state)

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    modified = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())

    excluded_fields = set()

    def __repr__(self):
        """
        Return string description of model object instance
        :return: str
        """
        format_string = "{class_name} {identifier}"
        class_name = self.__class__.__name__
        try:
            identifier = self.name
        except AttributeError:
            identifier = self.id

        return format_string.format(class_name=class_name, identifier=identifier)

    def to_dict(self):
        """Return dict containing the keys and values of all property columns, and the keys and identifiers of
        all N-1 or 1-1 relationships for the current model object instance"""
        orm_descriptors = inspect(type(self)).all_orm_descriptors
        excluded_fields_keys = [excluded_field.key for excluded_field in self.excluded_fields]

        modified_descriptors = []
        for key, value in orm_descriptors.items():
            # In the return value from `all_orm_descriptors` we get a `Mapper` instance which we ignore
            if type(value) is sqlalchemy.orm.Mapper:
                continue

            if key in excluded_fields_keys:
                continue

            try:
                # Will return either `ColumnProperty` or `RelationshipProperty`
                property_type = type(value.property)
            except AttributeError as e:
                err = e

                # Hybrid properties does not have a `property value`.
                # Let's ensure we are dealing with a Hybrid property
                if type(value) is hybrid_property:
                    property_type = hybrid_property

                # If not, something have gone wrong, so let's throw the original exception:
                else:
                    raise err from None
            modified_descriptors.append((key, property_type))

        return_dict = {}

        for (key, property_type) in modified_descriptors:
            try:
                value = getattr(self, key)
                if isinstance(value, collections.Iterable) and property_type is RelationshipProperty:
                    # We will only return N-1 or 1-1 relationships
                    continue

                if property_type is RelationshipProperty:
                    # We will return the ID of the foreign key
                    value = value.id

                # Return the 'value' for Enums
                if isinstance(value, Enum):
                    value = value.value

                # Return ISO-strings for datetimes
                if isinstance(value, (datetime.datetime, datetime.date)):
                    value = value.isoformat()

            except AttributeError:
                value = None
            return_dict[key] = value
        return return_dict

    def to_json(self, sort_keys=False):
        """
        Return a JSON representation of `to_dict()`. The output is indented (pretty-printed) and will serialize complex
        attributes.
        :param sort_keys:
        :return: str
        """
        def converter(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            error_message = "No converter implemented for type '{0}'".format(type(obj))
            raise TypeError(error_message)

        return json.dumps(self.to_dict(), indent=True, default=converter, sort_keys=sort_keys)

    @classmethod
    def add(cls, **kwargs):

        instance = cls(**kwargs)
        db.session.add(instance)
        try:
            db.session.commit()
        except (IntegrityError, DataError) as e:
            # Session should rollback
            db.session.rollback()
            raise e

        # Execute hooks
        cls._execute_on_create(instance)

        return instance

    @classmethod
    def update(cls, instance_id, **kwargs):
        instance = db.session.query(cls).get(instance_id)
        instance_copy = copy.copy(instance)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        try:
            db.session.commit()
        except (IntegrityError, DataError) as e:
            # Session should rollback
            db.session.rollback()
            raise e

        # Execute hooks
        cls._execute_on_update(instance, instance_copy)

        return instance

    @classmethod
    def delete(cls, instance_id):
        instance = db.session.query(cls).get(instance_id)
        if not instance:
            raise ValueError("No instance of {class_name} with ID: {instance_id}".format(
                class_name=cls.__name__, instance_id=instance_id))

        db.session.delete(instance)
        try:
            db.session.commit()
        except DataError:
            db.session.rollback()

        return instance_id

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
