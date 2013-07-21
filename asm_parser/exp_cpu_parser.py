# encoding: utf-8

import logging
from ply import yacc
from asm_parser.libs.ast_structure import *
from shared.misc import sgn
from asm_parser.exp_cpu_lex import tokens, lexer
from asm_parser.libs.auto import def_inst, get, inc


def setup_logger():
    logging.basicConfig(level=logging.DEBUG)

setup_logger()

label_imm_table = {}

def p_stmt_inst(p):
    """stmt : stmt instruction
            | instruction"""
    if len(p) == 2 and p[1]:
        p[0] = [p[1]]
    elif len(p) == 3 and p[1]:
        p[0] = p[1]
        if p[0] is None:
            p[0] = [None]
        if p[2]:
            p[0].append(p[2])


@def_inst(name='r_r_r',
          cls=InstRRR,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('rd', 2, 'REGISTER'),
                 ('ignored', 3, 'COMMA'),
                 ('rs', 4, 'REGISTER'),
                 ('ignored', 5, 'COMMA'),
                 ('rt', 6, 'REGISTER'),
                 ('ignored', 7, 'NEWLINE')])
def p_instruction_r_r_r(p):
    logging.debug('r_r_r OPRT %s REG %s REG %s REG %s, size=%s',
                             p[1],   p[2],  p[4],  p[6],    4)


@def_inst(name='r_r_imm',
          cls=InstRRImm,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('rd', 2, 'REGISTER'),
                 ('ignored', 3, 'COMMA'),
                 ('rs', 4, 'REGISTER'),
                 ('ignored', 5, 'COMMA'),
                 ('imm', 6, 'IMMEDIATE'),
                 ('ignored', 7, 'NEWLINE')])
def p_instruction_r_r_imm(p):
    logging.debug('r_r_imm OPRT %s REG %s REG %s IMM %s, size=%s',
                                p[1],  p[2],  p[4],  p[6],    4)


@def_inst(name='r_r',
          cls=InstRR,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('rd', 2, 'REGISTER'),
                 ('ignored', 3, 'COMMA'),
                 ('rs', 4, 'REGISTER'),
                 ('ignored', 5, 'NEWLINE')])
def p_instruction_r_r(p):
    logging.debug('r_r OPRT %s REG %s REG %s, size=%s',
                  p[1], p[2], p[4], 2)


@def_inst(name='r_imm',
          cls=InstRImm,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('rd', 2, 'REGISTER'),
                 ('ignored', 3, 'COMMA'),
                 ('imm', 4, 'IMMEDIATE'),
                 ('ignored', 5, 'NEWLINE')])
def p_instruction_r_imm(p):
    logging.debug('r_imm OPRT %s REG %s IMM %s, size=%s',
                  p[1], p[2], p[4], 4)


@def_inst(name='r_offset_r',
          cls=InstROffsetR,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('rd', 2, 'REGISTER'),
                 ('ignored', 3, 'COMMA'),
                 ('imm', 4, 'IMMEDIATE'),
                 ('ignored', 5, 'LPARAN'),
                 ('rs', 6, 'REGISTER'),
                 ('ignored', 7, 'RPARAN'),
                 ('ignored', 8, 'NEWLINE')])
def p_instruction_r_offset_r(p):
    logging.debug('r_offset_r OPRT %s REG %s IMM %s REG %s, size=%s',
                  p[1], p[2], p[4], p[6], 4)


@def_inst(name='r',
          cls=InstR,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('rd', 2, 'REGISTER'),
                 ('ignored', 3, 'NEWLINE')])
def p_instruction_r(p):
    logging.debug('r OPRT %s REG %s, size=%s',
                  p[1], p[2], 2)


@def_inst(name='',
          cls=InstNoArg,
          specs=[('op_code', 1, 'OPERATOR'),
                 ('ignored', 2, 'NEWLINE')])
def p_instruction_nullary(p):
    logging.debug('nullary OPRT %s, size=%s',
                  p[1], 2)


@def_inst(name='empty',
          cls=object,
          specs=[('ignored', 1, 'NEWLINE')])
def p_instruction_empty(_):
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

    #result.traverse(force)

    return result


if __name__ == '__main__':
    ast(open('../sample.asm', 'r').read())
    pass


