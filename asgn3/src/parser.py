import ply.yacc as yacc
from anytree import Node, RenderTree
import lexer
import sys
import re
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
    curr_out=[]
    for i in curr_derivation:
        if i in children_map.keys():
            curr_out.append("<a>"+str(number_map[i])+"</a>")
        else:
            curr_out.append(str(number_map[i]))
    for j in range(len(curr_out)-1,-1,-1):
        if "<a>" in curr_out[j] and "</a>" in curr_out[j]:
            curr_out[j]=curr_out[j].replace("<a>","<b>")
            curr_out[j]=curr_out[j].replace("</a>","</b>")
            break
    curr_out=" ".join(curr_out)
    curr_out=curr_out.replace('\n','\\n')
    curr_out=curr_out.replace('None','&epsilon;')
    html+=curr_out+"</br>"
    if last_tuple is []:
        return
    else:
        for j in range(len(last_tuple)-1,-1,-1):
            rightDerivation(tuple_part[last_tuple[j]],last_tuple[j])

#Get list representaion at each BNF rule 
def getRule(p,node_name):
    # print(node_name)
    # print(p[1:])
    if len(p) > 0:
        p[0] = [node_name]+p[1:]
    else:
        p[0] = (p[1])

file_location=sys.argv[1]

start='compstmt'

#The Actual Grammar Rules Below

def p_compstmt(p):
    '''compstmt : multcompstmt
    '''
    getRule(p,'compstmt')

def p_multcompstmt(p):
    '''multcompstmt : newline stmt multcompstmt
                | stmt multcompstmt
                | newline
                | empty
    '''
    getRule(p,'multcompstmt')

def p_stmt(p):
    '''stmt : def IDENTIFIER argdecl compstmt end
            | def singleton DOT IDENTIFIER argdecl compstmt end
            | def singleton CONSTANT_RESOLUTION IDENTIFIER argdecl compstmt end
            | class IDENTIFIER LESS IDENTIFIER compstmt end
            | class IDENTIFIER compstmt end
            | break
            | expr
    '''
    getRule(p,'stmt')


def p_expr(p):
    '''expr : if expr1 pthen compstmt end
            | if expr1 pthen compstmt multelsif else compstmt end
            | while expr1 pdo compstmt end
            | until expr1 pdo compstmt end
            | case compstmt multcase else compstmt end
            | case compstmt multcase end
            | for mlhs in expr1 pdo compstmt end
            | expr1
    '''
    getRule(p,'expr1')

def p_expr1(p):
    '''expr1 : return callargs
            | return OPEN_BRACKET callargs CLOSE_BRACKET
            | return OPEN_BRACKET CLOSE_BRACKET
            | return
            | expr2
    '''
    getRule(p,'expr1')

def p_expr2(p):
    '''expr2 : call
            | arg
    '''
    getRule(p,'expr2')

def p_call(p):
    '''call : function
    '''
    getRule(p,'call')

def p_function(p):
    '''function : IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
                | IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
                | primary DOT IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
                | primary DOT IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
                | primary CONSTANT_RESOLUTION IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
                | primary CONSTANT_RESOLUTION IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
                | primary DOT IDENTIFIER
                | primary CONSTANT_RESOLUTION IDENTIFIER
    '''
    getRule(p,'function')

def p_arg(p):
    '''arg : arg BIT_OR term0
           | term0
    '''
    getRule(p,'arg')

def p_term0(p):
    '''term0 : mlhs EQUALS IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
           | mlhs EQUALS IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
           | mlhs opasgn IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
           | term1
    '''
    getRule(p,'term0')

def p_term1(p):
    '''term1 : mlhs EQUALS mrhs
              | mlhs opasgn mrhs
              | term2
    '''
    getRule(p,'term1')

def p_term2(p):
    '''term2 : term3 INCL_RANGE term3
            | term3 EXCL_RANGE term3
            | term3
    '''
    getRule(p,'term2')

def p_term3(p):
    '''term3 : term3 LOGICAL_OR term4
            | term4
    '''
    getRule(p,'term3')

def p_term4(p):
    '''term4 : term5 DOUBLE_EQUALS term5
             | term5 TRIPLE_EQUALS term5
             | term5 NOT_EQUALS term5
             | term5 EQUAL_TILDE term5
             | term5 BANG_TILDE term5
             | term5 COMPARISON term5
            | term5
    '''
    getRule(p,'term4')

def p_term5(p):
    '''term5 : term5 LESS term6
            | term5 LESS_EQUALS term6
            | term5 GREATER term6
            | term5 GREATER_EQUALS term6
            | term6
    '''
    getRule(p,'term5')

def p_term6(p):
    '''term6 : term6 BIT_XOR term7
            | term7
    '''
    getRule(p,'term6')

def p_term7(p):
    '''term7 : term7 BIT_AND term8
            | term8
    '''
    getRule(p,'term7')

def p_term8(p):
    '''term8 : term8 LEFT_SHIFT term9
            | term8 RIGHT_SHIFT term9
            | term9
    '''
    getRule(p,'term8')

def p_term9(p):
    '''term9 : term9 PLUS term10
            | term9 MINUS term10
            | term10
    '''
    getRule(p,'term9')

def p_term10(p):
    '''term10 : term10 MULTIPLY term11
            | term10 DIVIDE term11
            | term10 MODULO term11
            | term11
    '''
    getRule(p,'term10')

def p_term11(p):
    '''term11 : MINUS term11
            | term12
    '''
    getRule(p,'term11')

def p_term12(p):
    '''term12 : PLUS term12
            | term13
    '''
    getRule(p,'term12')

def p_term13(p):
    '''term13 : primary POWER term13
            | primary
    '''
    getRule(p,'term13')

def p_primary(p):
    '''primary : OPEN_BRACKET expr2 CLOSE_BRACKET
            | variable CONSTANT_RESOLUTION IDENTIFIER
            | CONSTANT_RESOLUTION IDENTIFIER
            | OPEN_SQUARE args COMMA CLOSE_SQUARE
            | OPEN_SQUARE args CLOSE_SQUARE
            | OPEN_SQUARE CLOSE_SQUARE
            | OPEN_FLOWER args COMMA CLOSE_FLOWER
            | OPEN_FLOWER args CLOSE_FLOWER
            | OPEN_FLOWER CLOSE_FLOWER
            | OPEN_FLOWER assocs COMMA CLOSE_FLOWER
            | OPEN_FLOWER assocs CLOSE_FLOWER
            | literal
            | lhs
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
               | STRING
               | true
               | false
    '''
    getRule(p,'literal')

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
            | mlhsitem
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
           | variable OPEN_SQUARE args CLOSE_SQUARE
           | variable OPEN_SQUARE CLOSE_SQUARE
           | variable DOT IDENTIFIER 
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
    print("Syntax error in input!")
    print("ERROR at line number:"+str(p.lineno)+" with token:"+str(p.type)+" and value:"+str(p.value))
    quit()

# Build the parser
parser = yacc.yacc(errorlog=yacc.NullLogger())
fp=open(file_location,'r')
file_contents=fp.read()
t=yacc.parse()
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