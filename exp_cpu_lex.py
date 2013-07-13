# encoding: utf-8

from ply import lex

tokens = (
    'IMMEDIATE',
    'OPERATOR',
    'REGISTER',
    'COMMA',
    'COLON',
    'ID',
    'NEWLINE'
)

operators = [
    # arithmetic instructions
    'add', 'inc', 'adc', 'sub', 'cmp', 'dec', 'sbb',
    'shl', 'shr', 'shl', 'shr',
    # logic instructions
    'and', 'test', 'or', 'xor', 'not',
    # register instructions
    'mvrr',
    # memory instructions
    'jr', 'jrc', 'jrnc', 'jrz', 'jrnz', 'jmpa',
    'ldrr', 'strr', 'mvrd',
    # test instruction
    'cld'
]

t_COMMA = ','
t_COLON = ':'

t_ignore_WHITESPACE = r'[\t ]+'
t_ignore_COMMENT = r';.*'

def t_IMMEDIATE(t):
    r'(?i)0x[a-f0-9]+|\d+(?![ \t]*[:a-z])'
    if t.value.isdigit():
        base = 10
        val = t.value
    else:
        base = 16
        val = t.value[2:]
    t.value = int(val, base=base)

    return t


def t_REGISTER(t):
    r'(?i)r\d+'
    return t


def t_ID(t):
    r'\w+'
    if t.value.lower() in operators:
        t.type = 'OPERATOR'

    return t


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print 'Illegal character \'%s\'' % t.value[0]
    t.lexer.skip(1)


lexer = lex.lex(debug=0)

if __name__ == '__main__':
    lexer.input(open('sample.asm', 'r').read())
    while True:
        tok = lexer.token()
        if not tok:
            break
        print tok

