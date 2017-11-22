from sys import argv
import pprint 
import ox

file_name, lf_source = argv

in_file = open(lf_source)
source = in_file.read()

lexer = ox.make_lexer([
    ('COMMENT', r';(.)*'),
    ('NEW_LINE', r'\n+'),
    ('NAME', r'[a-zA-Z_][a-zA-Z_0-9-]*'),
    ('NUMBER', r'\d+(\.\d*)?'),
    ('OPEN_BRACKET', r'\('),
    ('CLOSE_BRACKET', r'\)'),
])

token_list = [
    'NAME',
    'NUMBER',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
]

parser = ox.make_parser([


    ('expr : OPEN_BRACKET term CLOSE_BRACKET', lambda openbracket, \
        atom, closebracket: atom),
    ('term : term term', lambda term, other_term: (term, other_term)),
    ('term : term atom', lambda term, atom: (term, atom)),
    ('term : atom term', lambda atom, term: (atom, term)),
    ('term : term', lambda term: term),
    ('term : atom', lambda term: atom),
    ('atom : NAME', lambda name: name),
    ('atom : NUMBER', lambda x: float(x)),
    ('atom : OPEN_BRACKET CLOSE_BRACKET', lambda open_bracket, close_bracket: ()),

], token_list)

print_ast = pprint.PrettyPrinter(width=60, compact=True)

tokens = lexer(source)
tokens = [value for value in tokens if str(value)[:7] != 'COMMENT' and str(value)[:8] != 'NEW_LINE']
ast = parser(tokens)

print_ast.print(ast)




