#To Supply data structures to code generator
import sys
import codegen
class Instruction3AC:
	typ=None#if goto,goto,assignemnt,arithmetic
	in1=None
	in2=None
	out=None
	target=None
	op=None	#=,+,-,*,/,%,ifgoto,call,ret,label,print,scan
	lineno=None

def parse_input(file_location,ir,leaders):
	#to read ir code to Instruction3AC format
	fp=open(file_location,'r')
	curr=0
	for line in fp:
		line=line.strip()
		words=line.split(",")
		ir.append(Instruction3AC())
		# print words[1]
		ir[curr].lineno=int(words[0])
		ir[curr].op=words[1]
		if words[1]=="=":
			ir[curr].typ="assign"
			ir[curr].in1=words[3]
			ir[curr].out=words[2]
		elif words[1] in ['+','-','*','/','%']:
			ir[curr].typ="arithmetic"
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
		elif words[1]=="call":
			ir[curr].typ="call"
			ir[curr].in1=words[2]
		elif words[1]=="ret":
			ir[curr].typ="ret"
		elif words[1]=="label":
			ir[curr].typ="label"
			ir[curr].in1=words[2]
		elif words[1]=="print":
			ir[curr].typ="print"
			ir[curr].in1=words[2]
		elif words[1]=="scan":
			ir[curr].typ="scan"
			ir[curr].out=words[2]
		curr+=1
	leaders=sorted(leaders)
	fp.close()
	return

def create_symbol_table(ir,leaders,symbol_table):
	'''need to separate blocks and deal with them individually
	first assign default values and then do back scanning to 
	assign proper values to each variable
	for each line a map {var name -> [live or dead,next use in line]}'''
	pass
ir=[]
leaders=[1]
symbol_table=[]
file_location=sys.argv[1]
parse_input(file_location,ir,leaders)
for i in ir:
	print i.in1,i.in2,i.out,i.typ,i.op
print(leaders)
'''better to separate blocks here itself or later?
what happens to symbol table for each block after it ends?

'''
create_symbol_table(ir,leaders,symbol_table)
codegen.generate_code(ir,leaders,symbol_table)