import ply.yacc as yacc
from .lexer import tokens, YamlLexer
from .ast import  LocalizableOrderedDict, LocalizableList

class YamlParser(object):
    def __init__(self):
        self.lexer = YamlLexer()
        self.lexer.build()
        self.tokens = tokens
        self.yacc = yacc.yacc(module=self,debug=True)

    def p_document(p):
        '''document : collection
                    | literal'''
        p[0] = p[1]

    def p_literal(p):
        '''literal : INT
                   | FLOAT
                   | BOOL
                   | string'''
        p[0] = p[1]

    def p_string(p):
        '''string : SIMPLE_STRING
                  | DOUBLE_STRING
                  | NON_QUOTED_STRING'''
        p[0] = p[1]

    def p_collection(p):
        '''collection : inline_collection
                      | structured_collection '''
        p[0] = p[1]

    def p_inline_collection(p):
        '''inline_collection : inline_dict
                             | inline_list'''
        p[0] = p[1]

    def p_inline_dict(p):
        '''inline_dict : OPEN_BRACKET inline_dict_items CLOSE_BRACKET'''
        p[0] = p[2]

    def p_inline_dict_items(p):
        '''inline_dict_item : dict_element
                            | inline_dict_item COMMA dict_element
                            | empty'''
        if len(p) == 1:
           p[0] = LocalizableOrderedDict()
        elif len(p) == 2:
           p[0] = LocalizableOrderedDict()
           (key, val) = p[1]
           p[0].add(key, val)
        else:
           p[0] = P[1]
           (key, val) = p[3]
           p[0].add(key, val)

    def p_inline_dict_item(p):
        ''' inline_dict_item : string COLOM inline_literal '''
        p[0] = (p[1], p[3])

    def p_inline_literal(p):
        ''' inline_literal : literal
                           | inline_collection '''
        p[0] = p[1]

    def p_inline_list(p):
        ''' inline_list : OPEN_BRACKET inline_list_items CLOSE_BRACKED'''
        p[0] = p[2]

    def p_inline_list_items(p):
        ''' inline_list_items: inline_literal
                             | inline_list_items COMA inline_literal
                             | empty'''
        if len(p) == 1:
           p[0] = LocalizableList()
        elif len(p) == 2:
           p[0] = LocalizableList()
           p[0].add(p[1])
        else:
           p[0] = P[1]
           (key, val) = p[3]
           p[0].add(key, val)

    def p_structured_collection(p):
        '''structured_collection: BEGIN_BLOCK structured_collection_items END_BLOCK'''
        p[0] = p[2]

    def p_structured_collection_items(p):
        '''structured_collection_items: structured_list
                                      | structured_dict '''
        p[0] = p[1]

    def p_structured_list(p):
        '''structured_list : structured_list_item
                           | structured_list structured_list_item
                           | empty'''
        if len(p) == 1:
           p[0] = LocalizableList()
        elif len(p) == 2:
           p[0] = LocalizableList()
           p[0].add(p[1])
        else:
           p[0] = P[1]
           (key, val) = p[3]
           p[0].add(key, val)

    def p_structured_list_item(p):
        ''' structured_list_item: MINUS document '''
        p[0] = p[2]

    def p_structured_dict(p):
        ''' structured_dict: structured_dict_item
                            | structured_dict structured_dict_item
                            | empty'''
        if len(p) == 1:
           p[0] = LocalizableOrderedDict()
        elif len(p) == 2:
           p[0] = LocalizableOrderedDict()
           (key, val) = p[1]
           p[0].add(key, val)
        else:
           p[0] = P[1]
           (key, val) = p[3]
           p[0].add(key, val)

    def p_structured_dict_item(p):
        ''' structrured_dict_item: string COLOM inline_literal'''
        p[0] = (p[1], p[3])

    def parse_string(self, s):
        return self.yacc.parse(s)

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

