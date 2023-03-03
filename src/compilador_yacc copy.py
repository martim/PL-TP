import ply.yacc as yacc
import sys
from compilador_lex import tokens

# Production errors
def p_S(p):
    "S : BlocoDecl BlocoPrograma"
    p[0] = f'{p[1]}' + f'START\n{p[2]}STOP'

###############
#   Declarações
###############

def p_BlocoDecl_Var(p):
    "BlocoDecl : Decl BlocoDecl"
    p[0] = f'{p[1]}' + f'{p[2]}'

def p_BlocoDecl_Empty(p):
    "BlocoDecl : "
    p[0] = ""
  
def p_Decl_Int(p):
    "Decl : int AtribList"
    p[0] = p[2]


###########################
#   Atribuições Declarações
###########################

def p_AtribList(p):
    "AtribList : AtribDecl ContAtrib"
    p[0] = p[1] + p[2]

def p_ContAtrib_Cont(p):
    "ContAtrib : ',' AtribDecl ContAtrib"
    p[0] = p[2] + p[3]

def p_ContAtrib_Empty(p):
    "ContAtrib : "
    p[0] = ""

def p_AtribDecl(p):
    "AtribDecl : id Atribution"
    p.parser.registers.update({p[1]:{"type":"int","position":p.parser.position,"offset":1}})
    p.parser.position += p.parser.registers[p[1]]["offset"]
    p[0] = p[2] + '\n'

def p_AtribDecl_Arr(p):
    "AtribDecl : id '[' num ']'"
    p.parser.registers.update({p[1]:{"type":"arrayInt","position":p.parser.position,"offset":int(p[3])}})
    p.parser.position += p.parser.registers[p[1]]["offset"]
    p[0] = f'PUSHN {p[3]}\n'

def p_Atribution_Eq(p):
    "Atribution : '=' Exp"
    p[0] = p[2]

def p_Atribution_Empty(p):
    "Atribution : "
    p[0] = "PUSHI 0"

############
#   Programa
############

def p_BlocoPrograma(p):
    "BlocoPrograma : Programa BlocoPrograma"
    p[0] = f'{p[1]}' + f'{p[2]}'

def p_BlocoPrograma_Empty(p):
    "BlocoPrograma :"
    p[0] = ""

def p_Programa_Ler(p):
    "Programa : Ler"
    p[0] = p[1]

def p_Programa_Escrever(p):
    "Programa : Escrever"
    p[0] = p[1]

def p_Programa_Atrib(p):
    "Programa : AtribProg"
    p[0] = p[1]
   
def p_Programa_If(p):
    "Programa : If"
    p[0] = p[1]

def p_Programa_While(p):
    "Programa : While"
    p[0] = p[1]

def p_Programa_Repeat(p):
    "Programa : Repeat"
    p[0] = p[1]

def p_Programa_For(p):
    "Programa : For"
    p[0] = p[1]

########
#   Read
########

def p_Ler(p):
    "Ler : read id"
    p[0] = f'READ\nATOI\nSTOREG {p.parser.registers.get(p[2]).get("position")}\n'

def p_Ler_Arr(p):
    "Ler : read id '[' Exp ']'"
    p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[2]).get("position")}\nPADD\n{p[4]}\nREAD\nATOI\nSTOREN\n'

""" def p_Programa_Ler(p):
    "Programa : read id"
    p[0] = f'READ\nATOI\nSTOREG {p.parser.registers.get(p[2]).get("position")}\n'

def p_Programa_Ler_Arr(p):
    "Programa : read id '[' Exp ']'"
    p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[2]).get("position")}\nPADD\n{p[4]}\nREAD\nATOI\nSTOREN\n'
 """
#########
#   Print
#########

def p_Escrever(p):
    "Escrever : print RelExp"
    p[0] = f'{p[2]}\nWRITEI\nPUSHS " "\nWRITES\n'

""" def p_Programa_Escrever(p):
    "Programa : print RelExp"
    p[0] = f'{p[2]}\nWRITEI\nPUSHS " "\nWRITES\n'
 """
########################
#   Atribuições Programa
########################

""" def p_Programa_Atrib(p):
    "Programa : id '=' Exp"
    p[0] = f'{p[3]}\nSTOREG {p.parser.registers.get(p[1]).get("position")}\n'

def p_Programa_Atrib_Arr(p):
    "Programa : id '[' Exp ']' '=' Exp"
    p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1]).get("position")}\nPADD\n{p[3]}\n{p[6]}\nSTOREN\n'
 """
