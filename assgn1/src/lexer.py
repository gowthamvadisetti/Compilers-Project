import ply.lex as lex
import sys
file_location=sys.argv[1]

#token specification
keywords=['BEGIN','class','ensure','nil','self','when','END','def','false','not','super','while','alias','defined','for','or','then','yield','and','do','if','redo','true','begin','else','in','rescue','undef','break','elsif','module','retry','unless','case','end','next','return','until']
tokens=keywords+['IDENTIFIER','NUMBER','PLUS']
t_PLUS=r'\+'

reserved={}

for word in keywords:
	reserved[word]=word

def t_IDENTIFIER(t):
	r'[a-zA-Z_][a-zA-Z_0-9_]*'
	t.type = reserved.get(t.value,'IDENTIFIER')# Check for reserved words
	return t

def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

t_ignore = "\t"

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

#build the lexer
lex.lex()
fp=open(file_location,'r')
file_contents=fp.read()
print file_contents+"\n\n\n"
lex.input(file_contents) #give ruby file input
print "TOKEN VALUE"
while True:
	tok=lex.token()
	if not tok:
		break
	else:
		print tok.type,tok.value