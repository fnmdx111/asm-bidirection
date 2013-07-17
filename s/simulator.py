# encoding: utf-8
from s.misc import i_2c, mkw, w


class Simulator(object):
    def __init__(self):
        self._c_flag = 0
        self._z_flag = 0

        self._r0 = 0
        self._r1 = 0
        self._r2 = 0
        self._r3 = 0
        self._r4 = 0

        self._pc = 0
        self._ir = 0

        self._mem = {}

        self.machine_code = []

        self._d_sr = 0
        self._d_dr = 0

        self._op_code_z_c_binary_table = {
            0x10: lambda a, b: a + b,                        # add
            0x14: lambda a, b: a + b + self._c_flag,         # adc
            0x12: lambda a, b: a - b,                        # sub
            0x16: lambda a, b: a - b + self._c_flag,         # sbb
        }
        self._op_code_z_c_binary_n_table = {
            0x02: self._op_code_z_c_binary_table[0x12]       # cmp
        }
        self._op_code_z_c_unary_table = {
            0x18: lambda a: a + 1,                           # inc
            0x1a: lambda a: a - 1,                           # dec
            0x1d: lambda a: a << 1,                          # shl
            0x1e: lambda a: a >> 1 | a & 0x8000,             # shr
        }
        self._op_code_z_binary_table = {
            0x11: lambda a, b: a & b | (self._c_flag << 16), # and
            0x13: lambda a, b: a | b | (self._c_flag << 16), # or
            0x17: lambda a, b: a ^ b | (self._c_flag << 16), # xor
        }
        self._op_code_z_binary_n_table = {
            0x01: lambda a, b: a - b,                        # test
        }
        self._op_code_z_unary_table = {
            0x19: lambda a: ~a,                              # not
        }
        self._op_code_binary_table = {
            0x1f: lambda a, b: a,                            # mvrr
        }

        self._op_codes = {}
        for d in [self._op_code_z_c_binary_table,
                  self._op_code_z_c_binary_n_table,
                  self._op_code_z_c_unary_table,
                  self._op_code_z_binary_table,
                  self._op_code_z_binary_n_table,
                  self._op_code_z_unary_table,
                  self._op_code_binary_table]:
            self._op_codes.update(d)


    def load_machine_code(self, machine_code, auto_halt=True):
        self.machine_code = machine_code

        self._ins_counter = 0

        self._auto_halt = auto_halt
        if self._auto_halt:
            self._last_dump = ''


    def _next_word(self):
        self._pc += 2
        return self.machine_code[self._pc - 2 : self._pc]


    def _reg_mux(self, num):
        return '_r%s' % num


    def _ins_decode(self):
        self._d_dr, self._d_sr = (self._reg_mux(self._ir[1] >> 4),
                                  self._reg_mux(self._ir[1] & 0x0f))
        # both of _d_xr are str

        op_code = self._ir[0] & 0x1f

        if self._ir[0] & 0xe0 == 0:
            # arithmetic instruction

            self.__f_single = False
            self.__f_modify = False
            self.__f_z = False
            self.__f_c = False

            if op_code in self._op_code_z_c_binary_table:
                self.__f_modify = True
                self.__f_z = True
                self.__f_c = True
            elif op_code in self._op_code_z_c_binary_n_table:
                self.__f_z = True
                self.__f_c = True
            elif op_code in self._op_code_z_binary_table:
                self.__f_modify = True
                self.__f_z = True
            elif op_code in self._op_code_z_binary_n_table:
                self.__f_z = True
            elif op_code in self._op_code_z_c_unary_table:
                self.__f_single = True
                self.__f_modify = True
                self.__f_z = True
                self.__f_c = True
            elif op_code in self._op_code_z_unary_table:
                self.__f_single = True
                self.__f_modify = True
                self.__f_z = True
            elif op_code in self._op_code_binary_table:
                self.__f_modify = True

            self._alu_func = self._op_codes[op_code]
            result, carry, zero = self._alu_proc()

            if self.__f_modify:
                self.__setattr__(self._d_dr, result)
            if self.__f_c:
                self._c_flag = carry
            if self.__f_z:
                self._z_flag = zero
        elif self._ir[0] & 0xe0 == 0x40:
            # jump instruction

            absolute, jump = False, False
            if op_code == 0:
                jump = True
            elif op_code == 0x04:
                jump = self._c_flag
            elif op_code == 0x05:
                jump = not self._c_flag
            elif op_code == 0x02:
                jump = self._z_flag
            elif op_code == 0x03:
                jump = not self._z_flag
            elif op_code == 0x0f:
                jump = True
                absolute = True
            if not absolute:
                if jump:
                    self._pc += i_2c(self._ir[1], size=8)
            if absolute:
                self._pc = i_2c(mkw(*self._next_word()))
        elif self._ir[0] & 0xe0 == 0x80:
            # memory instruction

            if op_code == 0x01:
                self.__setattr__(self._d_dr,
                                 i_2c(mkw(*self._next_word()),
                                      size=16))


    def _alu_proc(self):
        dr, sr = (self.__getattribute__(self._d_dr),
                  self.__getattribute__(self._d_sr))
        if self.__f_single:
            dr = self._alu_func(dr)
        else:
            dr = self._alu_func(dr, sr)

        carry = (dr & 0x10000) >> 16
        zero = int(dr & 0xffff == 0)
        dr = w(dr)

        return dr, carry, zero


    def next(self):
        self._ir = self._next_word()

        self._ins_decode()

        self._ins_counter += 1

        if self._auto_halt:
            if self._test_halt():
                raise StopIteration
            else:
                self._last_dump = self.dump()


    def dump(self):
        return ('%04x' * 9) % (self._pc, mkw(*self._ir),
                               self._r0, self._r1, self._r2, self._r3, self._r4,
                               self._c_flag, self._z_flag)


    def _test_halt(self):
        if self._last_dump == self.dump():
            return True
        return False


    def report(self):
        print (' %s ' % self._ins_counter).rjust(8, '-').ljust(60, '-')
        print 'PC = %04x, IR = %04x' % (self._pc, mkw(*self._ir))
        print 'R0 = %04x, R1 = %04x, R2 = %04x, R3 = %04x, R4 = %04x' %\
              (self._r0, self._r1, self._r2, self._r3, self._r4)
        print 'CF = %s, ZF = %s' % (self._c_flag, self._z_flag)


    def __iter__(self):
        return self



if __name__ == '__main__':
    sim = Simulator()
    sim.load_machine_code([129, 0, 0, 25, 129, 16,
                           0, 6, 129, 32, 0, 0,
                           129, 48, 0, 8, 129, 64,
                           0, 1, 17, 65, 66, 2,
                           16, 32, 29, 0, 30, 16,
                           26, 48, 67, 238, 64, 254])

    for i in sim:
        sim.report()


