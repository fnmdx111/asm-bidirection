# encoding: utf-8

from asm_parser.exp_cpu_lex import lexer
from asm_parser.exp_cpu_parser import parser

if __name__ == '__main__':
    result = parser.parse(open('sample.asm').read(),
                          lexer=lexer)

    result = [item() if callable(item) else item
              for item in result]

    print result

    with open('../test.bin', 'w') as f:
        for byte in result:
            print '%02x' % byte,
            f.write(chr(byte))


