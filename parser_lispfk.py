import click
import pprint 
import ox

lexer = ox.make_lexer([
    ('COMMENT', r';(.)*'),
    ('NEW_LINE', r'\n+'),
    ('OPEN_BRACKET', r'\('),
    ('CLOSE_BRACKET', r'\)'),
    ('NAME', r'[a-zA-Z_][a-zA-Z_0-9-]*'),
    ('NUMBER', r'\d+(\.\d*)?'),
])

token_list = [
    'NAME',
    'NUMBER',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
]

parser = ox.make_parser([


    ('term : OPEN_BRACKET term CLOSE_BRACKET', lambda openbracket, term, closebracket: term),
    ('term : term term', lambda term, other_term: (term, other_term)),
    ('term : term atom', lambda term, atom: (term, atom)),
    ('term : atom term', lambda atom, term: (atom, term)),
    ('term : atom', lambda term: term),
    ('atom : NAME', lambda name: name),
    ('atom : NUMBER', lambda x: float(x)),
    ('atom : OPEN_BRACKET CLOSE_BRACKET', lambda open_bracket, close_bracket: ()),

], token_list)

@click.command()
@click.argument('source_file',type=click.File('r'))
def build(source_file):

    print_ast = pprint.PrettyPrinter(width=60, compact=True)
    source = source_file.read()

    tokens = lexer(source)
    tokens = [value for value in tokens if str(value)[:7] != 'COMMENT' and str(value)[:8] != 'NEW_LINE']
    ast = parser(tokens)

    print_ast.pprint(ast)

if __name__ == '__main__':
    build()



