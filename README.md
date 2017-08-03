# TwoStack

A simple stack based language inspired by [GolfScript](http://www.golfscript.com/golfscript/) and [brainfuck](https://en.wikipedia.org/wiki/Brainfuck).

## Basics:

*Give an overview of RPN and some examples involving arithmatic.*

## Operators:

### Mathematical Operators:

* Addition: +
* Subtraction: -
* Multiplication: *
* Division: /
* Integer Division: //
* Modulo: %
* Power: ^

### Conditional Operators:

* Equal to: =
* Less than: <
* Greater than: >
* Unary not: !

### Literals:

* String literals are enclosed in "
* Integer literals are written normally
* Code blocks are written enclosed in { and }

### Stack Operators:

* Duplicate: :
* Discard: ;
* Swap: \
* Swap 3: \\
* Switch stacks: $
* Crosspop: `

### Other Features:

* Comment: begin with # and end at the next newline
* Define an alias: |
* Recall an alias by typing the alias symbol
* Unconditional jump: @
* Conditional jump: ?
* Print character: .
* Read character: ,

## Examples

##### Hello, World!
This example displays the string "Hello, World!" and quits.
```
"Hello, World!"[`]$[.;]
```

##### If Else Statement
This example displays the string "true" if the condition is true and "false" if the condition is false.
```
# define a print function
{[`]$[.;]}|print

# execute a particular block depending on the condition (10 == 10).
{"false"print@}{;"true"print@{}0}10 10=?;@
```