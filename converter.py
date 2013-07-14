# encoding: utf-8

operator_binary = {
    'add': 0x10,
    'adc': 0x14,
    'sub': 0x12,
    'cmp': 0x02,
    'and': 0x11,
    'test': 0x01,
    'or': 0x13,
    'xor': 0x17,
    'not': 0x19,
    'mvrr': 0x1f,
    'ldrr': 0x82,
    'strr': 0x83,
    'mvrd': 0x810,
}

operator_unary = {
    'inc': 0x18,
    'dec': 0x1a,
    'shl': 0x0d,
    'shr': 0x0f,
    'jr': 0x40,
    'jrc': 0x44,
    'jrnc': 0x45,
    'jrz': 0x42,
    'jrnz': 0x43,
    'jmpa': 0x4f00,
}

register = {
    'r0': 0,
    'r1': 1,
    'r2': 2,
    'r3': 3,
    'r4': 4,
}

from exp_cpu_lex import label_table, lexer
from exp_cpu_parser import parser



if __name__ == '__main__':
    parser.parse(open('sample.asm', 'r').read(),
                 lexer=lexer)

    label_table = dict(zip(label_table.keys(),
                           range(len(label_table))))
    print label_table

