from datetime import datetime
from graphene.types import Scalar
from graphql.language import ast


class DateType(Scalar):
    """
    Custom DateType.
    Converter between 'date'-object and string in ISO format and 'yyyy-mm-dd'.
    """

    @staticmethod
    def serialize(date):
        """ Converts python 'date'-type to ISO-string ('yyyy-mm-dd') """
        # From database to client

        # Convert date-object to datetime
        # See: https://stackoverflow.com/questions/1937622/convert-date-to-datetime-in-python
        dt = datetime.combine(date, datetime.min.time())
        date_format = "%Y-%m-%d"
        return datetime.strftime(dt, date_format)

    @staticmethod
    def parse_literal(node):
        """ Converts string in ISO date ('yyyy-mm-dd') to Python Date-object """
        # From client to database
        if isinstance(node, ast.StringValue):
            date_format = "%Y-%m-%d"
            try:
                dt = datetime.strptime(node.value, date_format)
            except TypeError as exception:
                raise exception
            return datetime.date(dt)

    @staticmethod
    def parse_value(value):
        # When is this function called?
        return value


class EnumValue(Scalar):
    """
    Custom type EnumValue
    Returns the value of an enum from database.
    Supports Integers, floats and strings

    If a String is passed from client to database, it is converted to uppercase.

    If a non-supported type is fetched, ValueError is raised
    """
    @staticmethod
    def serialize(enum):
        """ Returns the enum-value """
        # From database to client
        if enum.value is None or isinstance(enum.value, (int, str, float)):
            return enum.value
        raise ValueError("Enum value not supported")

    @staticmethod
    def parse_literal(node):
        """ Converts strings to uppercase """
        # From client to database
        if isinstance(node, ast.StringValue):
            if isinstance(node.value, str):
                return node.value.upper()
            return node.value

    @staticmethod
    def parse_value(value):
        return value
