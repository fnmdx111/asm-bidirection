
Bidirectional Transformer between Assembly Language and Machine Code
====


Dependency
----

* Ply 3.4


Note
----

This transformer now can only understand the instruction spec defined in
[here](https://github.com/brickgao/CPU_Exercise/blob/master/op_codes.md ).

However, the final goal is to support a subset of the MIPS ASM.


Simulator
----

In recent commits, a simulator is added (though only a subset of the
instruction set is implemented), which is able to run the `sample.asm`
program correctly.

`sample.asm` is a trivial program that calculates the product of two number,
which are stored in `R0` and `R1`.


ASM Parser
----

The asm parser consumes proper ASM programs and generates ASTs according to
the programs provided. The parser uses Ply to parse ASM programs.


Machine Code Parser
----

The machine code parser creates ASTs of machine codes by using some sort
of state machine currently, may change to Ply parsing in the future.


TODO
----

Support MIPS assembly language.


License
----

lgpl


contact: chsc4698@gmail.com

