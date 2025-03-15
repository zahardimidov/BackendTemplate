from collections import namedtuple
from typing import ClassVar, Self, get_type_hints

from pydantic import BaseModel, ConfigDict


def get_cls_fields_type(cls: BaseModel):
    annotations = get_type_hints(cls)

    data = {k: v.annotation for k, v in cls.model_fields.items()}

    for k, v in annotations.items():
        if v.__dict__.get("_name") == "Optional":
            class_ = v.__dict__.get("__args__", [str])[0]
        else:
            class_ = v
        data[k] = class_

    return namedtuple("fields", data.keys())(**data)


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fields: ClassVar[Self]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        _fields = get_cls_fields_type(cls)
        setattr(cls, "fields", _fields)  # noqa: B010


class ResponseModel(BaseModel):
    ...
