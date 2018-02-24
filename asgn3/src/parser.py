import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
import lexer
import sys
tokens=lexer.tokens

file_location=sys.argv[1]

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+',p[1],p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-',p[1],p[3])

def p_expression_term(p):
    'expression : term'
    p[0]=(p[1])

def p_term_factor(p):
    'term : factor'
    p[0] = (p[1])

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('NUM',p[1])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

fp=open(file_location,'r')
file_contents=fp.read()
t=yacc.parse()
print(t)