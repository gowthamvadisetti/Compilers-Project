# Ruby to MIPS Compiler

This is a compiler for the programming language Ruby. The target assembly language is MIPS and the compiler is implemented in Python

The 'project' folder contains the final compiler

'project/src' folder contains the code of the compiler

'project/test' contains sample test cases to test various features implemented in the compiler

Use the following commands to run the compiler

```
cd project
./ruby.sh test/1.basic_arithmetic.rb
```

After testing run ```make clean``` to remove the binaries

## Implemented features

* Data types:
  * int
  * bool
  * arrays 
  * strings(printing of a string)
  * classes
  
 * Typechecking of data types
 * Register spilling has been taken care of
 * Operators:
   * Arithmetic operators: +, -, *, /, %, +=, -=, *=, /=, %=
   * Logical operators: 
      * |, &, ^, <<, >>, |=, &=, ^= (for int)
      * ||, && (for bool)
   * All these have been implemented with appropriate operator precedence
* Input:
   * gets
* Output:
  * print(for int and bool)
  * puts(for strings)
* Loops:
  * For loop(both inclusive and exclusive range)
  * While loop
  * Until loop
  * 'Break' is implemented for each of the above loops
* Conditional constructs:
  * if-else:
    * if
    * if....else....
    * if....elsif...elsif...else....
    * Dangling if-else has been handled
  * switch case
* Functions:
  * Simple functions(no arguments or return value)
  * Functions with return value
  * Functions with one or multiple arguments
  * Recursive functions
  * Scoping (Differentiating local variables of various functions from global variables) has been handled
* Classes
  * Creation of an object with desired set of attributes
  * Creation of multiple objects of the same class
  * Multiple classes having same names for attributes has been handled
 
 
