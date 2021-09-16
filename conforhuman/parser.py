from ast import LocalizableLiteral, FilePosition

class YamlLexer(object):
    tokens = (
        'COLOM',
        'OPEN_BRACE',
        'CLOSE_BRACE',
        'OPEN_BRACKET',
        'CLOSE_BRACKET',
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

   def getPos(self):
       return FilePosition(self.lineno, self.column)

   def build(self, **kwargs):
       self.lexer = lex.lex(module=self, **kwargs)

   def t_newline(t):
       r'\n+'
       t.lexer.lineno += len(t.value)
       self.column = 0

   def t_COLOM(self, t):
       r':'
       self.column++

   def t_OPEN_BRACE(self, t):
       r'\{'
       self.column++

   def t_CLOSE_BRACE(self, t):
       r'\}'
       self.column++

   def t_OPEN_BRACKET(self, t):
       r'\['
       self.column++

   def t_CLOSE_BRACKET(self, t):
       r'\]'
       self.column++

   def t_SPACE(self, t):
       r'[ ]+'
       self.column+=len(t.value)

   def t_INT(self, t):
       r'[0-9]+'
       begin = self.getPos()
       self.column+=len(t.value)
       end = self.getPos()
       t.value = LocalizableLiteral(begin, end, int(t.value))
       

   def t_FLOAT(self, t):
       r'[0-9]+\.[0-9]+'
       begin = self.getPos()
       self.column+=len(t.value)
       end = self.getPos()
       t.value = LocalizableLiteral(begin, end, float(t.value))

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

   def t_NULL(self, t):
       r'null'
       begin = self.getPos()
       self.column+=len(t.value)
       end = self.getPos()
       t.value = LocalizableLiteral(begin, end, None)



   def decode_string(self, t):
       begin = self.getPos()
       data = t.value[1:-2].decode('string_escape')
       self.column+=len(t.value)
       self.line+=data.count('\n')
       last_return = t.value.rfind(r'\n')
       if t.value.rfind(r'\n') >= 0:
           self.column = len(t.value - t.value.rfind(r'\n') - 2
       end = self.getPos()
       t.value = LocalizableLiteral(begin, end, data)

   def t_SIMPLE_STRING(self, t):
       r"'([^']|\')*'"
       self.decode_string(t)
   
   def t_DOUBLE_STRING(self, t):
       r'"([^"]|\")"'
       self.decode_string(t)

   def t_NON_QUOTED_STRING
       r"[^ :\"'][^:\"']*"
       begin = self.getPos()
       data = t.decode('string_escape')
       self.column+=len(t.value)
       self.line+=data.count('\n')
       last_return = t.value.rfind(r'\n')
       if t.value.rfind(r'\n') >= 0:
           self.column = len(t.value - t.value.rfind(r'\n') - 2
       end = self.getPos()
       t.value = LocalizableLiteral(begin, end, data)
