import ply.yacc as yacc
from anytree import Node, RenderTree
# Get the token map from the lexer.  This is required.
import lexer
import sys
tokens=lexer.tokens
def createTree(root,tuple_part):
    curr=Node("",parent=root)
    if type(tuple_part) is tuple:
        for i in tuple_part:
            if type(i) is tuple:
                createTree(curr,i)
            else:
                endnode=Node(i,parent=curr)
    return

file_location=sys.argv[1]

def p_stmt(p):
    'stmt : expr'
    p[0]=(p[1])
def p_expr_plus(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | term
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term_factor(p):
    '''term : term MULTIPLY factor
            | term DIVIDE factor
            | term MODULO factor
            | factor
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_factor(p):
    'factor : NUMBER'
    p[0] = (p[1])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

fp=open(file_location,'r')
file_contents=fp.read()
t=yacc.parse()
root = Node("root")
createTree(root,t)
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
print(t)