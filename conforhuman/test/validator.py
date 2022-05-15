import string
import unittest

from click import Choice
from conforhuman.validator.literal import Max, Min, FixedChoice
from conforhuman.ast import LocalizableLiteral, FilePosition
import logging
from typing import Union

logger = logging.getLogger(__name__)

class TestValidator(unittest.TestCase):
    def _init_literal(self, size: Union[int, float, str]) -> LocalizableLiteral:
        beg = FilePosition(0, 0, None)
        end = FilePosition(0, 0, None)

        return LocalizableLiteral(beg, end, size)

    def test_min(self):
        min1 = Min(1)
        min2 = Min(2)
        min3 = Min(3)
        minPi = Min(3.14)

        a = self._init_literal(0)
        b = self._init_literal(1)
        c = self._init_literal(3)
        d = self._init_literal(4)
        e = self._init_literal(3.13)
        f = self._init_literal(3.15)
        g = self._init_literal(3.14)
        
        self.assertFalse(min1.validate(a))
        self.assertTrue(min1.validate(b))
        self.assertTrue(min1.validate(c))
        self.assertTrue(min1.validate(d))
        self.assertTrue(min1.validate(e))
        self.assertTrue(min1.validate(f))
        self.assertTrue(min1.validate(g))

        self.assertFalse(min2.validate(a))
        self.assertFalse(min2.validate(b))
        self.assertTrue(min2.validate(c))
        self.assertTrue(min2.validate(d))
        self.assertTrue(min2.validate(e))
        self.assertTrue(min2.validate(f))
        self.assertTrue(min2.validate(g))

        self.assertFalse(min3.validate(a))
        self.assertFalse(min3.validate(b))
        self.assertTrue(min3.validate(c))
        self.assertTrue(min3.validate(d))
        self.assertTrue(min3.validate(e))
        self.assertTrue(min3.validate(f))
        self.assertTrue(min3.validate(g))

        self.assertFalse(minPi.validate(a))
        self.assertFalse(minPi.validate(b))
        self.assertFalse(minPi.validate(c))
        self.assertTrue(minPi.validate(d))
        self.assertFalse(minPi.validate(e))
        self.assertTrue(minPi.validate(f))
        self.assertTrue(minPi.validate(g))

    def test_max(self):
        max1 = Max(1)
        max2 = Max(2)
        max3 = Max(3)
        minPi = Max(3.14)

        a = self._init_literal(0)
        b = self._init_literal(1)
        c = self._init_literal(3)
        d = self._init_literal(4)
        e = self._init_literal(3.13)
        f = self._init_literal(3.15)
        g = self._init_literal(3.14)
        
        self.assertTrue(max1.validate(a))
        self.assertTrue(max1.validate(b))
        self.assertFalse(max1.validate(c))
        self.assertFalse(max1.validate(d))
        self.assertFalse(max1.validate(e))
        self.assertFalse(max1.validate(f))
        self.assertFalse(max1.validate(g))

        self.assertTrue(max2.validate(a))
        self.assertTrue(max2.validate(b))
        self.assertFalse(max2.validate(c))
        self.assertFalse(max2.validate(d))
        self.assertFalse(max2.validate(e))
        self.assertFalse(max2.validate(f))
        self.assertFalse(max2.validate(g))

        self.assertTrue(max3.validate(a))
        self.assertTrue(max3.validate(b))
        self.assertTrue(max3.validate(c))
        self.assertFalse(max3.validate(d))
        self.assertFalse(max3.validate(e))
        self.assertFalse(max3.validate(f))
        self.assertFalse(max3.validate(g))

        self.assertTrue(minPi.validate(a))
        self.assertTrue(minPi.validate(b))
        self.assertTrue(minPi.validate(c))
        self.assertFalse(minPi.validate(d))
        self.assertTrue(minPi.validate(e))
        self.assertFalse(minPi.validate(f))
        self.assertTrue(minPi.validate(g))

    def test_choice(self):
        choice1 = FixedChoice([1, 3])
        choice2 = FixedChoice([3.14, 3.15])

        a = self._init_literal(0)
        b = self._init_literal(1)
        c = self._init_literal(3)
        d = self._init_literal(4)
        e = self._init_literal(3.13)
        f = self._init_literal(3.15)
        g = self._init_literal(3.14)
        
        self.assertFalse(choice1.validate(a))
        self.assertTrue(choice1.validate(b))
        self.assertTrue(choice1.validate(c))
        self.assertFalse(choice1.validate(d))
        self.assertFalse(choice1.validate(e))
        self.assertFalse(choice1.validate(f))
        self.assertFalse(choice1.validate(g))

        self.assertFalse(choice2.validate(a))
        self.assertFalse(choice2.validate(b))
        self.assertFalse(choice2.validate(c))
        self.assertFalse(choice2.validate(d))
        self.assertFalse(choice2.validate(e))
        self.assertTrue(choice2.validate(f))
        self.assertTrue(choice2.validate(g))