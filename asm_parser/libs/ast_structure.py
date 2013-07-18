# encoding: utf-8

from shared.ast_structure import *

class Label(Instruction):
    def __init__(self, name, pos):
        super(Label, self).__init__(None)
        self.name = name
        self.pos = pos


