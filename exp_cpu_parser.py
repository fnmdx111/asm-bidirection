# encoding: utf-8

from ply import yacc

lut = {
}

from exp_cpu_lex import tokens, lexer

def p_stmt_inst(p):
    """stmt : stmt instruction
            | stmt label
            | instruction
            | label"""


def p_instruction_r_r(p):
    'instruction : OPERATOR REGISTER COMMA REGISTER NEWLINE'
    print 'r_r'
    print p[1], p[2], p[4]


def p_instruction_r_imm(p):
    'instruction : OPERATOR REGISTER COMMA IMMEDIATE NEWLINE'
    print 'r_imm'
    print p[1], p[2], p[4]


def p_instruction_r_id(p):
    'instruction : OPERATOR REGISTER COMMA ID NEWLINE'
    print 'r_id'
    print p[1], p[2], p[4]


def p_instruction_r(p):
    'instruction : OPERATOR REGISTER NEWLINE'
    print 'r'
    print p[1], p[2]


def p_instruction_imm(p):
    'instruction : OPERATOR IMMEDIATE NEWLINE'
    print 'imm'
    print p[1], p[2]


def p_instruction_id(p):
    'instruction : OPERATOR ID NEWLINE'
    print 'id'
    print p[1], p[2]


def p_instruction_unary(p):
    'instruction : OPERATOR NEWLINE'
    print 'unary'
    print p[1]


def p_instruction_empty(p):
    'instruction : NEWLINE'
    pass


def p_label(p):
    'label : ID COLON'
    print 'label'
    print p[1]


parser = yacc.yacc(method='LALR')

if __name__ == '__main__':
    result = parser.parse(open('sample.asm').read(),
                          lexer=lexer)

