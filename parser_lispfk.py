from getch import getche
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

identity = lambda x: x

parser = ox.make_parser([

    ('tuple : OPEN_BRACKET elements CLOSE_BRACKET', lambda a, x, b: x),
    ('tuple : OPEN_BRACKET CLOSE_BRACKET', lambda a, b: '[]'),
    ('elements : term elements', lambda x, xs: [x] + xs),
    ('elements : term', lambda x: [x]),
    ('term : atom', identity),
    ('term : tuple', identity),
    ('atom : NAME', identity),
    ('atom : NUMBER', lambda x: int(x)),

], token_list)

data = [0]
ptr = 0
code_ptr = 0
breakpoints = []

@click.command()
@click.argument('source_file',type=click.File('r'))
def build(source_file):

    print_ast = pprint.PrettyPrinter(width=60, compact=True)
    source = source_file.read()

    tokens = lexer(source)
    print('\ntokens:\n')
    print(tokens)

    tokens = [value for value in tokens if str(value)[:7] != 'COMMENT' and str(value)[:8] != 'NEW_LINE']
    ast = parser(tokens)

    print('\nsyntatic tree:\n')
    print_ast.pprint(ast)

if __name__ == '__main__':
    build()
