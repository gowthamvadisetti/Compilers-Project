import ply.yacc as yacc
import lexer
import sys
from main_parser import *
tokens=lexer.tokens
counter=0
number_map={}
children_map={}
curr_derivation=[]
html=""
ir_code=[]
func_code=[]

st=SymbolTable("",None)

file_location=sys.argv[1]

start='compstmt'
labelcount=0
def newlabel():
    global labelcount
    labelname="l"+str(labelcount)
    labelcount+=1
    return labelname

#The Actual Grammar Rules Below

def p_compstmt(p):
    '''compstmt : multcompstmt
    '''
    getRule(p,'compstmt')

def p_multcompstmt(p):
    '''multcompstmt : newline stmt1 multcompstmt
                | stmt1 multcompstmt
                | newline
                | empty
    '''
    getRule(p,'multcompstmt')

def p_stmt1(p):
    '''stmt1 : stmt
    '''
    global ir_code
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None
    ir_code+=p[0].code

def p_stmt(p):
    '''stmt : keydef argdecl newline multstmt keyend
            | puts OPEN_BRACKET STRING CLOSE_BRACKET
            | print OPEN_BRACKET primary CLOSE_BRACKET
            | gets OPEN_BRACKET IDENTIFIER CLOSE_BRACKET
            | class IDENTIFIER newline multstmt end
            | class IDENTIFIER LESS IDENTIFIER newline multstmt end
            | break
            | expr
    '''
    global func_code
    p[0]=SDT()
    if len(p[1:])== 1 and p[1]=="break":
        p[0].code=["break"]
        p[0].place=None
    elif len(p[1:])==1:
        p[0].code=p[1].code
        p[0].place=None
    elif p[1]=="puts":
        p[0].code=[Instruction3AC("puts",None,None,p[3],None,None,st.fname)]
        p[0].place=None
    elif p[1]=="print":
        p[0].code=[Instruction3AC("print",None,None,p[3].place,None,None,st.fname)]
        p[0].place=None
    elif p[1]=="gets":
        p[0].code=[Instruction3AC("scan",None,p[3],None,None,None,st.fname)]
        st.insert(p[3],"int")
        p[0].place=None
    elif p[1]=="class":
        p[0].code=[Instruction3AC("unimplemented",None,None,None,None,None,st.fname)]
    elif len(p[1:])==5:
        p[0].code=[]
        func_code+=p[1].code+p[2].code+p[4].code
        func_code+=[Instruction3AC("ret",None,None,None,None,None,st.fname)]
def p_keydef(p):
    '''keydef : def IDENTIFIER
    '''
    global st
    p[0]=SDT()
    temp=SymbolTable(p[2],st)
    st=temp
    p[0].code=[Instruction3AC("flabel",None,None,p[2],None,None,st.fname)]
    p[0].place=None
def p_keyend(p):
    '''keyend : end
    '''
    global st
    st=st.parent
