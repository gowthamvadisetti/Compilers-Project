import ply.yacc as yacc
import lexer
import sys
from main import *
tokens=lexer.tokens
counter=0
number_map={}
children_map={}
curr_derivation=[]
html=""
ir_code=[]

st=SymbolTable()

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
            | break
            | expr
    '''
    global ir_code
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None
    ir_code+=p[0].code


def p_expr(p):
    '''expr : if expr1 pthen compstmt end
            | if expr1 pthen compstmt multelsif else compstmt end
            | while expr1 pdo compstmt end
            | case compstmt multcase else compstmt end
            | case compstmt multcase end
            | for mlhs in expr1 pdo compstmt end
            | expr1
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None

def p_expr1(p):
    '''expr1 : return callargs
            | return OPEN_BRACKET callargs CLOSE_BRACKET
            | return OPEN_BRACKET CLOSE_BRACKET
            | return
            | expr2
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None

def p_expr2(p):
    '''expr2 : call
            | arg
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None

def p_call(p):
    '''call : function
    '''
    getRule(p,'call')

def p_function(p):
    '''function : IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
                | IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
    '''
    getRule(p,'function')

def p_arg(p):
    '''arg : arg BIT_OR term0
           | term0
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None

def p_term0(p):
    '''term0 : mlhs EQUALS IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
           | mlhs EQUALS IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
           | mlhs opasgn IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
           | term1
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None

def p_term1(p):
    '''term1 : mlhs EQUALS mrhs
              | mlhs opasgn mrhs
              | term2
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=None
    else:
        p[0]=SDT()
        st.insert(p[1].place,"int")
        p[0].code=p[3].code+[Instruction3AC(None,p[2],p[1].place,p[3].place,None,None)]
        p[0].place=p[1].place

def p_term2(p):
    '''term2 : term3 INCL_RANGE term3
            | term3 EXCL_RANGE term3
            | term3
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place

def p_term3(p):
    '''term3 : term3 LOGICAL_OR term4
            | term4
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None)]
        p[0].place=temp

def p_term4(p):
    '''term4 : term5 DOUBLE_EQUALS term5
             | term5 TRIPLE_EQUALS term5
             | term5 NOT_EQUALS term5
             | term5 EQUAL_TILDE term5
             | term5 BANG_TILDE term5
             | term5 COMPARISON term5
            | term5
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code
        p[0].code+=[Instruction3AC("ifgoto",p[2],None,p[1].place,p[3].place,3)]
        p[0].code+=[Instruction3AC(None,"=",temp,"0",None,None)]
        p[0].code+=[Instruction3AC("goto",None,None,None,None,2)]
        p[0].code+=[Instruction3AC(None,"=",temp,"1",None,None)]
        p[0].place=temp

def p_term5(p):
    '''term5 : term5 LESS term6
            | term5 LESS_EQUALS term6
            | term5 GREATER term6
            | term5 GREATER_EQUALS term6
            | term6
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code
        p[0].code+=[Instruction3AC("ifgoto",p[2],None,p[1].place,p[3].place,3)]
        p[0].code+=[Instruction3AC(None,"=",temp,"0",None,None)]
        p[0].code+=[Instruction3AC("goto",None,None,None,None,2)]
        p[0].code+=[Instruction3AC(None,"=",temp,"1",None,None)]
        p[0].place=temp

def p_term6(p):
    '''term6 : term6 BIT_XOR term7
            | term7
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None)]
        p[0].place=temp

def p_term7(p):
    '''term7 : term7 BIT_AND term8
            | term8
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None)]
        p[0].place=temp

def p_term8(p):
    '''term8 : term8 LEFT_SHIFT term9
            | term8 RIGHT_SHIFT term9
            | term9
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None)]
        p[0].place=temp

def p_term9(p):
    '''term9 : term9 PLUS term10
            | term9 MINUS term10
            | term10
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None)]
        p[0].place=temp

def p_term10(p):
    '''term10 : term10 MULTIPLY term11
            | term10 DIVIDE term11
            | term10 MODULO term11
            | term11
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None)]
        p[0].place=temp

def p_term11(p):
    '''term11 : MINUS term11
            | term12
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[2].code+[Instruction3AC(None,"*",temp,"-1",p[2].place,None)]
        p[0].place=temp

def p_term12(p):
    '''term12 : PLUS term12
            | term13
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
    else:
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[2].code+[temp+"="+p[2].place]
        p[0].code=p[2].code+[Instruction3AC(None,"*",temp,"1",p[2].place,None)]
        p[0].place=temp

def p_term13(p):
    '''term13 : primary POWER term13
            | primary
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place

def p_primary(p):
    '''primary : OPEN_BRACKET expr2 CLOSE_BRACKET
            | variable CONSTANT_RESOLUTION IDENTIFIER
            | CONSTANT_RESOLUTION IDENTIFIER
            | OPEN_SQUARE args COMMA CLOSE_SQUARE
            | OPEN_SQUARE args CLOSE_SQUARE
            | OPEN_SQUARE CLOSE_SQUARE
            | literal
            | varname
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place


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
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=[]
        if p[1] == "true":
            p[1]=1
        elif p[1] == "false":
            p[1]=0
        p[0].place=str(p[1])
        # print(p[0].code)

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
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=[]

def p_multmlhs(p):
    '''multmlhs : COMMA mlhsitem multmlhs
                | empty
    '''
    getRule(p,'multmlhs')

def p_mlhsitem(p):
    '''mlhsitem : IDENTIFIER
                | OPEN_BRACKET mlhs CLOSE_BRACKET
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1]
        p[0].code=[]

def p_lhs(p):
    '''lhs : variable
           | variable OPEN_SQUARE args CLOSE_SQUARE
           | variable OPEN_SQUARE CLOSE_SQUARE
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=p[1].code

def p_mrhs(p):
    '''mrhs : term2
            | args COMMA MULTIPLY arg
            | MULTIPLY arg
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=p[1].code
        # print(p[0].place)

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
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=[]

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
    if len(p[1:]) == 1:
        if st.lookup(p[1]):
            p[0]=SDT()
            p[0].place=p[1]
            p[0].code=[]
        else:
            print("Error not declared")

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
output_location=file_location.replace(".rb",".ir")
Print3AC(ir_code,output_location)