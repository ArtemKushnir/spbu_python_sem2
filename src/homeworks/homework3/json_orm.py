from dataclasses import asdict, dataclass
from json import dumps
from typing import Any, Type, TypeVar, get_args

T = TypeVar("T", bound="ORM")


class JsonAttributeError(Exception):
    pass


class JsonError(Exception):
    pass


def parse_json_dict_args(instance: T, name: str) -> Any:
    if not hasattr(instance, "json_dict"):
        raise JsonError("instance and json dict are not bound")
    json_dict = instance.json_dict
    json_value = json_dict.get(name, None)
    if json_value is None:
        raise JsonAttributeError(f"json dict doesnt have {name}")
    elif isinstance(json_value, list) and len(json_value) == 1 and isinstance(json_value[0], dict):
        return instance.__annotations__[name].bind_lazy_dict(json_value[0])
    elif isinstance(json_value, list):
        result = []
        for arg in json_value:
            if isinstance(arg, dict):
                result.append(get_args(instance.__annotations__[name])[0].bind_lazy_dict(arg))
            else:
                result.append(arg)
        return result
    elif isinstance(json_value, dict):
        annotations = instance.__annotations__
        if name in annotations:
            return annotations[name].bind_lazy_dict(json_value)
    return json_value


class Descriptor:
    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, instance: T, owner: Type[T]) -> Any:
        if instance is None:
            return self
        value = instance.__dict__[self.name]
        if value is not None:
            return value
        new_value = parse_json_dict_args(instance, self.name)
        instance.__dict__[self.name] = new_value
        return new_value

    def __set__(self, instance: T, value: Any) -> None:
        instance.__dict__[self.name] = value


@dataclass
class ORM:
    @classmethod
    def bind_lazy_dict(cls: Type[T], json_dict: dict, strict: bool = False) -> T:
        if strict:
            if set(json_dict.keys()) != set(cls.__annotations__.keys()):
                raise JsonError("dataclass does not match the json")
        for key in cls.__annotations__.keys():
            setattr(cls, key, Descriptor(key))
        args = len(cls.__annotations__) * [None]
        instance = cls(*args)
        instance.__dict__["json_dict"] = json_dict
        return instance

    def dump(self) -> str:
        return dumps(asdict(self))
