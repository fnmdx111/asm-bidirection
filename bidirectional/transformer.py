# encoding: utf-8

from asm_parser.exp_cpu_parser import ast

from bidirectional.tables import operators, register
from shared.misc import inv_dict


class Transformer(object):
    asm_table = operators
    m_code_table = inv_dict(asm_table)
    asm_reg_table = register
    m_code_reg_table = inv_dict(register)

    def __init__(self):
        pass


    def load_ast(self, ast):
        self.ast = ast


    def transform(self):
        def _(ast_node):
            if not ast_node:
                return

            op_code = ast_node.op_code
            if op_code in self.asm_table:
                ast_node.op_code = self.asm_table[op_code]
                if hasattr(ast_node, 'dr'):
                    ast_node.dr = self.asm_reg_table[ast_node.dr]
                if hasattr(ast_node, 'sr'):
                    ast_node.sr = self.asm_reg_table[ast_node.sr]

            elif op_code in self.m_code_table:
                ast_node.op_code = self.m_code_table[op_code]
                if hasattr(ast_node, 'dr'):
                    ast_node.dr = self.m_code_reg_table[ast_node.dr]
                if hasattr(ast_node, 'sr'):
                    ast_node.sr = self.m_code_reg_table[ast_node.sr]

        self.ast.traverse(_)



if __name__ == '__main__':
    trans = Transformer()
    trans.load_ast(ast(open('../sample.asm', 'r').read()))
    trans.transform()
    trans.ast.traverse(lambda _: _)


