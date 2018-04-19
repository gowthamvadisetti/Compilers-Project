make clean;
make;
bin/irgen $1;
FILE1="ir/test1.ir"     
if [ -f $FILE1 ]; then
	make codegen;
else
   echo "ERROR in Parser/Irgen check above"
   exit
fi
FILE2="mips/test1.asm"     
if [ -f $FILE2 ]; then
	make spim;
else
   echo "ERROR in Codegen check above"
fi