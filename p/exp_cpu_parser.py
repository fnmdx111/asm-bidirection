# encoding: utf-8

import logging

from ply import yacc

from p.misc import sgn, b, r, w2b, gen_byte_counter
from p.tables import register, operator_binary, operator_unary, operator_nullary
from p.exp_cpu_lex import tokens, lexer


def setup_logger():
    logging.basicConfig(level=logging.DEBUG)

setup_logger()

label_imm_table = {}
get, inc = gen_byte_counter()


def p_stmt_inst(p):
    """stmt : stmt instruction
            | stmt label
            | instruction
            | label"""
    if len(p) == 2 and p[1] is not None:
        p[0] = []
        p[0] += p[1]
    elif len(p) == 3 and p[1] is not None:
        p[0] = p[1]
        if p[0] is None:
            p[0] = []
        if p[2]:
            p[0] += p[2]


def p_instruction_r_r(p):
    """instruction : OPERATOR REGISTER COMMA REGISTER NEWLINE"""
    logging.debug('r_r OPRT %s REG %s REG %s, size=%s',
                  p[1], p[2], p[4], 2)

    inc()

    p[0] = b(operator_binary[p[1]],
             r(register[p[2]], register[p[4]]))


def p_instruction_r_imm(p):
    """instruction : OPERATOR REGISTER COMMA IMMEDIATE NEWLINE"""
    logging.debug('r_imm OPRT %s REG %s IMM %s, size=%s',
                  p[1], p[2], p[4], 4)

    inc(4)

    p[0] = b(operator_binary[p[1]],
             r(register[p[2]], 0), # no sr so there's a 4-bit padding here
             w2b(sgn(p[4], 0xffff)))


def p_instruction_r_label(p):
    """instruction : OPERATOR REGISTER COMMA LABEL NEWLINE"""
    logging.debug('r_label OPRT %s REG %s LABEL %s, size=%s',
                  p[1], p[2], p[4], 2)

    inc()

    p[0] = b(operator_binary[p[1]],
             r(register[p[2]],
               PendingLabel(p[4], sgn, [0xf])))


def p_instruction_r(p):
    """instruction : OPERATOR REGISTER NEWLINE"""
    logging.debug('r OPRT %s REG %s, size=%s',
                  p[1], p[2], 2)

    inc()

    p[0] = b(operator_unary[p[1]],
             r(register[p[2]],
               0))


def p_instruction_imm(p):
    """instruction : OPERATOR IMMEDIATE NEWLINE"""
    size, operand = 2, p[2]
    if 'jr' in p[1]:
        operand = sgn(p[2], 0xff)
    elif 'jmp' in p[1]:
        size = 4
        operand = w2b(operand)

    logging.debug('imm OPRT %s IMM %s, size=%s',
                  p[1], operand, size)

    inc(size)

    p[0] = b(operator_unary[p[1]],
             operand)


class PendingLabel(object):
    """lazy evaluation of labels"""
    def __init__(self, name, func, args=()):
        self.name = name
        self.func = func
        self.func_args = args
    def __call__(self):
        return self.func(label_imm_table[self.name],
                         *self.func_args)
    def __str__(self):
        return '%s(\'%s\', %s)' % (self.func.__name__,
                                   self.name,
                                   ', '.join(map(str, self.func_args)))
    def __repr__(self):
        return str(self)


def p_instruction_label(p):
    """instruction : OPERATOR LABEL NEWLINE"""
    logging.debug('label OPRT %s LABEL %s, size=%s',
                  p[1], p[2], 2)

    inc()

    if 'jr' not in p[1]:
        operand = PendingLabel(p[2], sgn, [0xff])
    else:
        # this is a relative jump instruction
        current_byte = get() # immediately get the current position
        operand = PendingLabel(p[2],
                               lambda l_imm: sgn(l_imm - current_byte,
                                                 0xff))
    p[0] = b(operator_unary[p[1]],
             operand)


def p_instruction_nullary(p):
    """instruction : OPERATOR NEWLINE"""
    logging.debug('nullary OPRT %s, size=%s',
                  p[1], 2)

    inc()

    p[0] = b(operator_nullary[p[1]])


def p_instruction_empty(p):
    """instruction : NEWLINE"""
    logging.debug('empty, size=%s',
                  0)

    p[0] = b()


def p_label(p):
    """label : LABEL COLON NEWLINE
             | LABEL COLON"""
    logging.debug('label_def LABEL %s, current byte=%s',
                  p[1], get())

    label_imm_table[p[1]] = get()
    p[0] = b()


def p_error(_):
    logging.error('error occurred')


parser = yacc.yacc(method='LALR')

if __name__ == '__main__':
    result = parser.parse(open('../sample.asm').read(),
                          lexer=lexer)
    result = [item() if callable(item) else item for item in result]
    print label_imm_table
    print result
    b = 0
    with open('../test.bin', 'w') as f:
        while result:
            print '%02x' % result[0],
            f.write(chr(result[0]))
            result.pop(0)
            b += 1