def p_multstmt(p):
    '''multstmt : stmt newline multstmt
                | empty 
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=[]
        p[0].place=None
    elif len(p[1:]) == 3:
        p[0].code=p[1].code+p[3].code
        p[0].place=None



def p_expr(p):
    '''expr : if expr1 pthen M_1 multstmt else newline M_1 multstmt end M_1
            | if expr1 pthen M_1 multstmt M_1 multelsif end M_1
            | if expr1 pthen M_1 multstmt end M_1
            | while M_1 expr1 pdo M_1 multstmt end M_1
            | until M_1 expr1 pdo M_1 multstmt end M_1
            | case expr1 newline multcase end M_1
            | for M_1 mlhs in expr1 pdo M_1 multstmt end M_1
            | expr1
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    elif p[1]=="if" and len(p[1:]) == 11:
        p[0].code=p[2].code
        p[0].code+=[Instruction3AC("ifgoto",">",None,p[2].place,"0",p[4].label,st.fname)]
        p[0].code+=[Instruction3AC("goto",None,None,None,None,p[8].label,st.fname)]
        p[0].code+=p[4].code+p[5].code
        p[0].code+=[Instruction3AC("goto",None,None,None,None,p[11].label,st.fname)]
        p[0].code+=p[8].code+p[9].code+p[11].code

    elif p[1] == "if" and len(p[1:]) == 9:
        p[0].code = p[2].code
        p[0].code += [Instruction3AC("ifgoto", ">", None, p[2].place, "0", p[4].label,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[6].label,st.fname)]
        p[0].code += p[4].code+p[5].code
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[9].label,st.fname)]
        p[0].code += p[6].code+p[7].code
        p[0].code += p[9].code


    elif p[1]=="if" and len(p[1:]) == 7:
        p[0].code=p[2].code
        p[0].code+=[Instruction3AC("ifgoto",">",None,p[2].place,"0",p[4].label,st.fname)]
        p[0].code+=[Instruction3AC("goto",None,None,None,None,p[7].label,st.fname)]
        p[0].code+=p[4].code+p[5].code
        p[0].code+=p[7].code

    elif p[1]=="while":
        p[0].code = p[2].code
        p[0].code += p[3].code
        p[0].code += [Instruction3AC("ifgoto", ">", None, p[3].place, "0", p[5].label,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[8].label,st.fname)]
        for i in range(len(p[6].code)):
            if p[6].code[i]=="break":
                p[6].code[i]= Instruction3AC("goto", None, None, None, None, p[8].label,st.fname)
        p[0].code += p[5].code+p[6].code
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[2].label,st.fname)]
        p[0].code += p[8].code

    elif p[1]=="for":
        
        #print (p[3].place)
        low = str(p[5].place[0])
        high = str(p[5].place[1])
        new_lab = newlabel()
        counter = st.newtemp()
        p[0].code = p[3].code+p[5].code
        p[0].code += [Instruction3AC(None, "=", counter, low, None, None,st.fname)]

        p[0].code += p[2].code

        p[0].code += [Instruction3AC("ifgoto", ">=", None, counter, low, new_lab,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[10].label,st.fname)]
        p[0].code += [Instruction3AC("label", new_lab, None, None, None, None,st.fname)]
        p[0].code += [Instruction3AC("ifgoto","<=", None, counter, high, p[7].label,st.fname)]
        p[0].code += [Instruction3AC("goto",None,None,None,None,p[10].label,st.fname)]
        for i in range(len(p[8].code)):
            if p[8].code[i]=="break":
                p[8].code[i]=Instruction3AC("goto", None, None, None, None, p[10].label,st.fname)
        p[0].code += p[7].code + p[8].code
        p[0].code += [Instruction3AC(None, "+=", counter, None, "1", None,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[2].label,st.fname)]  
        p[0].code += p[10].code

    elif p[1] == "until":
        p[0].code = p[2].code+p[3].code
        p[0].code += [Instruction3AC("ifgoto", "==", None, p[3].place, "0", p[5].label,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[8].label,st.fname)]
        p[0].code += p[5].code+p[6].code
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[2].label,st.fname)]
        p[0].code += p[8].code
        
    elif p[1]=="case":
        for i in range(len(p[4].code)):
            if p[4].code[i].typ=="ifgoto":
                p[4].code[i].in1=p[2].place
        p[0].code = p[2].code
        p[0].code += p[4].code
        p[0].code += p[6].code



def p_M_1(p):
    '''M_1 : empty
    '''
    p[0]=SDT()
    label1=newlabel()
    p[0].code=[Instruction3AC("label",None,None,label1,None,None,st.fname)]
    p[0].label=label1

