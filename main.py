from libs.exp_cpu_lex import lexer
from libs.exp_cpu_parser import parser, label_imm_table

if __name__ == '__main__':
    result = parser.parse(open('sample.asm').read(),
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
