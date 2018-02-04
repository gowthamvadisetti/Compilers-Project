#The actual code generator
addr_desc={}
reg_desc={}
mips=""#mips code
registers=["$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$t8","$t9","$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7"]
def getEmptyRegister():
	global reg_desc
	global registers
	for i in registers:
		if not reg_desc.has_key(i):
			return i
	return  None

def getreg(instruction,variable,symbol_attach,line,is_input):
	global addr_desc
	global reg_desc
	global registers
	global mips
	reg=None
	if addr_desc.has_key(variable) and addr_desc[variable][0]=="register":
		reg=addr_desc[variable][1]
	elif getEmptyRegister() is not None:
		reg=getEmptyRegister()
		reg_desc[reg]=variable
		addr_desc[variable]=["register",reg]
		if is_input:
			if type(variable) is not int:
				mips+="lw "+reg+","+variable+"\n"
			else:
				mips+="li "+reg+","+str(variable)+"\n"
	else:
		print "is it"
		maxnextuse=line
		reqvar=None
		for i in reg_desc.keys():
			if symbol_attach[line].has_key(reg_desc[i]) and symbol_attach[line][reg_desc[i]][1] is not None:
				if symbol_attach[line][reg_desc[i]][1] > maxnextuse:
					reqvar=reg_desc[i]
					reg=i
					maxnextuse=symbol_attach[line][i][1]
			else:
				reg=i
				reqvar=reg_desc[i]
				break
		#move req var to memory
		addr_desc[reqvar]=["memory",None]
		reg_desc[reg]=variable
		addr_desc[variable]=["register",reg]
		mips+="sw "+reg+","+reqvar+"\n"
		if is_input:
			if type(variable) is not int:
				mips+="lw "+reg+","+variable+"\n"
			else:
				mips+="li "+reg+","+str(variable)+"\n"
	return reg

def generate_code(ir,block_start,block_end,symbol_attach):
	'''define getreg fn to assign registers or memory 
	for variables(as in slides) using symbol tables,address 
	descriptors,register descriptors

	reg_desc {register => variable}

	addr_desc {variable => register or memory,R2 or addr}

	how many registers in mips(16 or 32)?

	'''
	global addr_desc
	global reg_desc
	global mips
	for i in range(block_start,block_end+1):
		if ir[i].typ=="assign" or ir[i].typ=="arithmetic":
			if ir[i].op=="+":
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="add "+reg3+","+reg1+","+reg2+"\n"
			elif ir[i].op=="-":
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="sub "+reg3+","+reg1+","+reg2+"\n"

			elif ir[i].op=="=":
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="move "+reg2+","+reg1+"\n"				
		elif ir[i].typ=="print":
			reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
			mips+="li $v0,1\n"
			mips+="move $a0,"+reg1+"\n"
			mips+="syscall\n"
	return mips