def p_AtribProg(p):
    "AtribProg : id '=' Exp"
    p[0] = f'{p[3]}\nSTOREG {p.parser.registers.get(p[1]).get("position")}\n'

def p_AtribProg_Arr(p):
    "AtribProg : id '[' Exp ']' '=' Exp"
    p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1]).get("position")}\nPADD\n{p[3]}\n{p[6]}\nSTOREN\n'

###########
#   If Else
###########

def p_If(p):
    "If : if '(' Cond ')' '{' BlocoPrograma '}' Else"
    p[0] = f'{p[3]}\nJZ ELSE{p.parser.ifcounter}\n{p[6]}JUMP FIMIF{p.parser.ifcounter}\nELSE{p.parser.ifcounter}:\n{p[8]}FIMIF{p.parser.ifcounter}:\n'
    p.parser.ifcounter = p.parser.ifcounter + 1

""" def p_Programa_If(p):
    "Programa : if '(' Cond ')' '{' BlocoPrograma '}' Else"
    p[0] = f'{p[3]}\nJZ ELSE{p.parser.ifcounter}\n{p[6]}JUMP FIMIF{p.parser.ifcounter}\nELSE{p.parser.ifcounter}:\n{p[8]}FIMIF{p.parser.ifcounter}:\n'
    p.parser.ifcounter = p.parser.ifcounter + 1
 """
def p_Else(p):
    "Else : else '{' BlocoPrograma '}'"
    p[0] = f'{p[3]}'

def p_Else_Empty(p):
    "Else :"
    p[0] = ""

#########
#   While
#########

def p_While(p):
    "While : while '(' Cond ')' do '{' BlocoPrograma '}'"
    p[0] = f'CICLO{p.parser.whilecounter}:\n{p[3]}\nJZ FIMCICLO{p.parser.whilecounter}\n{p[7]}JUMP CICLO{p.parser.whilecounter}\nFIMCICLO{p.parser.whilecounter}:\n'
    p.parser.whilecounter = p.parser.whilecounter + 1

""" 
def p_Programa_While(p):
    "Programa : while '(' Cond ')' do '{' BlocoPrograma '}'"
    p[0] = f'CICLO{p.parser.whilecounter}:\n{p[3]}\nJZ FIMCICLO{p.parser.whilecounter}\n{p[7]}JUMP CICLO{p.parser.whilecounter}\nFIMCICLO{p.parser.whilecounter}:\n'
    p.parser.whilecounter = p.parser.whilecounter + 1
 """
##########
#   Repeat
##########

def p_Repeat(p):
    "Repeat : repeat '{' BlocoPrograma '}' until Cond"
    p[0] = f'CICLO{p.parser.whilecounter}:\n{p[3]}\n{p[6]}\nJZ CICLO{p.parser.whilecounter}\n'
    p.parser.whilecounter = p.parser.whilecounter + 1

""" def p_Programa_Repeat(p):
    "Programa : repeat '{' BlocoPrograma '}' until Cond"
    p[0] = f'CICLO{p.parser.whilecounter}:\n{p[3]}\n{p[6]}\nJZ CICLO{p.parser.whilecounter}\n'
    p.parser.whilecounter = p.parser.whilecounter + 1 """
    

#######
#   For
#######

def p_For(p):
    "For : for '(' AtribFor ';' Cond ';' AtribProg ')' do '{' BlocoPrograma '}'"
    p[0] = f'{p[3]}\nCICLO{p.parser.whilecounter}:\n{p[5]}\nJZ FIMCICLO{p.parser.whilecounter}\n{p[11]}\n{p[7]}\nJUMP CICLO{p.parser.whilecounter}\nFIMCICLO{p.parser.whilecounter}:\n'
    p.parser.whilecounter = p.parser.whilecounter + 1

""" def p_Programa_For(p):
    "Programa : for '(' AtribFor ';' Cond ';' AtribProg ')' do '{' BlocoPrograma '}'"
    p[0] = f'{p[3]}\nCICLO{p.parser.whilecounter}:\n{p[5]}\nJZ FIMCICLO{p.parser.whilecounter}\n{p[11]}\n{p[7]}\nJUMP CICLO{p.parser.whilecounter}\nFIMCICLO{p.parser.whilecounter}:\n'
    p.parser.whilecounter = p.parser.whilecounter + 1
 """
def p_AtribFor(p):
    "AtribFor : AtribProg"
    p[0] = p[1]

