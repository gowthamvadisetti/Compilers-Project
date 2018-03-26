#The actual code generator
addr_desc={}
reg_desc={}
mips=""
#18 mips registers for our use
registers=["$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$t8","$t9","$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7"]
# registeers=registers[:4]

def getEmptyRegister():
	global reg_desc
	global registers
	for i in registers:
		if not (i in reg_desc):
			return i
	return  None

def end_block(symbol_attach,line):
	global reg_desc
	global mips
	del_keys=[]
	for i in reg_desc.keys():
		# print(line)
		# print(symbol_attach)
		if not(reg_desc[i] in symbol_attach[line] and symbol_attach[line][reg_desc[i]][0]=="live"):
			mips+="sw "+i+","+reg_desc[i]+"\n"
			print("sw "+i+","+reg_desc[i]+"\n")
			addr_desc[reg_desc[i]]=["memory",None]
			del_keys.append(i)
	for i in del_keys:
		del reg_desc[i]

def getreg(instruction,variable,symbol_attach,line,is_input):
	global addr_desc
	global reg_desc
	global registers
	global mips
	reg=None
	if (variable in addr_desc) and addr_desc[variable][0]=="register":
		reg=addr_desc[variable][1]
	elif getEmptyRegister() is not None:
		reg=getEmptyRegister()
		if type(variable) is not int:
			reg_desc[reg]=variable
			addr_desc[variable]=["register",reg]
		if is_input:
			if type(variable) is not int:
				mips+="lw "+reg+","+variable+"\n"
			else:
				mips+="li "+reg+","+str(variable)+"\n"
				
	else:

		maxnextuse=line
		reqvar=None
		for i in reg_desc.keys():
			print(line)
			print(symbol_attach[line])
			if (reg_desc[i] in symbol_attach[line]) and symbol_attach[line][reg_desc[i]][1] is not None:
				if symbol_attach[line][reg_desc[i]][1] > maxnextuse:
					reqvar=reg_desc[i]
					reg=i
					maxnextuse=symbol_attach[line][i][1]
			else:
				print(i)
				print(reg_desc[i])
				reg=i
				reqvar=reg_desc[i]
				break
		#move req var to memory
		addr_desc[reqvar]=["memory",None]
		if type(variable) is not int:
			reg_desc[reg]=variable
			addr_desc[variable]=["register",reg]
		mips+="sw "+reg+","+reqvar+"\n"
		# print(reg_desc[reg])
		if is_input:
			if type(variable) is not int:
				mips+="lw "+reg+","+variable+"\n"
			else:
				mips+="li "+reg+","+str(variable)+"\n"
	return reg

