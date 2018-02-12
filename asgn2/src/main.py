#To Supply data structures to code generator
import sys
import codegen
import re
variables={}
string_vars={}
class Instruction3AC:
	typ=None#if goto,goto,assignemnt,arithmetic
	in1=None
	in2=None
	out=None
	target=None
	op=None	#=,+,-,*,/,%,~,~|,ifgoto,call,ret,label,print,scan
	lineno=None

def parse_input(file_location,ir,leaders):
	#to read ir code to Instruction3AC format
	global variables
	global string_vars
	fp=open(file_location,'r')
	curr=0
	for line in fp:
		line=line.strip()
		words=line.split(",")
		ir.append(Instruction3AC())
		for i in range(len(words)):
			try:
				words[i]=int(words[i])
			except:
				pass
		try:
			ir[curr].lineno=int(words[0])
		except:
			pass
		ir[curr].op=words[1]
		if words[1]=="=":
			try:
				match1=re.search('(.*?)\[(.*?)\]$',str(words[2]))
				match2=re.search('(.*?)\[(.*?)\]$',str(words[3]))
				if match1:
					ir[curr].typ="assign_to_array"
					ir[curr].out=match1.group(1)
					ir[curr].in1=match1.group(2)
					try:
						ir[curr].in1=int(ir[curr].in1)
					except:
						pass
					ir[curr].in2=words[3]
				elif match2:
					ir[curr].typ="assign_from_array"
					ir[curr].in1=match2.group(1)
					ir[curr].in2=match2.group(2)
					try:
						ir[curr].in2=int(ir[curr].in2)
					except:
						pass
					ir[curr].out=words[2]
				elif words[2][0] == "*":       #*a = b 
					ir[curr].typ = "assign_refval"
					ir[curr].in1 = words[3]
					ir[curr].out = words[2][1:]
				elif words[3][0] == "&":       # a = &b
					ir[curr].typ = "ref"
					ir[curr].in1=words[3][1:]
					ir[curr].out=words[2]
				elif words[3][0] == "*":      # a = *b
					ir[curr].typ = "deref"
					ir[curr].in1 = words[3][1:]
					ir[curr].out = words[2]
				else:
					ir[curr].typ="assign"
					ir[curr].in1=words[3]
					ir[curr].out=words[2]
			except:
				ir[curr].typ="assign"
				ir[curr].in1=words[3]
				ir[curr].out=words[2]	
		elif words[1]=="array":
			ir[curr].typ="array"
			match=re.search('(.*?)\[(.*?)\]$',words[2])
			if match:
				ir[curr].in1=match.group(2)
				try:
					ir[curr].in1=int(ir[curr].in1)
				except:
					pass
				ir[curr].out=match.group(1)
			else:
				print("Array declaration error")
		elif words[1] in ['+','-','*','/','%',"++","--"]:
			ir[curr].typ="arithmetic"
			if words[1] == "++":
				ir[curr].in1 = words[2]
				ir[curr].in2 = 1
				ir[curr].out = words[2]

			elif words[1] == "--":
				ir[curr].in1 = words[2]
				ir[curr].in2 = 1
				ir[curr].out = words[2]
			else:
				ir[curr].in1=words[3]
				ir[curr].in2=words[4]
				ir[curr].out=words[2] 
		elif words[1] in ['|','^','>>','<<','&','~','~|']:
			ir[curr].typ="logical"
			if words[1] == '~':
				ir[curr].in1=words[3]
				ir[curr].out=words[2]
			else:
				ir[curr].in1=words[3]
				ir[curr].in2=words[4]
				ir[curr].out=words[2]
		elif words[1]=="ifgoto":
			ir[curr].typ="ifgoto"
			ir[curr].op=words[2]
			ir[curr].in1=words[3]
			ir[curr].in2=words[4]
			ir[curr].target=int(words[5])
			leaders.append(int(words[5]))
			leaders.append(ir[curr].lineno+1)
		elif words[1]=="goto":
			ir[curr].typ="goto"
			ir[curr].target=int(words[2])
			leaders.append(int(words[2]))
			leaders.append(ir[curr].lineno+1)
		elif words[1]=="call":
			ir[curr].typ="call"
			ir[curr].in1=words[2]
			if (len(words)>3):
				ir[curr].in2=words[3]
		elif words[1]=="ret":
			ir[curr].typ="ret"
			if (len(words) > 2):
				ir[curr].in1=words[2]
		elif words[1]=="label":
			ir[curr].typ="label"
			ir[curr].in1=words[2]
		elif words[1]=="print":
			ir[curr].typ="print"
			ir[curr].in1=words[2]
		elif words[1]=="puts":
			ir[curr].typ="puts"
			ir[curr].in1=words[2]
		elif words[1]=="scan":
			ir[curr].typ="scan"
			ir[curr].in1=words[2]
		if ((ir[curr].typ != "label") and (ir[curr].typ != "puts") and (ir[curr].typ != "call")):
			variables[ir[curr].in1]=True
			variables[ir[curr].in2]=True
			variables[ir[curr].out]=True
		if(ir[curr].typ == "puts"):
			string_vars[ir[curr].lineno]=ir[curr].in1
		curr+=1
	leaders=sorted(leaders)
	fp.close()
	return

