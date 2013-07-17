
ASM Parser for Exp CPU
====

How to Run
----

Run `python main.py`


Dependency
----

* Ply 3.4


Result
----

This parser can now act as an assembler, producing machine code
which agree with the instruction spec at
[here](https://github.com/brickgao/CPU_Exercise/blob/master/op_codes.md ).

Run `python main.py` to find out more.


Simulator
----

In recent commits, a simulator is added (though only a subset of the
instruction set is implemented), which is able to run the `sample.asm` program
correctly.

`sample.asm` is a trivial program that calculates the product of two number,
which are stored in `R0` and `R1`.


TODO
----

Automatic inverse transformation on machine code, i.e. deassembling.


License
----

lgpl


contact: chsc4698@gmail.com

