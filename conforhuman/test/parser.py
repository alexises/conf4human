import unittest
from conforhuman.parser import YamlParser 
import logging

logger = logging.getLogger(__name__)

class TestYaml(unittest.TestCase):
    def _compareString(self, string_data, result_obj):
        parser = YamlParser()
        out = parser.parse_string(string_data)
        logger.debug('out : %s', out)
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

    def test_dict(self):
        self._compareString(r'{}', {})
        self._compareString(r'{"foo":foo}', {"foo": "foo"})
        self._compareString(r'{"bar":42}', {"bar": 42})
        self._compareString(r'{"test":"foo","test2":42}', {"test": "foo", "test2": 42})

    def test_inlined_list(self):
        a = " - foo"
        b = """
        - foo
        - bar"""
        self._compareString(a, ["foo"])
        self._compareString(b, ["foo", "bar"])

    def test_inlined_dict(self):
        a = 'foo: "bar"'
        b = """
        foo: bar
        bar: 42"""
        self._compareString(a, {"foo": "bar"})
        self._compareString(b, {"foo": "bar", "bar": 42})

    def test_recursive_list(self):
        a = """
        - foo
        - 
          - bar
          - foobar
          -
            - barfoo
        """
        b = """
        - a
        - 
          - b
          -
            - c
          - d
        - e
        """
        c = """
        - a
        - - b
          - - c
          - d
        - e
        """
        self._compareString(a, ["foo", ["bar", "foobar", ["barfoo"]]])
        self._compareString(b, ["a", ['b', ['c'], 'd'],"e"])
        self._compareString(c, ["a", ['b', ['c'], 'd'],"e"])

    # def test_recursive_dict(self):
    #     a = """
    #       foo:
    #         bar: 42
    #         foobar:
    #           barfoo: 43
    #     """
    #     b = """
    #        a: a
    #        b:
    #           c: c
    #           d: 
    #             e: e
    #           f: f
    #        g: g
    #     """
    #     self._compareString(a, {"foo": {"bar": 42, "foobar": {"barfoo": 43}}})
    #     self._compareString(b, {
    #         "a": "a", 
    #         "b": {
    #             "c": "c", 
    #             "d": {
    #                 "e": "e"
    #             },
    #             "f": "f"
    #         },
    #         "g": "g"
    #     })

    # def test_inline_mix(self):
    #     a = """
    #     a: {}
    #     b: []
    #     c: 
    #       - d: []
    #       - e: { "f": "f", "g": "g"}
    #       - h: [ 10, 3.1415, "foo"]
    #     """
    #     self._compareString(a, {
    #         "a": {}, 
    #         "b": [], 
    #         "c": [
    #             {"d": []}, 
    #             {"e": {
    #                 "f": "f", 
    #                 "g": "g"
    #                 }
    #             }, 
    #             {'h': [10, 3.1415, "foo"]} 
    #        ]})

    # def test_list_of_dict(self):
    #     a = """
    #     - 
    #       a: 10
    #       b: 20
    #       c: 30
    #     - 
    #       a: 40
    #       b: 50
    #       c: 60
    #     - 
    #       d: 70
    #     """
    #     b = """
    #     - a: 10
    #       b: 20
    #       c: 30
    #     - a: 40
    #       b: 50
    #       c: 60
    #     - d: 70
    #     """
    #     self._compareString(a, [
    #         {"a": 10, "b": 20, "c": 30},
    #         {"a": 40, "b": 50, "c": 60},
    #         {"d": 70}
    #     ])
    #     self._compareString(b, [
    #         {"a": 10, "b": 20, "c": 30},
    #         {"a": 40, "b": 50, "c": 60},
    #         {"d": 70}
    #     ])
        
if __name__ == '__main__':
    unittest.main()
