import ply.yacc as yacc
from anytree import Node, RenderTree
import lexer
import sys
tokens=lexer.tokens
counter=0
number_map={}
children_map={}
curr_derivation=[]
html=""

#For creating parse tree
def createTree(root,tuple_part):
    global children_map
    if type(tuple_part) is list:
        node_name=tuple_part[0]
        tuple_part=tuple_part[1:]
    else:
        node_name=""
    curr=Node(node_name,parent=root)
    if root.name in children_map:
        children_map[root.name].append(node_name)
    else:
        children_map[root.name]=[node_name]
    if type(tuple_part) is list:
        for i in tuple_part:
            if type(i) is list:
                createTree(curr,i)
            else:
                endnode=Node(i,parent=curr)
                if curr.name in children_map:
                    children_map[curr.name].append(i)
                else:
                    children_map[curr.name]=[i]
    return

#Numbering Variables to distinguish them
def number_tuple(tuple_repr):
    global counter
    global number_map
    for i in range(len(tuple_repr)):
        if type(tuple_repr[i]) is list:
            number_tuple(tuple_repr[i])
        else:
            number_map[counter]=tuple_repr[i]
            tuple_repr[i]=counter
            counter+=1

#Get right derivation from list representation
def rightDerivation(tuple_part,curr_tuple):
    global curr_derivation
    global number_map
    global children_map
    global html
    if type(tuple_part) is list:
        node_name=tuple_part[0]
        tuple_part=tuple_part[1:]
    else:
        node_name=""
    last_tuple=[]
    replace_derivation=[]
    if type(tuple_part) is list:
        for i in range(len(tuple_part)):
            if type(tuple_part[i]) is list:
                replace_derivation.append(tuple_part[i][0])
                last_tuple.append(i)
            else:
                replace_derivation.append(tuple_part[i])
    curr_tuple=curr_derivation.index(node_name)
    curr_derivation=curr_derivation[0:curr_tuple]+replace_derivation+curr_derivation[curr_tuple+1:]
    curr_out=""
    for i in curr_derivation:
        if i in children_map.keys():
            if last_tuple and tuple_part[last_tuple[-1]][0] == i:
                curr_out+="<b>"+str(number_map[i])+"</b>"+" "
            else:
                curr_out+="<b>"+str(number_map[i])+"</b>"+" "
        else:
            curr_out+=str(number_map[i])+" "
    # print(last_tuple)
    curr_out=curr_out.replace('\n','\\n')
    html+=curr_out+"</br>"
    if last_tuple is []:
        return
    else:
        for j in range(len(last_tuple)-1,-1,-1):
            rightDerivation(tuple_part[last_tuple[j]],last_tuple[j])

#Get list representaion at each BNF rule 
def getRule(p,node_name):
    print(node_name)
    # print(p[1:])
    if len(p) > 2:
        p[0] = [node_name]+p[1:]
    else:
        p[0] = (p[1])

file_location=sys.argv[1]

start='compstmt'

def p_compstmt(p):
    '''compstmt : multcompstmt
    '''
    getRule(p,'compstmt')

def p_multcompstmt(p):
    '''multcompstmt : newline expr multcompstmt
                | expr multcompstmt
                | newline
                | empty
    '''
    getRule(p,'multcompstmt')

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
    getRule(p,'stmt')

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
    getRule(p,'expr')

def p_call(p):
    '''call : function
            | command
    '''
    getRule(p,'call')

def p_command(p):
    '''command : operation callargs
               | primary DOT operation callargs
               | primary CONSTANT_RESOLUTION operation callargs
               | super callargs
    '''
    getRule(p,'command')


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
    getRule(p,'function')

def p_arg_equals(p):
    '''arg : lhs EQUALS arg
           | lhs opasgn arg
           | term0
    '''
    getRule(p,'arg')

def p_term0(p):
    '''term0 : term1 INCL_RANGE term1
            | term1 EXCL_RANGE term1
            | term1
    '''
    getRule(p,'term0')

def p_term1(p):
    '''term1 : term2 DOUBLE_EQUALS term2
            | term2
    '''
    getRule(p,'term1')

def p_term2(p):
    '''term2 : term2 LESS term3
            | term2 LESS_EQUALS term3
            | term2 GREATER term3
            | term2 GREATER_EQUALS term3
            | term3
    '''
    getRule(p,'term2')

def p_term3(p):
    '''term3 : term3 PLUS term4
            | term3 MINUS term4
            | term4
    '''
    getRule(p,'term3')

def p_term4(p):
    '''term4 : term4 MULTIPLY term5
            | term4 DIVIDE term5
            | term4 MODULO term5
            | term5
    '''
    getRule(p,'term4')

def p_term5(p):
    '''term5 : MINUS term5
            | term6
    '''
    getRule(p,'term5')

def p_term6(p):
    '''term6 : PLUS term6
            | primary
    '''
    getRule(p,'term6')

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
            | if expr pthen compstmt end
            | if expr pthen compstmt multelsif else compstmt end
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
    getRule(p,'primary')

