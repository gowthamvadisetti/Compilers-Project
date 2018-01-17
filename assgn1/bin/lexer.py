import ply.lex as lex
import sys
file_location=sys.argv[1]

#token specification
tokens=['NAME','NUMBER','PLUS']
t_PLUS=r'\+'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

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