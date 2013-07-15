# encoding: utf-8

"""case insensitive parser for exp cpu"""

from ply import lex

import logging

def setup_logger():
    logging.basicConfig(level=logging.DEBUG)

setup_logger()


tokens = (
    'IMMEDIATE',
    'OPERATOR',
    'REGISTER',
    'COMMA',
    'COLON',
    'ID',
    'NEWLINE',
    'LABEL'
)

# TODO make this lexer aware of the arity of the operator `shl' and `shr'

operators = [
    # arithmetic instructions
    'add', 'inc', 'adc', 'sub', 'cmp', 'dec', 'sbb',
    'shl', 'shr',
    # logic instructions
    'and', 'test', 'or', 'xor', 'not',
    # register instructions
    'mvrr',
    # memory instructions
    'jr', 'jrc', 'jrnc', 'jrz', 'jrnz', 'jmpa',
    'ldrr', 'strr', 'mvrd',
    # test instruction
]

t_COMMA = ','
t_COLON = ':'

t_ignore_WHITESPACE = r'[\t ]+'
t_ignore_COMMENT = r';.*'

def t_IMMEDIATE(t):
    r"""(?i)-?(0x[a-f0-9]+|\d+(?![ \t]*[:a-z]))"""

    # lexer rule for imm, e.g.
    # 23, -1, 0x3F, -0X3f, 0
    # TODO add support for 0b 0o (?)
    if t.value.isdigit():
        base = 10
        val = t.value
    else:
        base = 16
        val = t.value.replace('0x', '').replace('0X', '')

    t.value = int(val, base=base)

    return t


def t_REGISTER(t):
    r"""(?i)r\d+"""

    # lexer rule for reg, e.g.
    # r0, R1

    t.value = t.value.lower()
    return t


def t_ID(t):
    r"""\w+"""

    # lexer rule for labels or instruction operators, e.g.
    # mvrd, Loop, 1F

    lowered = t.value = t.value.lower()
    if lowered in operators:
        t.type = 'OPERATOR'
    else:
        t.type = 'LABEL'
        logging.debug('found LABEL %s at line %s',
                      t.value, t.lexer.lineno)

    return t


def t_NEWLINE(t):
    r"""\n"""

    # lexer rule for newlines

    t.lexer.lineno += 1
    return t


def t_error(t):
    logging.error('illegal character \'%s\'', t.value[0])

    t.lexer.skip(1)


lexer = lex.lex(debug=0)

if __name__ == '__main__':
    lexer.input(open('../sample.asm', 'r').read())
    while True:
        tok = lexer.token()
        if not tok:
            break
        print tok


