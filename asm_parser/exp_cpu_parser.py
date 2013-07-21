# encoding: utf-8

import logging

from ply import yacc

from asm_parser.libs.ast_structure import *
from shared.bin_tree import BTNode
from shared.misc import sgn, gen_byte_counter
from asm_parser.exp_cpu_lex import tokens, lexer

# this is comment
def setup_logger():
    logging.basicConfig(level=logging.DEBUG)

setup_logger()

label_imm_table = {}
get, inc = gen_byte_counter()


def p_stmt_inst(p):
    """stmt : stmt instruction
            | instruction"""
    if len(p) == 2 and p[1]:
        p[0] = BTNode(p[1])
    elif len(p) == 3 and p[1]:
        p[0] = p[1]
        if p[0] is None:
            p[0] = BTNode(None)
        if p[2]:
            p[0].append(p[2])
    else:
        p[0] = p[0]


def p_instruction_r_r_r(p):
    """instruction : OPERATOR REGISTER COMMA REGISTER COMMA REGISTER NEWLINE"""
    logging.debug('r_r_r OPRT %s REG %s REG %s REG %s, size=%s',
                             p[1],   p[2],  p[4],  p[6],    4)

    inc()

    p[0] = InstRRR(p[1],
                   p[2],
                   p[4],
                   p[6])


def p_instruction_r_r_imm(p):
    """instruction : OPERATOR REGISTER COMMA REGISTER COMMA IMMEDIATE NEWLINE"""
    logging.debug('r_r_imm OPRT %s REG %s REG %s IMM %s, size=%s',
                                p[1],  p[2],  p[4],  p[6],    4)
    inc()

    p[0] = InstRRImm(p[1],
                     p[2],
                     p[4],
                     p[6])


def p_instruction_r_r(p):
    """instruction : OPERATOR REGISTER COMMA REGISTER NEWLINE"""
    logging.debug('r_r OPRT %s REG %s REG %s, size=%s',
                  p[1], p[2], p[4], 2)

    inc()

    p[0] = InstRR(p[1],
                  p[2],
                  p[4])


def p_instruction_r_imm(p):
    """instruction : OPERATOR REGISTER COMMA IMMEDIATE NEWLINE"""
    logging.debug('r_imm OPRT %s REG %s IMM %s, size=%s',
                  p[1], p[2], p[4], 4)

    inc()

    p[0] = InstRImm(p[1],
                    p[2],
                    sgn(p[4], 0xffff))


def p_instruction_r_offset_r(p):
    """instruction : OPERATOR REGISTER COMMA IMMEDIATE LPARAN REGISTER RPARAN NEWLINE"""
    logging.debug('r_offset_r OPRT %s REG %s IMM %s REG %s, size=%s',
                  p[1], p[2], p[4], p[6], 4)

    inc()

    p[0] = InstROffsetR(p[1],
                        p[2],
                        p[4],
                        p[6])


def p_instruction_r(p):
    """instruction : OPERATOR REGISTER NEWLINE"""
    logging.debug('r OPRT %s REG %s, size=%s',
                  p[1], p[2], 2)

    inc()

    p[0] = InstR(p[1],
                 p[2])
    # p[0] = b(operator_unary[p[1]],
    #          r(register[p[2]],
    #            0))


def p_instruction_imm(p):
    """instruction : OPERATOR IMMEDIATE NEWLINE"""
    size, operand = 2, p[2]
    if 'jr' in p[1]:
        operand = sgn(p[2], 0xff)
    elif 'jmp' in p[1]:
        size = 4

    logging.debug('imm OPRT %s IMM %s, size=%s',
                  p[1], operand, size)

    inc(size)

    p[0] = InstImm(p[1],
                   operand)
    # p[0] = b(operator_unary[p[1]],
    #          operand)


def p_instruction_nullary(p):
    """instruction : OPERATOR NEWLINE"""
    logging.debug('nullary OPRT %s, size=%s',
                  p[1], 2)

    inc()

    p[0] = InstNoArg(p[1])
    # p[0] = b(operator_nullary[p[1]])


def p_instruction_empty(_):
    """instruction : NEWLINE"""
    logging.debug('empty, size=%s',
                  0)


def p_error(_):
    logging.error('error occurred')


parser = yacc.yacc(method='LALR')


def ast(input_str):
    result = parser.parse(input_str, lexer=lexer)

    def force(inst):
        if 'Imm' in inst.__class__.__name__:
            if callable(inst.imm):
                inst.imm = inst.imm()

    result.traverse(force)

    return result


if __name__ == '__main__':
    ast(open('../sample.asm', 'r').read()).traverse(lambda _: _)