def create_symbol_table(ir,block_start,block_end,symbol_attach):
	symbol_table={}
	for i in range(block_start,block_end+1):

		if ir[i].typ=="assign" or ir[i].typ=="arithmetic":
			if type(ir[i].in1) is not int and (ir[i].in1) is not None:
				symbol_table[ir[i].in1]=["dead",None]
			if type(ir[i].in2) is not int and (ir[i].in2) is not None:
				symbol_table[ir[i].in2]=["dead",None]
			if type(ir[i].out) is not int and (ir[i].out) is not None:
				symbol_table[ir[i].out]=["live",None]

		elif ir[i].typ == "logical":
			if type(ir[i].in1) is not int and (ir[i].in1) is not None:
				symbol_table[ir[i].in1]=["dead",None]
			if type(ir[i].in2) is not int and (ir[i].in2) is not None:
				symbol_table[ir[i].in2]=["dead",None]
			if type(ir[i].out) is not int and (ir[i].out) is not None:
				symbol_table[ir[i].out]=["live",None]


	for i in range(block_end,block_start-1,-1):
		if ir[i].typ=="assign" or ir[i].typ=="arithmetic":
			if type(ir[i].in1) is not int and (ir[i].in1) is not None:
				symbol_attach[i]=symbol_table.copy()
				symbol_table[ir[i].in1]=["live",i]
			if type(ir[i].in2) is not int and (ir[i].in2) is not None:
				symbol_attach[i]=symbol_table.copy()
				symbol_table[ir[i].in2]=["live",i]
			if type(ir[i].out) is not int and (ir[i].out) is not None:
				symbol_attach[i]=symbol_table.copy()
				symbol_table[ir[i].out]=["dead",None]

		elif ir[i].typ == "logical":
			if type(ir[i].in1) is not int and (ir[i].in1) is not None:
				symbol_table[ir[i].in1]=["dead",None]
			if type(ir[i].in2) is not int and (ir[i].in2) is not None:
				symbol_table[ir[i].in2]=["dead",None]
			if type(ir[i].out) is not int and (ir[i].out) is not None:
				symbol_table[ir[i].out]=["live",None]


ir=[]
leaders=[1]
file_location=sys.argv[1]
parse_input(file_location,ir,leaders)
# for i in ir:
# 	print (i.in1,i.in2,i.out,i.typ,i.op)
print(leaders)
mips=""
mips+=".data\n"
for i in variables.keys():
	if i is not None and type(i) is not int:
		mips+=i+": .word 0\n"
for i in string_vars.keys():
	mips+="str"+str(i)+": .asciiz "+string_vars[i]+"\n"
mips+=".text\nmain:\n"
symbol_attach=[{} for i in range(len(ir))]
for i in range(len(leaders)):
	block_start=leaders[i]-1
	if i!=len(leaders)-1:
		block_end=leaders[i+1]-2
	else:
		block_end=len(ir)-1
	create_symbol_table(ir,block_start,block_end,symbol_attach)
	if i==len(leaders)-1:
		mips+=codegen.generate_code(ir,block_start,block_end,symbol_attach)
	else:
		temp=codegen.generate_code(ir,block_start,block_end,symbol_attach)
with open("mips/test1.asm","w") as fp:
	fp.write(mips)
print (mips)
# print(symbol_attach)