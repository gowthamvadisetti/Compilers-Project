#The actual code generator
def getreg(in1,in2,out,op,symbol_table,addr_desc,reg_desc):
	'''define getreg fn to assign registers or memory 
	for variables(as in slides) using symbol tables,address 
	descriptors,register descriptors
	
	x = y op z
	1)First, it searches for a register already containing the name y.
	If such a register exists, and if y has no further use after the 
	execution of x = y op z, and if it is not live at the end of the block and holds the value of no other name, then return the register for L.
	
	2)Otherwise, getreg() searches for an empty register; and if an empty register 
	is available, then it returns it for L.

	3)If no empty register exists, and if x has further use in the block, 
	or op is an operator such as indexing that requires a register,
	then getreg() it finds a suitable, occupied register. 
	The register is emptied by storing its value in the proper memory
	location M, the address descriptor is updated, the register is 
	returned for L. (The least-recently used strategy can be used to
	find a suitable, occupied register to be emptied.)

	4)If x is not used in the block or no suitable, occupied register
	can be found, getreg() selects a memory location of x and returns it for L.

	'''
	pass

def generate_code(ir,leaders,symbol_table):
	'''define getreg fn to assign registers or memory 
	for variables(as in slides) using symbol tables,address 
	descriptors,register descriptors

	reg_desc {register => variable}

	addr_desc {variable => register or memory}

	how many registers in mips(16 or 32)?


	'''
	mips=""#mips code
	return mips