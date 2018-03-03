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

def p_compstmt(p):
    '''compstmt : stmt
                | newline stmt 
                | stmt newline
                | stmt newline expr
                | stmt newline expr newline
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_stmt(p):
    'stmt : expr'
    p[0]=(p[1])

def p_expr(p):
    'expr : arg'
    p[0]=(p[1])

def p_arg_equals(p):
    '''arg : lhs EQUALS arg
            | arg
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_arg_range(p):
    '''arg : term1 INCL_RANGE term1
            | term1 EXCL_RANGE term1
            | term1
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term1(p):
    '''term1 : term2 DOUBLE_EQUALS term2
            | term2
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term2(p):
    '''term2 : term2 LESS term3
            | term2 LESS_EQUALS term3
            | term2 GREATER term3
            | term2 GREATER_EQUALS term3
            | term3
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term3(p):
    '''term3 : term3 PLUS term4
            | term3 MINUS term4
            | term4
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term4(p):
    '''term4 : term4 MULTIPLY term5
            | term4 DIVIDE term5
            | term4 MODULO term5
            | term5
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term5(p):
    '''term5 : MINUS term5
            | term6
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_term6(p):
    '''term6 : PLUS term6
            | primary
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_primary(p):
    '''primary : OPEN_BRACKET compstmt CLOSE_BRACKET
        | literal
        | variable
        | if expr pthen compstmt multelsif else compstmt end
        | if expr pthen compstmt end
        | while expr pdo compstmt end
        | for blockvar in expr pdo compstmt end 
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_multelsif(p):
    '''multelsif : elsif expr pthen compstmt multelsif
                 | empty
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_literal(p):
    '''literal : NUMBER
               | symbol
               | STRING
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_blockvar(p):
    '''blockvar : lhs
                | mlhs
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_mlhs(p):
    '''mlhs : lhs
                | OPEN_BRACKET mlhs CLOSE_BRACKET
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_mlhsitem(p):
    '''mlhsitem : lhs
                | OPEN_BRACKET mlhs CLOSE_BRACKET
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_lhs(p):
    '''lhs : variable
           | primary OPEN_SQUARE args CLOSE_SQUARE
           | primary OPEN_SQUARE CLOSE_SQUARE
           | primary DOT IDENTIFIER 
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_mrhs(p):
    '''mrhs : args
            | args COMMA MULTIPLY arg
            | MULTIPLY arg
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_callargs(p):
    '''callargs : args
                | args COMMA assocs COMMA MULTIPLY arg COMMA BIT_AND arg
                | args COMMA MULTIPLY arg COMMA BIT_AND arg
                | args COMMA assocs COMMA BIT_AND arg
                | args COMMA assocs COMMA MULTIPLY arg
                | args COMMA assocs
                | args COMMA MULTIPLY arg
                | args COMMA BIT_AND arg
                | assocs COMMA MULTIPLY arg COMMA BIT_AND arg
                | assocs COMMA MULTIPLY arg
                | assocs COMMA BIT_AND arg
                | assocs
                | MULTPIPLY arg COMMA BIT_AND arg
                | BIT_AND arg
                | command
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_args(p):
    '''args : arg multargs
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_multargs(p):
    '''multargs : COMMA arg multargs
                | empty
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_argdecl(p):
    '''argdecl : OPEN_BRACKET arglist CLOSE_BRACKET
               | arglist newline
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_arglist(p):
    '''arglist : IDENTIFIER multarglist COMMA MULTIPLY IDENTIFIER COMMA BIT_AND IDENTIFIER
               | IDENTIFIER multarglist COMMA MULTIPLY COMMA BIT_AND IDENTIFIER
               | IDENTIFIER multarglist COMMA BIT_AND IDENTIFIER
               | IDENTIFIER multarglist COMMA MULTIPLY IDENTIFIER
               | IDENTIFIER multarglist COMMA MULTIPLY
               | IDENTIFIER multarglist
               | MULTIPLY IDENTIFIER COMMA BIT_AND IDENTIFIER
               | MULTIPLY IDENTIFIER
               | BIT_AND IDENTIFIER
               | empty
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_multarglist(p):
    '''multarglist : COMMA IDENTIFIER multarglist
                 | empty
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_singleton(p):
    '''singleton : variable
               | OPEN_BRACKET expr CLOSE_BRACKET
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_assocs(p):
    '''assocs : assoc multassocs
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_multassocs(p):
    '''multassocs : comma assoc multassocs
                  | empty
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_assoc(p):
    '''assoc : arg MAP arg
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_variable(p):
    '''variable : varname
                | nil
                | self
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_pthen(p):
    '''pthen : newline
             | then
             | newline then
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_pdo(p):
    '''pdo : newline
           | do
           | newline do
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_opasgn(p):
    '''opasgn : MODULO_EQUALS
              | DIVIDE_EQUALS
              | MINUS_EQUALS
              | PLUS_EQUALS
              | OR_EQUALS
              | AND_EQUALS
              | XOR_EQUALS
              | RIGHT_SHIFT_EQUALS
              | LEFT_SHIFT_EQUALS
              | MULTIPLY_EQUALS
              | LOGICAL_AND_EQUALS
              | LOGICAL_OR_EQUALS
              | POWER_EQUALS
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])
def p_symbol(p):
    '''symbol : COLON fname
              | COLON varname
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_fname(p):
    '''fname : IDENTIFIER
             | INCL_RANGE
             | BIT_OR
             | BIT_XOR
             | BIT_AND
             | COMPARISON
             | DOUBLE_EQUALS
             | TRIPLE_EQUALS
             | EQUAL_TILDE
             | GREATER
             | GREATER_EQUALS
             | LESS
             | LESS_EQUALS
             | PLUS
             | MINUS
             | MULTIPLY
             | DIVIDE
             | MODULO
             | POWER
             | LEFT_SHIFT
             | RIGHT_SHIFT
             | COMPLEMENT
             | PLUS_AT
             | MINUS_AT
             | ELEMENT_REFERENCE
             | ELEMENT_SET
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_operation(p):
    '''operation  : IDENTIFIER
                | IDENTIFIER SYMBOL_NOT
                | IDENTIFIER QUESTION_MARK
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_varname(p):
    '''varname : GLOBAL 
              | AT_THE_RATE IDENTIFIER
              | IDENTIFIER
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_newline(p):
    '''newline : SEMI_COLON
               | NEWLINE 
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])


#For epsilon definitions
def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print(p)
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