import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
import lexer
import sys
tokens=lexer.tokens

file_location=sys.argv[1]

def p_stmt(p):
    '''stmt : stmt if expr
        | stmt while expr
        | expr'''
    p[0]=('expr',p[1])
def p_expr_plus(p):
    'expr : expr PLUS term'
    p[0] = tuple(p[1:])

def p_expr_minus(p):
    'expr : expr MINUS term'
    p[0] = tuple(p[1:])

def p_expr_term(p):
    'expr : term'
    print p[1:]
    p[0]=(p[1])

def p_term_factor(p):
    'term : factor'
    print(p[1:])
    p[0] = (p[1])

def p_factor_num(p):
    'factor : NUMBER'
    print p[1:]
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