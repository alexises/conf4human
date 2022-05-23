from http.client import NON_AUTHORITATIVE_INFORMATION
import string
from typing import Union
from conforhuman.validator.interface import ValidatorInterface
from conforhuman.ast import LocalizableList, LocalizableLiteral, LocalizableOrderedDict
from conforhuman.ast import FilePosition

class ConfigError(object):
    def __init__(self, msg: string, beg: FilePosition, end: Union[FilePosition, None] = None) -> None:
        self.msg = msg
        self.beg : FilePosition = beg
        self.end : FilePosition = end
    
    def __str__(self) -> str:
        out = f"{self.beg.filename} {self.beg.line}:{self.beg.column}"
        if self.end:
            out += f" to {self.end.line}:{self.end.column}"
        out += f" {self.msg}"
        return out 

class Field(object):
    def __init__(self, name: str, required: bool = True, default = None):
        self._validator : list[ValidatorInterface] = []
        self._name = name
        self._required = required
        self._default = default
        self._value = None
        self._serialized = False

    def get(self):
        return self._value

    def get_name(self) -> str:
        return self._name

    def get_default(self):
        return self._default
    
    def add_validator(self, validator: ValidatorInterface) -> None:
        self._validator.append(validator) 

    def serialize(self, attr: LocalizableLiteral) -> None:
        self._value = attr.serialize()
        self._serialized = True

    def validate(self, attr: LocalizableLiteral) -> list[str]:
        validation_errors = []
        for validator in self._validator:
            if not validator.validate(attr):
                validation_errors.append(validator.getError(attr))

        return validation_errors

class ListField(Field):
    def validate(self, attr: LocalizableList):
        validation_error = []
        for item in attr:
            for validator in self._validator:
                if not validator.validate(attr):
                    validation_error.append(validator.getError(attr))

        return validation_error

    def serialize(self, attr: LocalizableList) -> None:
        self._value = attr.serialize()
        self._serialized = True

class ConfigurationObject(object):
    def __init__(self):
        self._attributes : dict[str, Field] = {}
        self._errors = []
    
    def _introspect(self):
        for key, value in self._attributes.__dict__.items():
            if isinstance(value, Field):
                self._attributes[key] = value

    def validate(self, attr: LocalizableOrderedDict):
        self._introspect()

        for key, val in self._attributes.items():
            error = val.validate(attr)
            if len(error) > 0:
                self._errors += error

        return self._errors

    def serialize(self, attr: LocalizableOrderedDict):
        for key, val in self._attributes.items():
            name = val.get_name()
            default = val.get_default()
            value = attr.get(name, default)
            val.serialize(value)
            
class SubConfigFIeld(Field):
    def __init__(self, subObj: ConfigurationObject, name: str, required: bool = True, default=None):
        super().__init__(name, required, default)

        self.subObj = subObj

    def validate(self, attr: LocalizableOrderedDict):
        return self.subObj.validate()

    def serialize(self, attr: LocalizableLiteral) -> None:
        ret = self.subObj.serialize()
        self._serialized = True
        return ret
        