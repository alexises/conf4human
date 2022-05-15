from secrets import choice
from .interface import ValidatorInterface
from conforhuman.ast import LocalizableLiteral
import logging

logger = logging.getLogger(__name__)

class Min(ValidatorInterface):
    def __init__(self, min_value: int):
        '''
            perform validation for a minimum values
            min_value: minimum values of the attribute
        '''
        self.min_value = min_value

    def validate(self, object: LocalizableLiteral) -> bool:
        return object.getValue() >= self.min_value

class Max(ValidatorInterface):
    def __init__(self, max_value: int):
        '''
            perform validation for a maximum values
            max_value: maximum values of the attribute
        '''
        self.max_value = max_value

    def validate(self, object: LocalizableLiteral) -> bool:
        return object.getValue() <= self.max_value

class FixedChoice(ValidatorInterface):
    def __init__(self, choices: list):
        '''
            perform validation against a predefined choice of item
            choice : list of valid item
        '''
        self.choices = choices
    
    def validate(self, object: LocalizableLiteral) -> bool:
        return object.getValue() in self.choices

