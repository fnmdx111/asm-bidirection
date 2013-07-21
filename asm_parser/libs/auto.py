# encoding: utf-8
from operator import itemgetter


def def_inst(name, cls, size, specs):
    """specs := {(attr_name, pos, type)}"""
    def wrapper(f):
        doc_string = 'instruction : %s' %\
                     ' '.join(map(itemgetter(2), specs))
        def _(p):
            inst_obj = cls()
            for attr, pos, t in specs:
                setattr(inst_obj, attr, p[pos])
            p[0] = inst_obj

            return f(p)
        _.__doc__ = doc_string
        return _
    return wrapper



