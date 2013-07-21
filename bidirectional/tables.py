# encoding: utf-8

operators = {
    'add':(0,32),
    'sub':(0,34),
    'lw':(35,0),
    'sw':(43,0),
    'and':(0,36),
    'or':(0,37),
    'mul':(28,2),
    'xor':(0,0x26),
    'sll':(0,0)
}

operator_unary = {
    'inc': 0x18,
    'dec': 0x1a,
    'shl': 0x1d,
    'shr': 0x1e,
    'jr': 0x40,
    'jrc': 0x44,
    'jrnc': 0x45,
    'jrz': 0x42,
    'jrnz': 0x43,
    'jmpa': 0x4f00, # this is a 2-byte instruction
}

operator_nullary = {
    'cld': NotImplemented
}

register = {
    '$zero' :   0,
    '$at'   :   1,
    '$v0'   :   2,
    '$v1'   :   3,
    '$a0'   :   4,
    '$a1'   :   5,
    '$a2'   :   6,
    '$a3'   :   7,
    '$t0'   :   8,
    '$t1'   :   9,
    '$t2'   :   10,
    '$t3'   :   11,
    '$t4'   :   12,
    '$t5'   :   13,
    '$t6'   :   14,
    '$t7'   :   15,
    '$s0'   :   16,
    '$s1'   :   17,
    '$s2'   :   18,
    '$s3'   :   19,
    '$s4'   :   20,
    '$s5'   :   21,
    '$s6'   :   22,
    '$s7'   :   23,
    '$t8'   :   24,
    '$t9'   :   25,
    '$gp'   :   28,
    '$sp'   :   29,
    '$k0'   :   26,
    '$k1'   :   27,
    '$fp'   :   30,
    '$s8'   :   30,
    '$ra'   :   31
}



