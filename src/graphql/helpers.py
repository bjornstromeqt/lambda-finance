
import graphql_relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from base64 import binascii


def convert_from_global_id(global_id: str, model: SQLAlchemyObjectType.__subclasses__()):
    """
    Convert relay global_id to integer. Checks that the global_id is corresponding to the given model.

    :param global_id:
    :param model:
    :return:
    """
    try:
        (model_name, model_id) = graphql_relay.from_global_id(global_id)
    except (UnicodeDecodeError, binascii.Error):
        raise ValueError("Invalid global_id")

    if not model_name == model.__name__:
        raise TypeError("The given ID represents a '{given}' model but model '{expected}' is required"
                        .format(given=model_name, expected=model.__name__))

    return int(model_id)


def convert_args_from_global_id(args: dict, fields: dict):
    """
    Converts global_id's to integers for a dictionary, where the id's and corresponding models are specified.

    :param args: Initial arguments
    :param fields: key-values where the 'key' is the name of the field and 'value' is the corresponding model
    :return: Updated arguments
    """

    for key, model in fields.items():
        global_id = args.get(key)
        if global_id is None or global_id == '':
            # This might happen when a key that should be converted is optional,
            # meaning that the key-model exists in the fields to be converted but
            # does not exist among the arguments
            continue

        args[key] = convert_from_global_id(global_id, model)

    return args
