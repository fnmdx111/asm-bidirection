# encoding: utf-8

class Instruction(object):
    def __init__(self, op_code):
        self.op_code = op_code
    def __str__(self):
        return 'op_code %s' % self.op_code


class InstRRR(Instruction):
    def __init__(self, op_code, rd, rs, rt):
        super(InstRRR, self).__init__(op_code)
        self.rd = rd
        self.rs = rs
        self.rt = rt
    def __str__(self):
        return super(InstRRR, self).__str__() + ', rd %s rs %s rt %s' % \
               (self.rd, self.rs, self.rt)


class InstRRImm(Instruction):
    def __init__(self, op_code, rd, rs, imm):
        super(InstRRImm, self).__init__(op_code)
        self.rd = rd
        self.rs = rs
        self.imm = imm
    def __str__(self):
        return super(InstRRImm, self).__str__() + ', rd %s rs %s imm %s' % \
               (self.rd, self.rs, self.imm)


class InstRR(Instruction):
    def __init__(self, op_code, rd, rs):
        super(InstRR, self).__init__(op_code)

        self.rd = rd
        self.rs = rs
    def __str__(self):
        return super(InstRR, self).__str__() + ', rd %s rs %s' % \
               (self.rd, self.rs)


class InstROffsetR(Instruction):
    def __init__(self, op_code, rd, offset, rs):
        super(InstROffsetR, self).__init__(op_code)
        self.rd = rd
        self.offset = offset
        self.rs = rs
    def __str__(self):
        return super(InstROffsetR, self).__str__() + ', rd %s offset %s rt %s' % \
               (self.rd, self.offset, self.rs)


class InstRImm(Instruction):
    def __init__(self, op_code, rd, imm):
        super(InstRImm, self).__init__(op_code)

        self.rd = rd
        self.imm = imm
    def __str__(self):
        return super(InstRImm, self).__str__() + ', rd %s IMM %s' % \
               (self.rd, self.imm)


class InstR(Instruction):
    def __init__(self, op_code, rd):
        super(InstR, self).__init__(op_code)

        self.rd = rd
    def __str__(self):
        return super(InstR, self).__str__() + ', rd %s' % self.rd


class InstImm(Instruction):
    def __init__(self, op_code, imm):
        super(InstImm, self).__init__(op_code)

        self.imm = imm
    def __str__(self):
        return super(InstImm, self).__str__() + ', IMM %s' % self.imm


class InstNoArg(Instruction):
    def __init__(self, op_code):
        super(InstNoArg, self).__init__(op_code)


