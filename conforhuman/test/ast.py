import unittest
from conforhuman.parser import YamlParser 
import logging

logger = logging.getLogger(__name__)

class TestAst(unittest.TestCase):
    def _getObject(self, string_data):
        parser = YamlParser()
        out = parser.parse_string(string_data)
        return out 

    def test_literal(self):
        a = self._getObject('42')
        b = self._getObject("-42")
        c = self._getObject("foo")
        d = self._getObject("'bar'")
        e = self._getObject('"foobar"')
        f = self._getObject("3.1415")
        g = self._getObject("-3.1415")
        h = self._getObject("true")
        i = self._getObject("false")
        j = self._getObject("null")
        k = self._getObject(r'"\0"')

        self.assertTrue(a.getStartPosition().line == 0)
        self.assertTrue(a.getStartPosition().column == 0)
        self.assertTrue(a.getEndPosition().line == 0)
        self.assertTrue(a.getEndPosition().column == 2)

        self.assertTrue(b.getStartPosition().line == 0)
        self.assertTrue(b.getStartPosition().column == 0)
        self.assertTrue(b.getEndPosition().line == 0)
        self.assertTrue(b.getEndPosition().column == 3)

        self.assertTrue(c.getStartPosition().line == 0)
        self.assertTrue(c.getStartPosition().column == 0)
        self.assertTrue(c.getEndPosition().line == 0)
        self.assertTrue(c.getEndPosition().column == 3)
        
        self.assertTrue(d.getStartPosition().line == 0)
        self.assertTrue(d.getStartPosition().column == 0)
        self.assertTrue(d.getEndPosition().line == 0)
        self.assertTrue(d.getEndPosition().column == 5)

        self.assertTrue(e.getStartPosition().line == 0)
        self.assertTrue(e.getStartPosition().column == 0)
        self.assertTrue(e.getEndPosition().line == 0)
        self.assertTrue(e.getEndPosition().column == 8)

        self.assertTrue(f.getStartPosition().line == 0)
        self.assertTrue(f.getStartPosition().column == 0)
        self.assertTrue(f.getEndPosition().line == 0)
        self.assertTrue(f.getEndPosition().column == 6)

        self.assertTrue(g.getStartPosition().line == 0)
        self.assertTrue(g.getStartPosition().column == 0)
        self.assertTrue(g.getEndPosition().line == 0)
        self.assertTrue(g.getEndPosition().column == 7)

        self.assertTrue(h.getStartPosition().line == 0)
        self.assertTrue(h.getStartPosition().column == 0)
        self.assertTrue(h.getEndPosition().line == 0)
        self.assertTrue(h.getEndPosition().column == 4)

        self.assertTrue(i.getStartPosition().line == 0)
        self.assertTrue(i.getStartPosition().column == 0)
        self.assertTrue(i.getEndPosition().line == 0)
        self.assertTrue(i.getEndPosition().column == 5)

        self.assertTrue(j.getStartPosition().line == 0)
        self.assertTrue(j.getStartPosition().column == 0)
        self.assertTrue(j.getEndPosition().line == 0)
        self.assertTrue(j.getEndPosition().column == 4)

        self.assertTrue(k.getStartPosition().line == 0)
        self.assertTrue(k.getStartPosition().column == 0)
        self.assertTrue(k.getEndPosition().line == 0)
        self.assertTrue(k.getEndPosition().column == 4)

