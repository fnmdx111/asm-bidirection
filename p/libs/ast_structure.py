# encoding: utf-8

class Instruction(object):
    def __init__(self, op_code):
        self.op_code = op_code
    def __str__(self):
        return 'OP_CODE %s' % self.op_code


class InstRR(Instruction):
    def __init__(self, op_code, dr, sr):
        super(InstRR, self).__init__(op_code)

        self.dr = dr
        self.sr = sr
    def __str__(self):
        return super(InstRR, self).__str__() + ', DR %s SR %s' % \
               (self.dr, self.sr)


class InstRImm(Instruction):
    def __init__(self, op_code, dr, imm):
        super(InstRImm, self).__init__(op_code)

        self.dr = dr
        self.imm = imm
    def __str__(self):
        return super(InstRImm, self).__str__() + ', DR %s IMM %s' % \
               (self.dr, self.imm)


class InstR(Instruction):
    def __init__(self, op_code, dr):
        super(InstR, self).__init__(op_code)

        self.dr = dr
    def __str__(self):
        return super(InstR, self).__str__() + ', DR %s' % self.dr


class InstImm(Instruction):
    def __init__(self, op_code, imm):
        super(InstImm, self).__init__(op_code)

        self.imm = imm
    def __str__(self):
        return super(InstImm, self).__str__() + ', IMM %s' % self.imm


class InstNoArg(Instruction):
    def __init__(self, op_code):
        super(InstNoArg, self).__init__(op_code)


class Label(Instruction):
    def __init__(self, name, pos):
        super(Label, self).__init__(None)
        self.name = name
        self.pos = pos


