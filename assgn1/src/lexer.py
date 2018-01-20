import ply.lex as lex
import sys
file_location=sys.argv[1]

#token specification
tokens=['NAME','NUMBER','PLUS']
t_PLUS=r'\+'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

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
print file_contents
lex.input(file_contents) #give ruby file input
while True:
	tok=lex.token()
	if not tok:
		break
	else:
		print tok.type,tok.value