def p_expr1(p):
    '''expr1 : return term2
            | return
            | expr2
    '''
    p[0]=SDT()
    if (len(p[1:]) == 1) and p[1]=="return":
        p[0].code=[Instruction3AC("ret",None,None,None,None,None,st.fname)]
        p[0].place=None
    elif p[1] == "return":
        p[0].code=p[2].code
        p[0].code+=[Instruction3AC("ret",None,None,p[2].place,None,None,st.fname)]
        p[0].place=None
        p[0].type = p[2].type
    elif len(p[1:]) == 1:
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

def p_expr2_1(p):
    '''expr2 : arg
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=p[1].place
    p[0].type = p[1].type

def p_expr2_2(p):
    '''expr2 : call
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=p[1].place

def p_call(p):
    '''call : function
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=p[1].place

def p_function(p):
    '''function : IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
                | IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
    '''
    p[0]=SDT()
    if len(p[1:]) == 3:
        p[0].code=[Instruction3AC("call",None,None,p[1],None,None,st.fname)]
        p[0].place=None
    elif len(p[1:]) == 4:
        num_args=0
        for i in range(len(p[3].code)):
            if p[3].code[i].typ == "param":
                p[3].code[i].in2=str(num_args)
                num_args+=1
        p[0].code=p[3].code
        p[0].code+=[Instruction3AC("call",None,None,p[1],None,None,st.fname)]
        p[0].place=None

def p_arg(p):
    '''arg : term0
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=p[1].place
    p[0].type = p[1].type

def p_term0(p):
    '''term0 : mlhs EQUALS IDENTIFIER OPEN_BRACKET CLOSE_BRACKET
           | mlhs EQUALS IDENTIFIER OPEN_BRACKET callargs CLOSE_BRACKET
           | term1
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    elif len(p[1:]) == 5:
        p[0].code=[Instruction3AC("call",None,None,p[3],p[1].place,None,st.fname)]
        st.insert(p[1].place,"int")
        p[0].place=p[1].place
    elif len(p[1:]) == 6:
        num_args=0
        p[0].code=[]
        stack = []
        if st.parent != None:
            func_vars=st.table.keys()
            for i in range(len(func_vars)):
                p[0].code+=[Instruction3AC("push",None,None,func_vars[i],None,None,st.fname)]
                stack.append(func_vars[i])
        for i in range(len(p[5].code)):
            if p[5].code[i].typ == "param":
                p[5].code[i].in2=str(num_args)
                num_args+=1
        p[0].code+=p[5].code
        p[0].code+=[Instruction3AC("call",None,None,p[3],p[1].place,None,st.fname)]
        st.insert(p[1].place,"int")
        while len(stack)>0:
            varname=stack.pop()
            p[0].code+=[Instruction3AC("pop",None,varname,None,None,None,st.fname)]
        p[0].place=p[1].place

def p_term1(p):
    '''term1 : mlhs EQUALS mrhs
              | mlhs opasgn mrhs
              | term2
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type
    else:
        p[0]=SDT()
        if "[" in p[1].place and "]" in p[1].place:
            pass
        else:
            if p[2] == "=":
                # if (p[1].type == "ptr" or p[3].type == "ptr"):
                #     print ("1")
                #     print ("Error: Type mismatch")
                #     quit()

                p[0].type = p[3].type

                if p[0].type == None:
                    st.insert(p[1].place,"int")
                else:
                    st.insert(p[1].place, p[0].type)

            else:
                if (p[1].type == "ptr" or p[3].type == "ptr"):
                    print ("Error: Type mismatch")
                    quit()

                if st.lookup(p[1].place) is None:
                    print("Error: "+p[1].place+" not declared")
                    quit()

        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],p[1].place,p[3].place,None,None,st.fname)]
        p[0].place=p[1].place
        p[0].type = p[1].type

