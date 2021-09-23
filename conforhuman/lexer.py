from .ast import LocalizableLiteral, FilePosition
import ply.lex as lex

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
        self.block.append(0)

    def getPos(self):
        return FilePosition(self.lineno, self.column)

    def getLiteral(self, t, callack=None):
        begin = self.getPos()
        t.column += len(t.value)
        end = self.getPos()
        if callback is not None:
            t.value = callback(t.value)
        t.value = LocalizableLiteral(begin, end, t.value)
        return t

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_middle_space(self, t):
        'r^[ ]+'
        indent_size = len(t.value)
        self.column += current_size
        if indent_size > self.block[-1]:
            self.block.append(current_size)
            t.type = 'BEGIN_BLOCK'
            return t
        elif indent_size == self.block:
            return None
        elif indent_size != self.block[-2]:
            raise Exception('bad section indentation')
       
        self.block.pop()

    def t_newline(self, t):
        r'\n+'
        t.lineno += len(t.value)
        self.column = 0

    def t_space(self, t):
        r'[ ]+'
        t.column += len(t.value)

    def t_COLOM(self, t):
        r':'
        return self.getLiteral(f)

    def t_OPEN_BRACE(self, t):
        r'\{'
        return self.getLiteral(f)

    def t_CLOSE_BRACE(self, t):
        r'\}'
        return self.getLiteral(f)

    def t_OPEN_BRACKET(self, t):
        r'\['
        return self.getLiteral(f)

    def t_CLOSE_BRACKET(self, t):
        r'\]'
        return self.getLiteral(f)

    def t_COMMA(self, t):
        r','
        return self.getLiteral(f)
   
    def t_MINUS(self, t):
        r'-'
        return self.getLiteral(f)

    def t_INT(self, t):
        r'[0-9]+'
        return self.getLiteral(f, int)

    def t_FLOAT(self, t):
        r'[0-9]+\.[0-9]+'
        return self.getLiteral(f, float)

    def t_BOOL(self, t):
        r'(true|false)'
        begin = self.getPos()
        if t.value == 'true':
            t.value = True
        else:
            t.value = False
        self.column+=len(t.value)
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, t.value)
        return t

    def t_NULL(self, t):
        r'null'
        begin = self.getPos()
        self.column+=len(t.value)
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, None)
        return t

    def decode_string(self, t):
        begin = self.getPos()
        data = t.value[1:-2].decode('string_escape')
        self.column+=len(t.value)
        self.line+=data.count('\n')
        last_return = t.value.rfind(r'\n')
        if t.value.rfind(r'\n') >= 0:
            self.column = len(t.value) - t.value.rfind(r'\n') - 2
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, data)
        return t

    def t_SIMPLE_STRING(self, t):
        r"'([^']|\')*'"
        return self.decode_string(t)
   
    def t_DOUBLE_STRING(self, t):
        r'"([^"]|\")"'
        return self.decode_string(t)

    def t_NON_QUOTED_STRING(self, t):
        r"[^ :\"'][^:\"']*"
        begin = self.getPos()
        data = t.decode('string_escape')
        self.column+=len(t.value)
        self.line+=data.count('\n')
        last_return = t.value.rfind(r'\n')
        if t.value.rfind(r'\n') >= 0:
            self.column = len(t.value) - t.value.rfind(r'\n') - 2
        end = self.getPos()
        t.value = LocalizableLiteral(begin, end, data)
        return t
