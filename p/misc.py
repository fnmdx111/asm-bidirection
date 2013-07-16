# encoding: utf-8

import string


def sgn(imm, mask=0xff):
    """
    get the two's complement of imm

    >>> sgn(-31, 0xff)
    225
    """
    imm = imm if imm >= 0 else (~-imm + 1) & mask
    return imm


def purify_label(label):
    """
    >>> purify_label('1f')
    '1'
    """
    return label.translate(None, string.ascii_letters)


def b(*args):
    """
    flatten args

    >>> b([0x40, 0], 2, 3)
    [64, 0, 2, 3]
    """
    # TODO auto-compute the size of the instructions
    ret = []
    for arg in args:
        if isinstance(arg, list):
            ret += arg
        else:
            ret.append(arg)
    return ret


def r(pos1, pos2):
    """
    lazily build two nibbles into a single byte

    >>> r(1, 0)()
    16
    """
    make_callable = lambda _: (lambda: _) if not callable(_) else _
    arg1, arg2 = make_callable(pos1), make_callable(pos2)

    # arg1 and arg2 are both callable
    return lambda: int('%01x%01x' % (arg1(), arg2()), base=16)


def w2b(word):
    """
    split a word imm into two byte imms

    >>> w2b(0x1234)
    [18, 52]
    """
    return [(word & 0xff00) >> 8, word & 0xff]


def gen_byte_counter():
    # caution: dirty hack here
    byte = [0]
    def get():
        return byte[0]
    def inc(size=2):
        byte[0] += size
    return get, inc


if __name__ == '__main__':
    print sgn(-31)


