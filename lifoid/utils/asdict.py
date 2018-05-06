"""
Serialization of object into dict
"""
from collections import OrderedDict


def namedtuple_asdict(obj):
    """
    Serializing a nested namedtuple into a Python dict
    """
    if obj is None:
        return obj
    if hasattr(obj, "_asdict"):  # detect namedtuple
        return OrderedDict(zip(obj._fields, (namedtuple_asdict(item)
                                             for item in obj)))
    if isinstance(obj, str):  # iterables - strings
        return obj
    if hasattr(obj, "keys"):  # iterables - mapping
        return OrderedDict(zip(obj.keys(), (namedtuple_asdict(item)
                                            for item in obj.values())))
    if hasattr(obj, "__iter__"):  # iterables - sequence
        return type(obj)((namedtuple_asdict(item) for item in obj))
    # non-iterable cannot contain namedtuples
    return obj