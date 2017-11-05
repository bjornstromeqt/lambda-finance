
from enum import Enum

from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.query import Query

from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene.relay.connection import PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice


RELAY_ARGUMENTS = ['first', 'last', 'before', 'after']


class FilterableSQLAlchemyConnectionField(SQLAlchemyConnectionField):
    """
    This subclass offers the functionality to add arbitrary arguments to filter results from connections.

    Some inspiration: https://github.com/graphql-python/graphene-sqlalchemy/issues/27
    """

    @classmethod
    def get_query(cls, model, info, **args):
        # Get base-query from the Super-class
        query = super(FilterableSQLAlchemyConnectionField, cls).get_query(model, info, **args)

        # Add all keyword-arguments as filter to the query, except relay-arguments
        for field, value in args.items():
            if field not in RELAY_ARGUMENTS:
                query = query.filter(getattr(model, field) == value)
        return query

    @classmethod
    def connection_resolver(cls, resolver, connection, model, root, info, **args):
        iterable = resolver(root, info, **args)
        if iterable is None:
            iterable = cls.get_query(model, info, **args)
        else:
            # Query is already executed, filter the result on the keyword-arguments
            for keyword, value in args.items():
                if keyword not in RELAY_ARGUMENTS:
                    iterable = filter(lambda row: _filter_iterable(keyword, value, row), iterable)

            # Convert back to the original type of the 'iterable'-variable
            iterable = InstrumentedList(iterable)

        # From here on it is the same as SQLAlchemyConnectionField :)
        if isinstance(iterable, Query):
            _len = iterable.count()
        else:
            _len = len(iterable)
        return connection_from_list_slice(
            iterable,
            args,
            slice_start=0,
            list_length=_len,
            list_slice_length=_len,
            connection_type=connection,
            pageinfo_type=PageInfo,
            edge_type=connection.Edge,
        )


def _filter_iterable(key, value, item) -> bool:
    """
    Helper function to filter items.

    Returns True if the 'item.key' equals 'value', otherwise False.

    :param key: The key to look for
    :param value: The value to match against
    :param item: SQLAlchemy object (instance)
    :return: bool
    """

    item_value = getattr(item, key)

    # If the value is of type 'Enum', match the Enum.value.
    if isinstance(item_value, Enum):
        return item_value.value == value

    # Todo: Add support for dates (maybe?)

    # Compare values
    return item_value == value