def generate_code(ir,block_start,block_end,symbol_attach):
	global addr_desc
	global reg_desc
	global mips
	global is_exit
	is_exit = True
	print(block_start,block_end)
	for i in range(block_start,block_end+1):
		if i==block_end:
			print(ir[i].lineno)
		if ir[i].typ != "label":
			mips+="line"+str(ir[i].lineno)+": \n"
		if i==block_end and ir[i].typ in ["ifgoto","goto","call"]:
			end_block(symbol_attach,ir[i].lineno-1)
		if ir[i].typ=="assign" or ir[i].typ=="arithmetic" or ir[i].typ == "ref" or ir[i].typ == "deref" or ir[i].typ == "assign_refval" or ir[i].typ == "assign_to_array" or ir[i].typ == "assign_from_array":
			if (ir[i].op=="+" or ir[i].op == "++" or ir[i].op == "+="):
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="add "+reg3+","+reg1+","+reg2+"\n"
			
			elif (ir[i].op=="-" or ir[i].op == "--" or ir[i].op == "-="):
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="sub "+reg3+","+reg1+","+reg2+"\n"

			elif (ir[i].op=="*" or ir[i].op == "*="):
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="mult "+reg1+","+reg2+"\n"
				mips+="mflo "+reg3+"\n"
			elif (ir[i].op=="/" or ir[i].op == "/="): 
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="div "+reg1+","+reg2+"\n"
				mips+="mflo "+reg3+"\n"
			elif (ir[i].op=="%" or ir[i].op == "%="):
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
				reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
				mips+="div "+reg1+","+reg2+"\n"
				mips+="mfhi "+reg3+"\n"


			elif ir[i].op == "=":
				if ir[i].typ == "ref":
					reg2 = getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips += "la "+reg2+","+ir[i].in1+"\n"
				elif ir[i].typ == "deref":
					reg1 = getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2 = getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips += "lw "+reg2+","+"0("+reg1+")\n"
				elif ir[i].typ == "assign_refval":
					reg1 = getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2 = getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips += "sw "+reg1+","+"0("+reg2+")\n"
				elif ir[i].typ == "assign_to_array":
					reg1=getreg(ir[i],ir[i].out,symbol_attach,i,True)
					reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					if not type(ir[i].in1) is int:
						mips+="sw "+reg3+","+str(ir[i].in1)+"\n"
					mips+="add "+reg3+","+reg3+","+reg3+"\n"
					mips+="add "+reg3+","+reg3+","+reg3+"\n"
					mips+="add "+reg1+","+reg1+","+reg3+"\n"
					mips+="sw "+reg2+",0("+reg1+")\n"
					mips+="lw "+reg1+","+ir[i].out+"\n"
					if not type(ir[i].in1) is int:
						mips+="lw "+reg3+","+str(ir[i].in1)+"\n"
				elif ir[i].typ == "assign_from_array":
					reg1=getreg(ir[i],ir[i].out,symbol_attach,i,False)
					reg2=getreg(ir[i],ir[i].in1,symbol_attach,i,True)#array pointer
					reg3=getreg(ir[i],ir[i].in2,symbol_attach,i,True)#array index
					if not type(ir[i].in2) is int:
						mips+="sw "+reg3+","+str(ir[i].in2)+"\n"
					mips+="add "+reg3+","+reg3+","+reg3+"\n"
					mips+="add "+reg3+","+reg3+","+reg3+"\n"
					mips+="add "+reg2+","+reg2+","+reg3+"\n"
					mips+="lw "+reg1+",0("+reg2+")\n"
					mips+="lw "+reg2+","+ir[i].in1+"\n"
					if not type(ir[i].in2) is int:
						mips+="lw "+reg3+","+str(ir[i].in2)+"\n"
				else:
					if type(ir[i].in1) is int:
						reg1=getreg(ir[i],ir[i].out,symbol_attach,i,False)
						mips+="li "+reg1+","+str(ir[i].in1)+"\n"
					else:	
						reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,False)
						reg2=getreg(ir[i],ir[i].out,symbol_attach,i,False)
						mips+="move "+reg2+","+reg1+"\n"
		elif ir[i].typ=="logical":									#logical operaters
				if (ir[i].op=="|" or ir[i].op == '|='):
					reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips+="or "+reg3+","+reg1+","+reg2+"\n"
				elif (ir[i].op=="^" or ir[i].op == '^='):
					reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips+="xor "+reg3+","+reg1+","+reg2+"\n"
				elif (ir[i].op==">>" or ir[i].op == '>>='):
					reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips+="srlv "+reg3+","+reg1+","+reg2+"\n"
					
				elif (ir[i].op=="<<" or ir[i].op == '<<='):
					reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips+="sllv "+reg3+","+reg1+","+reg2+"\n"
				elif (ir[i].op=="&" or ir[i].op == '&='):
					reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3=getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips+="and "+reg3+","+reg1+","+reg2+"\n"
				elif ir[i].op == "~":
					reg1 = getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg3 = getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips +="nor "+reg3+","+reg1+","+reg1+"\n"
				elif ir[i].op == "~|":
					reg1 = getreg(ir[i],ir[i].in1,symbol_attach,i,True)
					reg2 = getreg(ir[i],ir[i].in2,symbol_attach,i,True)
					reg3 = getreg(ir[i],ir[i].out,symbol_attach,i,False)
					mips += "nor "+reg3+","+reg1+","+reg2+"\n"
		elif ir[i].typ=="array":
			reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
			mips+="sll $a0,"+reg1+",2\n"
			mips+="li $v0,9\n"
			mips+="syscall\n"
			mips+="sw $v0,"+ir[i].out+"\n"
		elif ir[i].typ=="print":
			reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
			mips+="li $v0,1\n"
			mips+="move $a0,"+reg1+"\n"
			mips+="syscall\n"
		elif ir[i].typ=="puts":
			mips+="la $a0,"+"str"+str(ir[i].lineno)+"\n"
			mips+="li $v0,4\n"
			mips+="syscall\n"
		elif ir[i].typ=="scan":
			reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
			mips+="li $v0,5\n"
			mips+="syscall\n"
			mips+="move "+reg1+",$v0"+"\n"
		elif ir[i].typ == "label":
			mips+=ir[i].in1+":\n"
			is_exit = False;
		elif ir[i].typ == "call":
			mips+="jal "+ir[i].in1 + "\n"
			if ir[i].in2 != None:
				mips+="sw $v0,"+ir[i].in2+"\n"
		elif ir[i].typ == "ret":
			if ir[i].in1 != None:
				reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
				mips+="move $v0,"+reg1+"\n"
			if is_exit == False:
				mips+="jr $ra\n"
				is_exit = True
			else:
				mips+="li $v0,10\n"
				mips+="syscall\n"
				is_exit = False
		elif ir[i].typ=="ifgoto":
			reg1=getreg(ir[i],ir[i].in1,symbol_attach,i,True)
			reg2=getreg(ir[i],ir[i].in2,symbol_attach,i,True)
			if ir[i].op=="<=":
				if type(ir[i].target) is int:
					mips+="ble "+reg1+","+reg2+",line"+str(ir[i].target)+"\n"
				else:
					mips+="ble "+reg1+","+reg2+","+ir[i].target+"\n"
			elif ir[i].op==">=":
				if type(ir[i].target) is int:
					mips+="bge "+reg1+","+reg2+",line"+str(ir[i].target)+"\n"
				else:
					mips+="bge "+reg1+","+reg2+","+ir[i].target+"\n"
			elif ir[i].op=="<":
				if type(ir[i].target) is int:
					mips+="blt "+reg1+","+reg2+",line"+str(ir[i].target)+"\n"
				else:
					mips+="blt "+reg1+","+reg2+","+ir[i].target+"\n"
			elif ir[i].op==">":
				if type(ir[i].target) is int:
					mips+="bgt "+reg1+","+reg2+",line"+str(ir[i].target)+"\n"
				else:
					mips+="bgt "+reg1+","+reg2+","+ir[i].target+"\n"
			elif ir[i].op=="==":
				if type(ir[i].target) is int:
					mips+="beq "+reg1+","+reg2+",line"+str(ir[i].target)+"\n"
				else:
					mips+="beq "+reg1+","+reg2+","+ir[i].target+"\n"
			elif ir[i].op=="!=":
				if type(ir[i].target) is int:
					mips+="bne "+reg1+","+reg2+",line"+str(ir[i].target)+"\n"
				else:
					mips+="bne "+reg1+","+reg2+","+ir[i].target+"\n"
		elif ir[i].typ=="goto":
			mips+="j line"+str(ir[i].target)+"\n"
		if i==block_end and ir[i].typ not in ["ifgoto","goto","call"]:
			end_block(symbol_attach,ir[i].lineno-1)
			print(symbol_attach[ir[i].lineno-1],ir[i].lineno-1)
			pass
			return mips