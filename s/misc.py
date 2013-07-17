# encoding: utf-8

def mkw(b1, b2):
    return b1 << 4 | b2


def w(word):
    return word & 0xffff


def i_2c(word, size=16):
    """
    >>> i_2c(0xfffe)
    -2
    """
    if word & (1 << (size - 1)):
        word = word - int('1' * size, base=2) -1
    return int(word)


