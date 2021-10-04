import unittest
from conforhuman.parser import YamlParser 
import logging

logger = logging.getLogger(__name__)

class TestYaml(unittest.TestCase):
    def _compareString(self, string_data, result_obj):
        parser = YamlParser()
        out = parser.parse_string(string_data)
        logger.debug('%s', out)
        out_obj = out.serialize()
        logger.debug('%s == %s', out_obj, result_obj)
        self.assertTrue(out_obj == result_obj)

    def test_literals(self):
        self._compareString("42", 42)
        self._compareString("-42", -42)
        self._compareString("foo", "foo")
        self._compareString("'bar'", "bar")
        self._compareString('"foobar"', "foobar")
        self._compareString("3.1415", 3.1415)
        self._compareString("-3.1415", -3.1415)
        self._compareString("true", True)
        self._compareString("false", False)
        self._compareString("null", None)
        self._compareString(r'"\0"', "\0")

    def test_array(self):
        self._compareString(r'[]', [])
        self._compareString(r'["foo"]', ["foo"])
        self._compareString(r'[32]', [32])
        self._compareString(r'[32, "bar"]', [32, "bar"])


if __name__ == '__main__':
    unittest.main()
