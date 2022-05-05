import unittest
from conforhuman.test.parser import TestYaml
from conforhuman.test.ast import TestAst
import logging
import sys

if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    root.addHandler(stream_handler)
    
    unittest.main()
