#Assignment 2 - Code generator

Code generator to convert Three Adress Code(3AC) to MIPS
---------

src folder contains the main code.test cases are in test/ folder. 

Use the following commands to generate mips code.
```
cd asgn2
make
bin/codegen test/test1.ir
```

After generating MIPS code run using the following command
```
make spim
```

Then run the following command to clean binaries
```
make clean
```

## IR/3AC supported instructions:
* 