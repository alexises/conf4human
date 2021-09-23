import unittest
from conforhuman.parser import YamlParser 

class TestYaml(unittest.TestCase):
    def _compareString(self, string_data, result_object):
        parser = YamlParser()
        out = parser.parse_string(string_data)
        outObj = out.serialize()
        self.assertTrue(outObj == result_obj)

    def test_literals(self):
        self._compareString("42", 42)
        seff._compareString("foo", "foo")
        self._compareString("'bar'", "bar")
        self._compareString('"foobar"', "foobar")
        self._compareString("3.1415", 3.1415)
        self._compareString("true", True)
        self._compareString("false", False)
        self._compareString("null", None)
        self._compareString(r'"\0"', "\0")


if __name__ == '__main__':
    unittest.main()
