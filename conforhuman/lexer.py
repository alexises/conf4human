from sre_constants import LITERAL
from textwrap import indent
from .ast import LocalizableLiteral, FilePosition
import ply.lex as lex
import codecs
import logging

logger = logging.getLogger(__name__)



class YamlLexer(object):
    tokens = (
        'COLOM',
        'OPEN_BRACE',
        'CLOSE_BRACE',
        'OPEN_BRACKET',
        'CLOSE_BRACKET',
        'COMMA',
        'MINUS',
        'BEGIN_BLOCK',
        'END_BLOCK',
        'SPACE',
        'INT',
        'FLOAT',
        'NULL',
        'BOOL',
        'SIMPLE_STRING',
        'DOUBLE_STRING',
        'NON_QUOTED_STRING'
   )

    def __init__(self):
        self.lineno = 0
        self.column = 0
        self.block = []
        self.minus_pos = None
        self.state = None
        #self.block.append(0)

    def getPos(self):
        return FilePosition(self.lineno, self.column)

    def getLiteral(self, t, callback=None):
        self.state = "LITERAL"
        begin = self.getPos()
        self.column += len(t.value)
        end = self.getPos()
        if callback is not None:
            t.value = callback(t.value)
        t.value = LocalizableLiteral(begin, end, t.value)
        return t

    def rollback_lexpos(self, t):
        t.lexer.lexpos -= len(t.value)
        self.column -= len(t.value)

    def build(self, **kwargs):
        return lex.lex(module=self, **kwargs)

    def t_blank_line(self, t):
        r'(?m)^[ ]+$'
        return None

    def t_middle_space(self, t):
        r'(?m)^[ ]+'
        logger.debug('middle space')
        indent_size = len(t.value)
        self.column += indent_size

        # exclude minus pos block creation
        if self.minus_pos == indent_size:
            return
        self.minus_pos = None
        if len(self.block) == 0 or indent_size > self.block[-1]:
            # gretter size, new block
            self.block.append(indent_size)
            t.type = 'BEGIN_BLOCK'
            return t
        elif indent_size == self.block[-1]:
            # same size, no token
            return None
        # lower size, try to remove a token
        self.block.pop()
        t.type = 'END_BLOCK'

        if self.block[-1] > indent_size:
            # we could try another block, so rewind the token
            self.rollback_lexpos(t)
        elif self.block[-1] > indent_size:
            # we have some missident, raise an exception
            logger.debug("stack size : %s", self.block)
            logger.debug("ident size : %s at %s:%s", indent_size, self.lineno, self.column)
            raise Exception('bad section indentation') 
        #if we got an exact match, do nothing more fancy
        return t

    def t_newline(self, t):
        r'\n+'
        t.lineno += len(t.value)
        self.column = 0

    def t_space(self, t):
        r'[ ]+'
        self.column += len(t.value)

    def t_COLOM(self, t):
        r':'
        return self.getLiteral(t)

    def t_OPEN_BRACE(self, t):
        r'\{'
        return self.getLiteral(t)

    def t_CLOSE_BRACE(self, t):
        r'\}'
        return self.getLiteral(t)

    def t_OPEN_BRACKET(self, t):
        r'\['
        return self.getLiteral(t)

    def t_CLOSE_BRACKET(self, t):
        r'\]'
        return self.getLiteral(t)

    def t_COMMA(self, t):
        r','
        return self.getLiteral(t)

    def t_FLOAT(self, t):
        r'-?[0-9]+\.[0-9]+'
        logger.debug('float')
        return self.getLiteral(t, float)

    def t_INT(self, t):
        r'-?[0-9]+'
        return self.getLiteral(t, int)

    def t_MINUS(self, t):
        r'-[ ]*'
        # check if previous state was a list, so we can revert the inhibition if it was running
        logger.debug(self.state)
        if self.state == "LIST_ITEM" and \
           self.minus_pos != None:
            self.state = None
            self.minus_pos = None
            self.block.append(self.column)
            self.rollback_lexpos(t)
            t.type = "BEGIN_BLOCK"
            logger.debug("exit inhibition")
            return t
        # we set inhibition for the next section creation this allow to manage
        # nested dict into nested list
        self.minus_pos = self.column
        l = self.getLiteral(t)
        self.state = "LIST_ITEM"
        logger.debug(self.state)
        return l

    def t_BOOL(self, t):
        r'(true|false)'
        begin = self.getPos()
        self.column+=len(t.value)
        if t.value == 'true':
            t.value = True
        else:
            t.value = False
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, t.value)
        return t

    def t_NULL(self, t):
        r'null'
        self.state = "LITERAL"
        begin = self.getPos()
        self.column+=len(t.value)
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, None)
        return t

    def decode_string(self, t):
        begin = self.getPos()
        data = codecs.escape_decode(str(t.value[1:-1]))[0].decode('utf8')
        self.column += len(t.value)
        self.lineno += data.count('\n')
        last_return = t.value.rfind(r'\n')
        if t.value.rfind(r'\n') >= 0:
            self.column = len(t.value) - t.value.rfind(r'\n') - 2
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, data)
        return t

    def t_SIMPLE_STRING(self, t):
        r"'([^']|\\')*'"
        self.state = "LITERAL"
        return self.decode_string(t)
   
    def t_DOUBLE_STRING(self, t):
        r'"([^"]|\\")*"'
        self.state = "LITERAL"
        return self.decode_string(t)

    def t_NON_QUOTED_STRING(self, t):
        r"[^ :\"'0-9{}\[\]\n-][^:\"'{}\[\]\n]*"
        self.state = "LITERAL"
        begin = self.getPos()
        data = codecs.escape_decode(str(t.value))[0].decode('utf8')
        self.column += len(t.value)
        self.lineno += data.count("\n")
        last_return = t.value.rfind(r'\n')
        if t.value.rfind(r'\n') >= 0:
            self.column = len(t.value) - t.value.rfind(r'\n') - 2
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, data)
        return t

    def t_eof(self, t):
        r'$'
        logger.debug(f"pool size {self.block}")
        logger.debug(f"len {len(t.value)}")
        if len(self.block) > 1:
            self.rollback_lexpos(t)
        if len(self.block) == 0:
            return None
        else:
            logger.debug('return end_block')
            self.block.pop()
            t.type = 'END_BLOCK'
            return t
            
