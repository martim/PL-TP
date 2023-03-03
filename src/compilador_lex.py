import ply.lex as lex

tokens = ['num', 'id', 'print', 'read', 'int', 'or', 'and', 'not', 'if', 'else', 'Meq', 'meq', 'dif', 'eq', 'while', 'do', 'repeat', 'until', 'for']
literals = ['+', '-', '*', '/', '=', ',', '(', ')', '{', '}', '>', '<', '!', '%', '[', ']', ';']

def t_int(t):
    r'int'
    return t

def t_repeat(t):
    r'repeat'
    return t

def t_until(t):
    r'until'
    return t

def t_for(t):
    r'for'
    return t

def t_while(t):
    r'while'
    return t

def t_do(t):
    r'do'
    return t

def t_if(t):
    r'if'
    return t

def t_else(t):
    r'else'
    return t

def t_or(t):
    r'or'
    return t

def t_and(t):
    r'and'
    return t    

def t_not(t):
    r'not'
    return t

def t_print(t):
    r'print'
    return t

def t_read(t):
    r'read'
    return t

def t_num(t):
    r'-?\d+'
    return t

def t_id(t):
    r'[a-zA-Z]\w*'
    return t

def t_Meq(t):
    r'>='
    return t

def t_meq(t):
    r'<='
    return t

def t_eq(t):
    r'=='
    return t

def t_dif(t):
    r'!='
    return t

t_ignore = " \t\n"

def t_error(t):
    print(f"Illegal Character {t.value[0]}")
    t.lexer.skip(1)

#   Build the lexer
lexer = lex.lex()
