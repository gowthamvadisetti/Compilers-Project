#To Supply data structures to code generator
import sys
class Instruction3AC:
	typ=""#if goto,goto,assignemnt,arithmetic
	in1=""
	in2=""
	out=""
	target=None
	lineno=None
	op=""	#=,+,-,*,/,%,ifgoto,call,ret,label,print,scan

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
			pass
		elif words[1]=="ifgoto":
			ir[curr].typ="ifgoto"
			ir[curr].op=words[2]
			ir[curr].in1=words[3]
			ir[curr].in2=words[4]
			ir[curr].target=int(words[5])
			leaders.append(int(words[5]))
			leaders.append(ir[curr].lineno+1)
		elif words[1]=="call":
			pass
		elif words[1]=="ret":
			pass
		elif words[1]=="label":
			pass
		elif words[1]=="print":
			pass
		elif words[1]=="scan":
			pass
		curr+=1

ir=[]
leaders=[1]
file_location=sys.argv[1]
parse_input(file_location,ir,leaders)
print(ir[0].typ)
print(leaders)