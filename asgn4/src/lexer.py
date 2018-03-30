import ply.lex as lex
import sys

file_location=sys.argv[1]

#token declaration

#token specification
keywords=['BEGIN','class','ensure','nil','self','when','END',
			'def','false','not','super','while','alias',
			'defined','for','or','then','yield','and',
			'do','if','redo','true','begin','else','in','rescue',
			'undef','break','elsif','module','retry','unless','case',
			'end','next','return','until','Array','puts','print']

operators=['CONSTANT_RESOLUTION','ELEMENT_REFERENCE','ELEMENT_SET',
			'POWER','SYMBOL_NOT',
			'COMPLEMENT','MULTIPLY','DIVIDE','MODULO','PLUS',
			'MINUS','LEFT_SHIFT','RIGHT_SHIFT','BIT_AND','BIT_OR',
			'BIT_XOR','GREATER','GREATER_EQUALS','LESS','LESS_EQUALS',
			'COMPARISON','DOUBLE_EQUALS','TRIPLE_EQUALS','NOT_EQUALS',
			'EQUAL_TILDE','BANG_TILDE','LOGICAL_AND','LOGICAL_OR',
			'INCL_RANGE','EXCL_RANGE','EQUALS','MODULO_EQUALS',
			'DIVIDE_EQUALS','MINUS_EQUALS','PLUS_EQUALS','OR_EQUALS',
			'AND_EQUALS','XOR_EQUALS','RIGHT_SHIFT_EQUALS','LEFT_SHIFT_EQUALS',
			'MULTIPLY_EQUALS','LOGICAL_AND_EQUALS','LOGICAL_OR_EQUALS',
			'POWER_EQUALS','WORD_NOT','WORD_AND','WORD_OR','MAP','PLUS_AT','MINUS_AT']

tokens=keywords+operators+['IDENTIFIER','FLOAT','NUMBER','GLOBAL','STRING','STRING2',
							'HEREDOC','REGEXP','DOUBLE_QUOTE','DOLLAR','COLON','QUESTION_MARK',
							'OPEN_BRACKET','CLOSE_BRACKET','OPEN_FLOWER','CLOSE_FLOWER','OPEN_SQUARE',
							'CLOSE_SQUARE','COMMA','DOT','SEMI_COLON','AT_THE_RATE']+['NEWLINE']

reserved={}

for word in keywords:
	reserved[word]=word
#token specification
t_CONSTANT_RESOLUTION=r'::'
t_ELEMENT_REFERENCE=r'\[\]'
t_ELEMENT_SET=r'\[\]='
t_POWER=r'\*\*'
t_SYMBOL_NOT=r'!'
t_COMPLEMENT=r'~'
t_MULTIPLY=r'\*'
t_DIVIDE=r'/'
t_MODULO=r'%'
t_PLUS=r'\+'
t_MINUS=r'\-'
t_LEFT_SHIFT=r'<<'
t_RIGHT_SHIFT=r'>>'
t_BIT_AND=r'&'
t_BIT_OR=r'\|'
t_BIT_XOR=r'\^'
t_GREATER=r'>'
t_GREATER_EQUALS=r'>='
t_LESS=r'<'
t_LESS_EQUALS=r'<='
t_COMPARISON=r'<=>'
t_DOUBLE_EQUALS=r'=='
t_TRIPLE_EQUALS=r'==='
t_NOT_EQUALS=r'!='
t_EQUAL_TILDE=r'=~'
t_BANG_TILDE=r'!~'
t_LOGICAL_AND=r'&&'
t_LOGICAL_OR=r'\|\|'
t_INCL_RANGE=r'\.\.'
t_EXCL_RANGE=r'\.\.\.'
t_EQUALS=r'='
t_MODULO_EQUALS=r'%='
t_DIVIDE_EQUALS=r'/='
t_MINUS_EQUALS=r'\-='
t_PLUS_EQUALS=r'\+='
t_OR_EQUALS=r'\|='
t_AND_EQUALS=r'&='
t_XOR_EQUALS=r'\^='
t_RIGHT_SHIFT_EQUALS=r'>>='
t_LEFT_SHIFT_EQUALS=r'<<='
t_MULTIPLY_EQUALS=r'\*='
t_LOGICAL_AND_EQUALS=r'&&='
t_LOGICAL_OR_EQUALS=r'\|\|='
t_POWER_EQUALS=r'\*\*='
t_WORD_NOT=r'not'
t_WORD_AND=r'and'
t_WORD_OR=r'or'
t_MAP=r'=>'
t_PLUS_AT=r'\+@'
t_MINUS_AT=r'\-@'

def t_IDENTIFIER(t):
	r'[a-zA-Z_][a-zA-Z_0-9_]*'
	t.type = reserved.get(t.value,'IDENTIFIER')# Check for reserved words
	return t

def t_FLOAT(t):
	r'\d+\.\d+'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

t_GLOBAL=r'(\$[a-zA-Z_][a-zA-Z_0-9_]*)|(\$\-.)|(\$.)'
t_STRING=r'\'([^\\\']+|\\.)*\' | \"([^\\\"]+|\\.)*\"'
t_STRING2=r'%(Q|q|x)..*.'
t_HEREDOC=r'<<([a-zA-Z_][a-zA-Z_0-9_]*|(\".*\"|\'.*\'))\n.*\n[a-zA-Z_][a-zA-Z_0-9_]*'
t_REGEXP=r'(\/.*\/([iop])?)|(%r..*.)'
t_DOUBLE_QUOTE=r'\"'
t_DOLLAR=r'\$'
t_COLON=r':'
t_QUESTION_MARK=r'\?'
t_OPEN_BRACKET=r'\('
t_CLOSE_BRACKET=r'\)'
t_OPEN_FLOWER=r'\{'
t_CLOSE_FLOWER=r'\}'
t_OPEN_SQUARE=r'\['
t_CLOSE_SQUARE=r'\]'
t_COMMA=r'\,'
t_DOT=r'\.'
t_SEMI_COLON=r';'
t_AT_THE_RATE=r'\@'

t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	return t

def t_error(t):
	print("ILLEGAL CHARACTER '%s'" % t.value[0])
	t.lexer.skip(1)

#build the lexer
lex.lex()
fp=open(file_location,'r')
file_contents=fp.read()
lex.input(file_contents)