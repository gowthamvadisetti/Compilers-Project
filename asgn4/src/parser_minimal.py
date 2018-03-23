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


class SymbolTable():
    """docstring for ClassName"""
    def __init__(self):
        self.table={}
        self.tempcount=0        

    def insert(self,varname,vartype):
        self.table[varname]=vartype

    def lookup(self,varname):
        if varname in self.table:
            return self.table[varname]
        else:
            return None

    def newtemp(self):
        tempname="t"+str(self.tempcount)
        self.tempcount+=1
        return tempname

class SDT():
    def __init__(self):
        self.code=""
        self.place=None

st=SymbolTable()


file_location=sys.argv[1]

start='compstmt'

#The Actual Grammar Rules Below


def p_compstmt(p):
    '''compstmt : stmt2 NEWLINE stmt
    '''
    p[0]=SDT()
    p[0].code=p[1].code+"\n"+p[3].code
    p[0].place=None
    print(p[0].code)

def p_stmt2(p):
    '''stmt2 : IDENTIFIER EQUALS NUMBER
    '''
    p[0]=SDT()
    st.insert(p[1],"int")
    # print(st.table)
    p[0].code=p[1]+p[2]+str(p[3])
    p[0].place=None

def p_stmt(p):
    '''stmt : IDENTIFIER EQUALS term9
    '''
    p[0]=SDT()
    p[0].code=p[3].code+"\n"+p[1]+p[2]+p[3].place
    p[0].place=None

def p_term9(p):
    '''term9 : term9 PLUS IDENTIFIER
            | term9 MINUS IDENTIFIER
            | IDENTIFIER
    '''
    if len(p[1:]) == 1:
        if st.lookup(p[1]):
            p[0]=SDT()
            p[0].place=p[1]
            p[0].code=""
        else:
            print("Error not declared")
    else:
        if st.lookup(p[3]):
            p[0]=SDT()
            temp=st.newtemp()
            p[0].code=""+p[1].code+"\n"+temp+"="+p[1].place+p[2]+p[3]
            p[0].place=temp
        else:
            print("Error not declared")


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