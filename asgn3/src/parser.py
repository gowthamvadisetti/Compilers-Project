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
                | stmt newline
                | stmt newline expr
                | stmt newline expr newline
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_stmt(p):
    '''stmt : call do BIT_OR blockvar BIT_OR compstmt end
            | call do BIT_OR BIT_OR compstmt end
            | call do compstmt end
            | undef fname
            | alias fname fname
            | stmt if expr
            | stmt while expr
            | stmt unless expr
            | stmt until expr
            | BEGIN OPEN_FLOWER compstmt CLOSE_FLOWER
            | END OPEN_FLOWER compstmt CLOSE_FLOWER
            | lhs EQUALS command do BIT_OR blockvar BIT_OR compstmt end
            | lhs EQUALS command do BIT_OR BIT_OR compstmt end
            | lhs EQUALS command do compstmt end
            | lhs EQUALS command
            | expr
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_expr(p):
    '''expr : mlhs EQUALS mrhs
            | return callargs
            | yield callargs
            | expr and expr
            | expr or expr
            | not expr
            | command
            | SYMBOL_NOT command
            | arg
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_call(p):
    '''call : function
            | command
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_command(p):
    '''command : operation callargs
               | primary DOT operation callargs
               | primary CONSTANT_RESOLUTION operation callargs
               | super callargs
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])


def p_function(p):
    '''function : operation OPEN_BRACKET callargs CLOSE_BRACKET
                | operation OPEN_BRACKET CLOSE_BRACKET
                | operation
                | primary DOT operation OPEN_BRACKET callargs CLOSE_BRACKET
                | primary DOT operation OPEN_BRACKET CLOSE_BRACKET
                | primary CONSTANT_RESOLUTION operation OPEN_BRACKET callargs CLOSE_BRACKET
                | primary CONSTANT_RESOLUTION operation OPEN_BRACKET CLOSE_BRACKET
                | primary DOT operation
                | primary CONSTANT_RESOLUTION operation
                | super OPEN_BRACKET callargs CLOSE_BRACKET
                | super OPEN_BRACKET CLOSE_BRACKET
                | super
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_arg_equals(p):
    '''arg : lhs EQUALS arg
           | lhs opasgn arg
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
        | primary CONSTANT_RESOLUTION IDENTIFIER
        | CONSTANT_RESOLUTION IDENTIFIER
        | primary OPEN_SQUARE args CLOSE_SQUARE
        | primary OPEN_SQUARE CLOSE_SQUARE
        | OPEN_SQUARE args COMMA CLOSE_SQUARE
        | OPEN_SQUARE args CLOSE_SQUARE
        | OPEN_SQUARE CLOSE_SQUARE
        | OPEN_FLOWER args COMMA CLOSE_FLOWER
        | OPEN_FLOWER args CLOSE_FLOWER
        | OPEN_FLOWER CLOSE_FLOWER
        | OPEN_FLOWER assocs COMMA CLOSE_FLOWER
        | OPEN_FLOWER assocs CLOSE_FLOWER
        | return OPEN_BRACKET callargs CLOSE_BRACKET
        | return OPEN_BRACKET CLOSE_BRACKET
        | return
        | yield OPEN_BRACKET callargs CLOSE_BRACKET
        | yield OPEN_BRACKET CLOSE_BRACKET
        | yield
        | defined OPEN_BRACKET arg CLOSE_BRACKET
        | function
        | function OPEN_FLOWER BIT_OR blockvar BIT_OR compstmt CLOSE_FLOWER
        | function OPEN_FLOWER BIT_OR BIT_OR compstmt CLOSE_FLOWER
        | function OPEN_FLOWER compstmt CLOSE_FLOWER
        | if expr pthen compstmt multelsif else compstmt end
        | if expr pthen compstmt end
        | unless expr pthen compstmt else compstmt end
        | unless expr pthen compstmt end
        | while expr pdo compstmt end
        | until expr pdo compstmt end
        | case compstmt multcase else compstmt end
        | case compstmt multcase end
        | for blockvar in expr pdo compstmt end
        | class IDENTIFIER LESS IDENTIFIER compstmt end
        | class IDENTIFIER compstmt end
        | module IDENTIFIER compstmt end
        | def fname argdecl compstmt end
        | def singleton DOT fname argdecl compstmt end
        | def singleton CONSTANT_RESOLUTION fname argdecl compstmt end
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_multcase(p):
    '''multcase : when whenargs pthen compstmt multcase
                | when whenargs pthen compstmt
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
               | STRING2
               | HEREDOC
               | REGEXP
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

def p_whenargs(p):
    '''whenargs : args COMMA MULTIPLY arg
                | args
                | MULTIPLY arg
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_mlhs(p):
    '''mlhs : mlhsitem COMMA mlhsitem multmlhs MULTIPLY lhs
            | mlhsitem COMMA mlhsitem multmlhs MULTIPLY
            | mlhsitem COMMA mlhsitem multmlhs
            | mlhsitem COMMA MULTIPLY lhs
            | mlhsitem COMMA MULTIPLY
            | mlhsitem COMMA
    '''
    if len(p)>2:
        p[0] = tuple(p[1:])
    else:
        p[0] = (p[1])

def p_multmlhs(p):
    '''multmlhs : COMMA mlhsitem multmlhs
                | empty
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
                | MULTIPLY arg COMMA BIT_AND arg
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
    '''multassocs : COMMA assoc multassocs
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