def p_term2(p):
    '''term2 : term3 INCL_RANGE term3
            | term3 EXCL_RANGE term3
            | term3
    '''   
    p[0]=SDT()

    if len(p[1:]) == 1:
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    if len(p[1:]) == 3:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0].code = p[1].code+p[3].code
        temp1 = st.newtemp()
        temp2 = st.newtemp()


        if (p[2:][0] == ".."):
            p[0].code += [Instruction3AC(None, "=", None, temp1, p[1].place, None,st.fname)]
            p[0].code += [Instruction3AC(None, "=", None, temp2, p[3].place, None,st.fname)]
            p[0].place = [temp1, temp2]

        elif (p[2:][0] == "..."):
            #print (p[1].place)
            if st.lookup(p[1].place):
                p[0].code += [Instruction3AC(None, "+", temp1, p[1].place, str(1), None,st.fname)]
                p[0].code += [Instruction3AC(None, "-", temp2, p[3].place, str(1), None,st.fname)]
                p[0].place = [temp1, temp2]

            else: 
                p[0].code += [Instruction3AC(None, "=", None, temp1, str(int(p[1].place)+1), None,st.fname)]
                p[0].code += [Instruction3AC(None, "=", None, temp2, str(int(p[3].place)-1), None,st.fname)]
                p[0].place = [temp1, temp2]

   

