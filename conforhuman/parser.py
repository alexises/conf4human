import ply.yacc as yacc
from .lexer import YamlLexer
from .ast import  LocalizableOrderedDict, LocalizableList
import logging

logger = logging.getLogger(__name__)


class YamlParser(object):
    def __init__(self):
        self.lexer = YamlLexer()
        self.lexerObj = self.lexer.build()
        self.tokens = self.lexer.tokens
        self.yacc = yacc.yacc(module=self, debug=True)

    start = "document"
    def p_error(self, p):
        pass 

    def p_document(self, p):
        '''document : structured_collection_items
                    | collection
                    | literal'''
        p[0] = p[1]
        logger.debug(p[0])

    def p_literal(self, p):
        '''literal : INT
                   | FLOAT
                   | BOOL
                   | NULL
                   | string'''
        p[0] = p[1]

    def p_string(self, p):
        '''string : SIMPLE_STRING
                  | DOUBLE_STRING
                  | NON_QUOTED_STRING'''
        p[0] = p[1]

    def p_collection(self, p):
        '''collection : inline_collection
                      | structured_collection '''
        p[0] = p[1]

    def p_inline_collection(self, p):
        '''inline_collection : inline_dict
                             | inline_list'''
        p[0] = p[1]

    def p_inline_dict(self, p):
        '''inline_dict : OPEN_BRACE inline_dict_items CLOSE_BRACE'''
        p[0] = p[2]

    def p_inline_dict_items(self, p):
        '''inline_dict_items : inline_dict_element
                             | inline_dict_items COMMA inline_dict_element
                             | empty'''
        if len(p) == 2:
           p[0] = LocalizableOrderedDict(p[-1].getEndPosition())
           if p[1] is not None:
               (key, val) = p[1]
               p[0].add(key, val)
        else:
           p[0] = p[1]
           (key, val) = p[3]
           p[0].add(key, val)

    def p_inline_dict_element(self, p):
        ''' inline_dict_element : string COLOM inline_literal '''
        p[0] = (p[1], p[3])

    def p_inline_literal(self, p):
        ''' inline_literal : literal
                           | inline_collection '''
        p[0] = p[1]

    def p_inline_list(self, p):
        ''' inline_list : OPEN_BRACKET inline_list_items CLOSE_BRACKET'''
        p[0] = p[2]

    def p_inline_list_items(self, p):
        ''' inline_list_items : inline_literal
                              | inline_list_items COMMA inline_literal
                              | empty'''
        if len(p) == 2:
           p[0] = LocalizableList(p[-1].getEndPosition())
           if p[1] is not None:
               p[0].add(p[1])
        else:
           p[0] = p[1]
           p[0].add(p[3])

    def p_structured_collection(self, p):
        '''structured_collection : BEGIN_BLOCK structured_collection_items END_BLOCK'''
        p[0] = p[2]

    def p_structured_collection_items(self, p):
        '''structured_collection_items : structured_list
                                       | structured_dict '''
        p[0] = p[1]

    def p_structured_list(self, p):
        '''structured_list : structured_list_item
                           | structured_list structured_list_item'''
        if len(p) == 2:
           p[0] = LocalizableList(p[1].getStartPosition())
           p[0].add(p[1])
        else:
           p[0] = p[1]
           p[0].add(p[2])

    def p_structured_list_item(self, p):
        ''' structured_list_item : MINUS document '''
        p[0] = p[2]

    def p_structured_dict(self, p):
        ''' structured_dict : structured_dict_item
                            | structured_dict structured_dict_item'''
        if len(p) == 2:
           (key, val) = p[1]
           p[0] = LocalizableOrderedDict(key.getStartPosition())
           p[0].add(key, val)
        else:
           p[0] = p[1]
           (key, val) = p[2]
           p[0].add(key, val)

    def p_structured_dict_item(self, p):
        ''' structured_dict_item : string COLOM inline_literal'''
        p[0] = (p[1], p[3])

    def p_empty(self, p):
        ''' empty : '''
        p[0] = None

    def parse_string(self, s):
        logger.debug(s)
        return self.yacc.parse(s, lexer=self.lexerObj)

    def parse(self, s):
        return self.yacc.parse(s)

    def parse_stdin(self):
        while 1:
            try:
                s = input('parse> ')
            except EOFError:
                break
            if not s:
                continue
            r = self.yacc.parse(s)
            r.pretty_print()

