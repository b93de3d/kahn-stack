from typing import _GenericAlias, List, Dict
from enum import Enum
from datetime import datetime
import requests


def parse_json_value(json_value, item_type):
    print(json_value, item_type)
    if isinstance(item_type, _GenericAlias):
        if item_type._name == "List":
            if len(item_type.__args__) == 1:
                arg = item_type.__args__[0]
                print("ARGGG", arg)
                return [parse_json_value(v, arg) for v in json_value]
    if issubclass(item_type, Enum):
        enum = globals().get(item_type.__name__)
        print("GLOOO", enum)
        assert enum, f"Could not find {item_type.__name__} in {__file__}: {globals().keys()}"
        for v in enum:
            if v.value == json_value:
                return v
        assert False, f"Invalid enum value: {json_value}"
    return json_value

def deserialize_item(data, cls):
    init_args = {}
    for key, item_type in cls.__init__.__annotations__.items():
        init_args[key] = parse_json_value(data[key], item_type)
    return cls(**init_args)

def deserialize_res_data(res_data, cls):
    keys = list(res_data.keys())
    assert len(keys) == 1, f"Unexpected number of keys: {keys}"
    data = res_data[keys[0]]
    if type(data) == list:
        print("Handling list", cls)
        if len(cls.__args__) == 1:
            arg = cls.__args__[0]
            return [deserialize_item(i, arg) for i in data]
        assert False, "Not implemented"
    else:
        print("Handling single item")
        return deserialize_item(data, cls)

def dump_json_value(value, item_type):
    if issubclass(item_type, Enum):
        return value.value
    return value

def serialize_object(obj, cls):
    output = {}
    for key, item_type in cls.__init__.__annotations__.items():
        output[key] = dump_json_value(getattr(obj, key), item_type)
    return output

