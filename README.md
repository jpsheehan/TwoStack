# TwoStack

A simple stack based language inspired by [GolfScript](http://www.golfscript.com/golfscript/) and [brainfuck](https://en.wikipedia.org/wiki/Brainfuck).

## Basics:

*Give an overview of RPN and some examples involving arithmatic.*

## Operators:

### Mathematical Operators:

* Addition: +
* Subtraction: -
* Multiplication: *
* Integer Division: /
* Modulo: %
* Power: **

### Conditional Operators:

* Equal to: =
* Less than: <
* Greater than: >
* Unary not: !
* Logical and: &
* Logical or: |
* Logical xor: ^

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

* Comment: begin with 0[ and end with ];
* Define an alias: ~
* Recall an alias by typing the alias symbol
* Unconditional jump: @
* Conditional jump: ?
* Print character: .
* Read character: ,

## Examples

#### Hello, World!
This example displays the string "Hello, World!" and quits.
```
"Hello, World!"[`]$[.;]$
```

#### If Else Statement
This example displays the string "true" if the condition is true and "false" if the condition is false.
```
{[`]$[.;]$}~print
{
  "false"print@
}
{;
  "true"
  print@
{}0}

10 10 =

?;@
```

#### FizzBuzz Program
The infamous fizzbuzz test:
```
{[`]$[.;];$}~p$1 1[;${{{$:`0$[:10%48+`10/]$[`];0$p@10.}{;0$0$"Buzz"10p@{}0}$:`$5%0=?;@}{;0$0$"Fizz"10p@{}0}$:`$3%0=?;@}{;0$0$"Fizzbuzz"10p@{}0}$:`$:3%0=\5%0=&?;@$1+:100<]
```

#### Cat Program
Simply prints what it reads from the standard input. This works cleanly with pipes.
```
,:[;.;,:0 1-=!];;
```