def p_AtribFor_Empty(p):
    "AtribFor :"
    p[0] = ""
    
############
#   Condição
############

def p_Cond_Or(p):
    "Cond : Cond or Cond2"
    p[0] = f'{p[1]}\n{p[3]}\nADD\nPUSHI 0\nSUP'

def p_Cond(p):
    "Cond : Cond2"
    p[0] = f'{p[1]}'

def p_Cond2_And(p):
    "Cond2 : Cond2 and Cond3"
    p[0] = f'{p[1]}\n{p[3]}\nMUL\nPUSHI 1\nEQUAL'

def p_Cond3(p):
    "Cond2  : Cond3"
    p[0] = f'{p[1]}'

def p_Cond3_Not(p):
    "Cond3 : not Cond"
    p[0] = f'{p[2]}\nNOT'

def p_Cond3_RelExp(p):
    "Cond3 : RelExp"
    p[0] = f'{p[1]}'

def p_Cond_Agreg(p):
    "Cond3 : '(' Cond ')'"
    p[0] = f'{p[2]}'

##########################
#   Expressões Relacionais
##########################

def p_RelExp_M(p):
    "RelExp : Exp '>' Exp"
    p[0] = f'{p[1]}\n{p[3]}\nSUP'

def p_RelExp_m(p):
    "RelExp : Exp '<' Exp"
    p[0] = f'{p[1]}\n{p[3]}\nINF'

def p_RelExp_Meq(p):
    "RelExp : Exp Meq Exp"
    p[0] = f'{p[1]}\n{p[3]}\nSUPEQ'

def p_RelExp_meq(p):
    "RelExp : Exp meq Exp"
    p[0] = f'{p[1]}\n{p[3]}\nINFEQ'

def p_RelExp_dif(p):
    "RelExp : Exp dif Exp"
    p[0] = f'{p[1]}\n{p[3]}\nEQUAL\nNOT'

def p_RelExp_eq(p):
    "RelExp : Exp eq Exp"
    p[0] = f'{p[1]}\n{p[3]}\nEQUAL'
    pass

def p_RelExp_Exp(p):
    "RelExp : Exp"
    p[0] = f'{p[1]}'

##############
#   Expressões
##############

def p_Exp_add(p):
    "Exp : Exp '+' Termo"
    p[0] = f'{p[1]}\n{p[3]}\nADD'

def p_Exp_sub(p):
    "Exp : Exp '-' Termo"
    p[0] = f'{p[1]}\n{p[3]}\nSUB'

def p_Exp_Termo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_Termo_mul(p):
    "Termo : Termo '*' Factor"
    p[0] = f'{p[1]}\n{p[3]}\nMUL'

def p_Termo_div(p):
    "Termo : Termo '/' Factor"
    p[0] = f'{p[1]}\n{p[3]}\nDIV'

def p_Termo_mod(p):
    "Termo : Termo '%' Factor"
    p[0] = f'{p[1]}\n{p[3]}\nMOD'

def p_Termo_Factor(p):
    "Termo : Factor"
    p[0] = p[1]

def p_Factor_Exp(p):
    "Factor : '(' Exp ')'"
    p[0] = p[2]

def p_Factor_num(p):
    "Factor : num"
    p[0] = f'PUSHI {p[1]}'

def p_Factor_id(p):
    "Factor : id"
    p[0] = f'PUSHG {p.parser.registers.get(p[1]).get("position")}'

def p_Factor_id_Arr(p):
    "Factor : id '[' Exp ']'"
    p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1]).get("position")}\nPADD\n{p[3]}\nLOADN'

########
#   Erro
########

def p_error(p):
    print("Erro Sintático: ", p)
    parser.success = False

##########
#   "Main"
##########

argc = len(sys.argv)

if argc < 2:
    print("Not enough arguments!")
elif argc > 3:
    print("too many arguments!")
else:
    fileName = ""
    if argc == 2:
        splitName = sys.argv[1].split('.')
        for i in range (0,len(splitName)-1):
            fileName += splitName[i] + '.'
        fileName += 'vm'
    else:
        fileName = sys.argv[2]

    #   Build the Parser
    parser = yacc.yacc()

    # Creating the model
    parser.registers = {}
    parser.position = 0
    parser.ifcounter = 0
    parser.whilecounter = 0

    f_wr = open(fileName, "w")
    f_rd = open(sys.argv[1], "r")

    readFile = f_rd.read()
    result = parser.parse(readFile)
    f_wr.write(result)