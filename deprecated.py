# encoding: utf-8

def instruction_size(size):
    def wrapper(func):
        def _(p):
            global current_byte
            current_byte += size

            return func(p)
        _.__doc__ = func.__doc__
        _.__name__ = func.__name__
        _.__dict__.update(func.__dict__)
        return _
    return wrapper