def p_multcase(p):
    '''multcase : when whenargs pthen compstmt multcase
                | when whenargs pthen compstmt
    '''
    getRule(p,'multcase')

def p_multelsif(p):
    '''multelsif : elsif expr pthen compstmt multelsif
                 | empty
    '''
    getRule(p,'multelsif')

def p_literal(p):
    '''literal : NUMBER
               | FLOAT
               | symbol
               | STRING
               | STRING2
               | HEREDOC
               | REGEXP
    '''
    getRule(p,'literal')

def p_blockvar(p):
    '''blockvar : lhs
                | mlhs
    '''
    getRule(p,'blockvar')

def p_whenargs(p):
    '''whenargs : args COMMA MULTIPLY arg
                | args
                | MULTIPLY arg
    '''
    getRule(p,'whenargs')

def p_mlhs(p):
    '''mlhs : mlhsitem COMMA mlhsitem multmlhs MULTIPLY lhs
            | mlhsitem COMMA mlhsitem multmlhs MULTIPLY
            | mlhsitem COMMA mlhsitem multmlhs
            | mlhsitem COMMA MULTIPLY lhs
            | mlhsitem COMMA MULTIPLY
            | mlhsitem COMMA
    '''
    getRule(p,'mlhs')

def p_multmlhs(p):
    '''multmlhs : COMMA mlhsitem multmlhs
                | empty
    '''
    getRule(p,'multmlhs')

def p_mlhsitem(p):
    '''mlhsitem : lhs
                | OPEN_BRACKET mlhs CLOSE_BRACKET
    '''
    getRule(p,'mlhsitem')

def p_lhs(p):
    '''lhs : variable
           | primary OPEN_SQUARE args CLOSE_SQUARE
           | primary OPEN_SQUARE CLOSE_SQUARE
           | primary DOT IDENTIFIER 
    '''
    getRule(p,'lhs')

def p_mrhs(p):
    '''mrhs : args
            | args COMMA MULTIPLY arg
            | MULTIPLY arg
    '''
    getRule(p,'mrhs')

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
    getRule(p,'callargs')

def p_args(p):
    '''args : arg multargs
    '''
    getRule(p,'args')

def p_multargs(p):
    '''multargs : COMMA arg multargs
                | empty
    '''
    getRule(p,'multargs')

def p_argdecl(p):
    '''argdecl : OPEN_BRACKET arglist CLOSE_BRACKET
               | arglist newline
    '''
    getRule(p,'argdecl')

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
    getRule(p,'arglist')

def p_multarglist(p):
    '''multarglist : COMMA IDENTIFIER multarglist
                 | empty
    '''
    getRule(p,'multarglist')

def p_singleton(p):
    '''singleton : variable
               | OPEN_BRACKET expr CLOSE_BRACKET
    '''
    getRule(p,'singleton')

def p_assocs(p):
    '''assocs : assoc multassocs
    '''
    getRule(p,'assocs')

def p_multassocs(p):
    '''multassocs : COMMA assoc multassocs
                  | empty
    '''
    getRule(p,'multassocs')

def p_assoc(p):
    '''assoc : arg MAP arg
    '''
    getRule(p,'assoc')

def p_variable(p):
    '''variable : varname
                | nil
                | self
    '''
    getRule(p,'variable')

def p_pthen(p):
    '''pthen : newline
             | then
             | newline then
    '''
    getRule(p,'pthen')

def p_pdo(p):
    '''pdo : newline
           | do
           | newline do
    '''
    getRule(p,'pdo')

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
    getRule(p,'opasgn')
def p_symbol(p):
    '''symbol : COLON fname
              | COLON varname
    '''
    getRule(p,'symbol')

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
    getRule(p,'fname')

def p_operation(p):
    '''operation  : IDENTIFIER
                | IDENTIFIER SYMBOL_NOT
                | IDENTIFIER QUESTION_MARK
    '''
    getRule(p,'operation')

def p_varname(p):
    '''varname : GLOBAL 
              | AT_THE_RATE IDENTIFIER
              | IDENTIFIER
    '''
    getRule(p,'varname')

def p_newline(p):
    '''newline : SEMI_COLON
               | NEWLINE
    '''
    getRule(p,'newline')


#For epsilon definitions
def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Syntax error in input!")
    quit()

# Build the parser
parser = yacc.yacc()

fp=open(file_location,'r')
file_contents=fp.read()
t=yacc.parse()
# root = Node("root")
# createTree(root,t)
# for pre, fill, node in RenderTree(root):
#     print("%s%s" % (pre, node.name))
print(t)
curr_derivation=[0]
number_tuple(t)
root = Node(0)
createTree(root,t)
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre,number_map[node.name]))

html+='''<!DOCTYPE html>
<html>
<head>
<title>Right derivation</title>
</head>
<body>'''
html+="<b>compstmt</b></br>"
rightDerivation(t,0)
html+='''
</body>
</html>
'''
fp=open(file_location.replace(".rb",".html"),'w')
fp.write(html)
# print(html)