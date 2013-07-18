# encoding: utf-8

from public_libs.bin_tree import BTNode
from public_libs.ast_structure import *
from public_libs.misc import hn, i_2c, ln, mkw


class MachineCodeReader(object):

    OPRT_R_R = (
        0x10, 0x14, 0x12, 0x16, 0x02,
    #   add   adc   sub   sbb   cmp
        0x11, 0x01, 0x13, 0x17, 0x1f,
    #   and   test  or    xor   mvrr
        0x82, 0x83,
    #   ldrr  strr
    )

    OPRT_R_IMM = (
        0x81,
    #   mvrd
    )

    OPRT_R = (
        0x18, 0x1a, 0x1d, 0x1e,
    #   inc   dec   shl   shr
    )

    OPRT_IMM_1_BYTE = (
        0x40, 0x44, 0x45, 0x42, 0x43,
    #   jr    jrc   jrnc  jrz   jrnz
    )

    OPRT_IMM_2_BYTE = (
        0x4f,
    #   jmpa
    )

    OPRT_NO_ARG = ()

    def __init__(self):
        self._current_oprt = 0


    def load_machine_code(self, machine_code):
        self._machine_code = iter(machine_code)


    def __iter__(self):
        return self


    def next(self):
        if not self._machine_code:
            raise StopIteration
        else:
            self._current_oprt = self._machine_code.next()
            if self._current_oprt in self.OPRT_R_R:
                regs = self._machine_code.next()

                return InstRR(self._current_oprt,
                              hn(regs), ln(regs))

            elif self._current_oprt in self.OPRT_R_IMM:
                reg = self._machine_code.next()
                imm = mkw(self._machine_code.next(),
                          self._machine_code.next())

                return InstRImm(self._current_oprt,
                                hn(reg), i_2c(imm))

            elif self._current_oprt in self.OPRT_R:
                reg = self._machine_code.next()

                return InstR(self._current_oprt,
                             hn(reg))

            elif self._current_oprt in self.OPRT_IMM_1_BYTE:
                imm = self._machine_code.next()

                return InstImm(self._current_oprt,
                               i_2c(imm, size=8))

            elif self._current_oprt in self.OPRT_IMM_2_BYTE:
                # operators with one 2-byte imm arg are always 2-byte long
                self._current_oprt = mkw(self._current_oprt,
                                         self._machine_code.next())
                imm = mkw(self._machine_code.next(),
                          self._machine_code.next())

                return InstImm(self._current_oprt,
                               i_2c(imm))

            elif self._current_oprt in self.OPRT_NO_ARG:
                return InstNoArg(self._current_oprt)



if __name__ == '__main__':
    reader = MachineCodeReader()
    reader.load_machine_code([129, 0, 0, 25, 129, 16,
                              0, 6, 129, 32, 0, 0,
                              129, 48, 0, 8, 129, 64,
                              0, 1, 17, 65, 66, 2,
                              16, 32, 29, 0, 30, 16,
                              26, 48, 67, 238, 64, 254])
    ast = BTNode(None)
    for inst in reader:
        ast.append(inst)

    ast.traverse(lambda _: _)

