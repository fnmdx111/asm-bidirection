# encoding: utf-8
import StringIO
from operator import itemgetter
from shared.ast_structure import InstRRR
from shared.misc import gen_byte_counter

get, inc = gen_byte_counter()


FUCK_PLY = """
FUCKING ply uses line numbers as the rules' precedences,
and the line numbers of the decorated functions are the line number of
the decorator,
that's why there are so many blank lines here.

P.S. it took me nearly 3 hours to figure this out
P.S.S. why can't I just explicit set the precedence of each rule???
e.g. def p_stmt_inst_P1(p):
         pass
"""



token_to_punct = {
    'COMMA': ',',
    'LPARAN': '(',
    'RPARAN': ')',
    'NEWLINE': '\n',
}




cls_to_spec = {}

def def_inst(name, cls, specs, size=4):
    """specs := {(attr_name, pos, type)}"""
    def wrapper(f):
        # save spec of the specific instruction class
        cls_to_spec[cls] = specs

        doc_string = 'instruction : %s' %\
                     ' '.join(map(itemgetter(2), specs))
        def _(p):
            inc(size=size)

            inst_obj = cls()
            for attr, pos, t in specs:
                if attr != 'ignored':
                    setattr(inst_obj, attr, p[pos])
            p[0] = inst_obj

            # do further operations on p,
            # e.g. lazy evaluation
            return f(p)

        _.__doc__ = doc_string
        return _
    return wrapper



def auto_print(obj):
    sbuf = StringIO.StringIO()
    spec = cls_to_spec[obj.__class__]

    for attr, _, t in spec:
        # it is assumed that attrs come in right order,
        # so `pos' is ignored here
        if attr != 'ignored':
            sbuf.write('%s' % getattr(obj, attr))
        else:
            sbuf.write('%s' % token_to_punct[t])
    return ' '.join(sbuf.buflist)



if __name__ == '__main__':
    @def_inst(name='r_r_r',
              cls=InstRRR,
              size=4,
              specs=[('op_code', 1, 'OPERATOR'),
                     ('rd', 2, 'REGISTER'),
                     ('ignored', 3, 'COMMA'),
                     ('rs', 4, 'REGISTER'),
                     ('ignored', 5, 'COMMA'),
                     ('rt', 6, 'REGISTER'),
                     ('ignored', 7, 'NEWLINE')])
    def p_instruction_r_r_r(p):
        pass

    obj = InstRRR('add', '$r0', '$r1', '$s2')
    print auto_print(obj)



