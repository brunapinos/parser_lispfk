import ox
import click

number = lambda x: ('value', float(x))
name = lambda y: ('value', str(x))
brackets = lambda openbracket, term, closebracket: (openbracket, term, closebracket) 

lexer = ox.make_lexer([
    ('NUMBER', r'\d+(\.\d*)?'),
    ('NAME', r'[a-zA-Z]+'),
    ('OPEN_BRACKET', r'\('),
    ('CLOSE_BRACKET', r'\)'),
])

token_list = [
    'NUMBER',
    'NAME',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
]

parser = ox.make_parser([

    ('expression : OPEN_BRACKET term CLOSE_BRACKET', brackets),
    ('term : atom term', lambda atom, term: (atom, term)),
    ('term : term atom', lambda term, atom: (term, atom)),
    ('term : atom', lambda term: term),
    ('atom : NAME', name),
    ('atom : NUMBER', number),
], token_list)


@click.command()
@click.argument('source_file',type=click.File('r'))
def build(source_file):

    code = source_file.read()
  
    tokens = lexer(code)
    ast = parser(tokens)
    pprint.pprint(ast)

if __name__ == '__main__':
     build()



