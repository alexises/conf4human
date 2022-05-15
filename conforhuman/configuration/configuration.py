from conforhuman.validator.interface import ValidatorInterface

class Field(object):
    def __init__(self):
        self._validator = []
    
    def add_validator(self, validator: ValidatorInterface) -> None:
        self._validator.append(validator) 

    def validate(self):
        validation_status = []
        for i in self._validator:
            validation_status.append(i.validate())

        if False in validation_status:
            return False
        return True

class ConfigurationObject(object):
    def __init__(self):
        self._attributes = {}
    
    def _introspect(self):
        for key, value in self._attributes.__dict__.items():
            if isinstance(value, Field):
                self._attributes[key] = value

    def validate(self):
        attr_state = []
        for key, val in self._attributes.items():
            attr_state.append(val.validate())
            

        