def p_term3(p):
    '''term3 : term3 LOGICAL_OR term4
            |  term3 LOGICAL_AND term4
            |  term4
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

def p_term4(p):
    '''term4 : term5 DOUBLE_EQUALS term5
             | term5 NOT_EQUALS term5
             | term5 EQUAL_TILDE term5
             | term5 COMPARISON term5
             | term5
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code
        label1=newlabel()
        label2=newlabel()
        p[0].code+=[Instruction3AC("ifgoto",p[2],None,p[1].place,p[3].place,label1,st.fname)]
        p[0].code+=[Instruction3AC(None,"=",temp,"0",None,None,st.fname)]
        p[0].code+=[Instruction3AC("goto",None,None,None,None,label2,st.fname)]
        p[0].code+=[Instruction3AC("label",None,None,label1,None,None,st.fname)]
        p[0].code+=[Instruction3AC(None,"=",temp,"1",None,None,st.fname)]
        p[0].code+=[Instruction3AC("label",None,None,label2,None,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

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
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code
        label1=newlabel()
        label2=newlabel()
        p[0].code+=[Instruction3AC("ifgoto",p[2],None,p[1].place,p[3].place,label1,st.fname)]
        p[0].code+=[Instruction3AC(None,"=",temp,"0",None,None,st.fname)]
        p[0].code+=[Instruction3AC("goto",None,None,None,None,label2,st.fname)]
        p[0].code+=[Instruction3AC("label",None,None,label1,None,None,st.fname)]
        p[0].code+=[Instruction3AC(None,"=",temp,"1",None,None,st.fname)]
        p[0].code+=[Instruction3AC("label",None,None,label2,None,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

def p_term6(p):
    '''term6 : term6 BIT_XOR term7
            | term6 BIT_OR term7
            | term7
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

def p_term7(p):
    '''term7 : term7 BIT_AND term8
            | term8
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

def p_term8(p):
    '''term8 : term8 LEFT_SHIFT term9
            | term8 RIGHT_SHIFT term9
            | term9
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

def p_term9(p):
    '''term9 : term9 PLUS term10
            | term9 MINUS term10
            | term10
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[3].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        #print (p[1].type)
        #print (p[3].type)
        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

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
        p[0].type = p[1].type

    else:
        if (p[1].type == "ptr" or p[1].type == "ptr"):
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[1].code+p[3].code+[Instruction3AC(None,p[2],temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[1].type

def p_term11(p):
    '''term11 : MINUS term11
            | term12
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    else:
        if p[2].type == "ptr":
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[2].code+[Instruction3AC(None,"*",temp,"-1",p[2].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[2].type

def p_term12(p):
    '''term12 : PLUS term12
            | term13
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type
    else:
        if p[2].type == "ptr":
            print ("Error: Type mismatch")
            quit()

        p[0]=SDT()
        temp=st.newtemp()
        p[0].code=p[2].code+[temp+"="+p[2].place]
        p[0].code=p[2].code+[Instruction3AC(None,"*",temp,"1",p[2].place,None,st.fname)]
        p[0].place=temp
        p[0].type = p[2].type

def p_term13(p):
    '''term13 : primary 
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

def p_primary(p):
    '''primary : OPEN_BRACKET expr2 CLOSE_BRACKET
            | arrayd
            | arraya
            | literal
            | varname
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].code=p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type
    elif p[1]=="(":
        p[0]=SDT()
        p[0].code=p[2].code
        p[0].place=p[2].place

def p_arrayd(p):
    '''arrayd : Array OPEN_BRACKET array_size CLOSE_BRACKET
    '''
    p[0]=SDT()
    temp=st.newtemp()
    p[0].code=p[3].code
    p[0].code+=[Instruction3AC("array",None,None,temp+"["+str(p[3].place)+"]",None,None,st.fname)]
    p[0].place=temp
    p[0].type = "ptr"

def p_array_size(p):
    '''array_size : term2 COMMA array_size
                | term2
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=p[1].code
        p[0].place=p[1].place
    elif len(p[1:]) == 3:
        temp=st.newtemp()
        p[0].code=p[1].code
        p[0].code+=p[3].code
        p[0].code+=[Instruction3AC(None,"*",temp,p[1].place,p[3].place,None,st.fname)]
        p[0].place=temp

def p_arrayal(p):
    '''arrayal : variable OPEN_SQUARE array_args CLOSE_SQUARE
    '''
    p[0]=SDT()
    # temp=st.newtemp()
    p[0].code=p[3].code
    # p[0].code+=[Instruction3AC(None,"=",temp,p[1].place+"["+str(p[3].place)+"]",None,None,st.fname)]
    p[0].place=p[1].place+"["+str(p[3].place)+"]"

def p_arraya(p):
    '''arraya : variable OPEN_SQUARE array_args CLOSE_SQUARE
    '''
    p[0]=SDT()
    p[0].code=p[3].code
    temp=st.newtemp()
    p[0].code+=[Instruction3AC(None,"=",temp,p[1].place+"["+str(p[3].place)+"]",None,None,st.fname)]
    p[0].place=temp

def p_array_args(p):
    '''array_args : primary COMMA array_args
                  | primary
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=[]
        p[0].place=p[1].place
    elif len(p[1:]) == 3:
        pass
        # temp=st.newtemp()
        # p[0].code=p[3].code
        # p[0].code+=[Instruction3AC(None,"*",temp,p[1].place,p[3].place,None,st.fname)]
        # p[0].place=temp
def p_multcase(p):
    '''multcase : when whenargs pthen M_1 multstmt M_1 multcase
                | when whenargs pthen M_1 multstmt M_1
    '''
    p[0] = SDT()
    if len(p[1:]) == 6:
        p[0].code = [Instruction3AC("ifgoto", "==",None,None, p[2].place,p[4].label,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[6].label,st.fname)]
        p[0].code += p[4].code+p[5].code
        p[0].code += p[6].code
        #pass

    elif len(p[1:]) == 7:
        p[0].code = [Instruction3AC("ifgoto", "==",None,None, p[2].place, p[4].label,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[6].label,st.fname)]
        p[0].code += p[4].code+p[5].code
        p[0].code += p[6].code+p[7].code

def p_multelsif(p):
    '''multelsif : elsif expr pthen M_1 multstmt M_1 multelsif M_1
                 | else newline multstmt
                 | empty
    '''
    p[0] = SDT()

    if len(p[1:]) == 1:
        p[0].code = []
        p[0].place = None

    elif len(p[1:]) == 8:
        p[0].code = p[2].code
        p[0].code += [Instruction3AC("ifgoto", ">", None, p[2].place, "0", p[4].label,st.fname)]
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[6].label,st.fname)]
        p[0].code += p[4].code+p[5].code
        p[0].code += [Instruction3AC("goto", None, None, None, None, p[8].label,st.fname)]
        p[0].code += p[6].code+p[7].code+p[8].code

    elif len(p[1:]) == 3:
        p[0].code = p[3].code


    #getRule(p, 'multelsif')


def p_literal(p):
    '''literal : NUMBER
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
        p[0].type = "int"
        # print(p[0].place)

def p_whenargs(p):
    '''whenargs : arg
    '''
    p[0] = SDT()
    if len(p[1:]) == 1:
        # print(p[1].place)
        p[0].code = p[1].code
        p[0].place=p[1].place
        p[0].type = p[1].type

    elif len(p[1:]) == 2:
        pass

    elif len(p[1:]) == 4:
        pass

    #getRule(p,'whenargs')

def p_mlhs(p):
    '''mlhs : mlhsitem
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=p[1].code

def p_mlhsitem_1(p):
    '''mlhsitem : IDENTIFIER
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1]
        #print (p[1])
        p[0].code=[]

def p_mlhsitem_2(p):
    '''mlhsitem : arrayal
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=p[1].code

def p_mrhs(p):
    '''mrhs : term2
    '''
    if len(p[1:]) == 1:
        p[0]=SDT()
        p[0].place=p[1].place
        p[0].code=p[1].code
        p[0].type = p[1].type
        # print(p[0].place)

def p_callargs(p):
    '''callargs : callarglist
    '''
    p[0]=SDT()
    p[0].code=p[1].code
    p[0].place=None

def p_callarglist(p):
    '''callarglist : term2 callmultarglist
               | empty
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=[]
        p[0].place=None
    elif len(p[1:]) == 2:
        p[0].code=p[1].code
        p[0].code+=[Instruction3AC("param",None,None,p[1].place,None,None,st.fname)]
        p[0].code+=p[2].code
        p[0].place=None

def p_callmultarglist(p):
    '''callmultarglist : COMMA term2 callmultarglist
                       | empty
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=[]
        p[0].place=None
    elif len(p[1:]) == 3:
        p[0].code=p[2].code
        p[0].code+=[Instruction3AC("param",None,None,p[2].place,None,None,st.fname)]
        p[0].code+=p[3].code
        p[0].place=None

def p_argdecl(p):
    '''argdecl : OPEN_BRACKET arglist CLOSE_BRACKET
    '''
    p[0]=SDT()
    if len(p[1:]) == 3:
        p[0].code=p[2].code
        p[0].place=None
def p_arglist(p):
    '''arglist : IDENTIFIER multarglist
               | empty
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=[]
        p[0].place=None
    elif len(p[1:]) == 2:
        p[0].code=[Instruction3AC("deparam",None,None,p[1],None,None,st.fname)]
        st.insert(p[1],"int")
        p[0].code+=p[2].code
        p[0].place=None

def p_multarglist(p):
    '''multarglist : COMMA IDENTIFIER multarglist
                 | empty
    '''
    p[0]=SDT()
    if len(p[1:]) == 1:
        p[0].code=[]
        p[0].place=None
    elif len(p[1:]) == 3:
        p[0].code=[Instruction3AC("deparam",None,None,p[2],None,None,st.fname)]
        st.insert(p[2],"int")
        p[0].code+=p[3].code
        p[0].place=None

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
           | do newline
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
    '''
    p[0]=p[1]

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
            p[0].type = st.lookup(p[1])
        else:
            print("Error: "+p[1]+" is not declared")
            quit()

def p_newline(p):
    '''newline : SEMI_COLON
               | NEWLINE
               | empty
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
# output_location=file_location.replace(".rb",".ir")
output_location="ir/test1.ir"
ir_code+=[Instruction3AC("ret_main", None, None,None, None,None,st.fname)]
ir_code=[Instruction3AC("label", None, None,"main", None,None,st.fname)]+ir_code
ir_code+=func_code
Print3AC(ir_code,output_location)