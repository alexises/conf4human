import string
import unittest

from click import Choice
from conforhuman.configuration import Field
from conforhuman.validator.literal import Min
from conforhuman.ast import LocalizableLiteral, FilePosition
import logging
from typing import Union

logger = logging.getLogger(__name__)

class TestConfiguration(unittest.TestCase):
    def _init_literal(self, size: Union[int, float, str]) -> LocalizableLiteral:
        beg = FilePosition(0, 0, None)
        end = FilePosition(0, 0, None)

        return LocalizableLiteral(beg, end, size)

    def test_field(self):
        l1 = self._init_literal(43)
        l2 = self._init_literal(41)

        a = Field("foo", required=True)
        a.add_validator(Min(42))
        self.assertTrue(a.validate(l1) == [])
        self.assertFalse(a.validate(l2) == [])

        a.serialize(l1)
        self.assertTrue(a.get() == 43)
        a.serialize(l2)
        self.assertTrue(a.get() == 41)


    