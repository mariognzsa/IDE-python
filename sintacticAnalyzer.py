tokens = []
errors = []
tree = []
EOF = False
class Token(object):
    def __init__(self):
        self.token = None
        self.tokenType = None

ig = 0

class Nodo(object):
    def __init__(self):
        self.nombre  = None
        self.dato  = None
        self.hijo = [None,None,None]
        self.sibling = []
    
def match(tokensActual):
    global ig
    global tokens
    global EOF
    if tokens[ig].token == tokensActual:
        if ig < len(tokens)-1:
            ig += 1
        else:
            EOF = True
    else:
        #print(tokens[ig].token)
        error(0, tokensActual, tokens[ig].line)

def programa():
    global ig
    global tokens
    global EOF
    temp = Nodo()
    temp.nombre = "Main"
    match('main')
    match('{')
    temp.hijo[0] = lista_declaracion()
    temp.hijo[1] = lista_sentencias()
    if not EOF:
        match('}')
    else:
        error(1,"Error. Main inconcluso, falta cerrar llave.", tokens[ig].line)
    return temp

def lista_declaracion():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Lista Declaracion"
    temp.hijo[0] = declaracion()
    if temp.hijo[0] != None:
        match(';')
    while (temp.hijo[0] != None):
        temp.hijo[0].sibling.append(declaracion())
        if temp.hijo[0].sibling[len(temp.hijo[0].sibling)-1] != None:
            match(';')
        else:
            break
    return temp

def declaracion():
    global ig
    global tokens
    if (tokens[ig].token == 'int' or tokens[ig].token == 'float' or tokens[ig].token == 'bool'):
        temp = Nodo()
        temp.nombre = "Declaracion"
        temp.hijo[0] = tipo()
        temp.hijo[1] = lista_variables()
        return temp

def tipo():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Tipo"
    if tokens[ig].token == "int":
        temp.dato = tokens[ig].token
        match('int')
    elif tokens[ig].token == "float":
        temp.dato = tokens[ig].token
        match('float')
    elif tokens[ig].token == "bool":
        temp.dato = tokens[ig].token
        match('bool')
    return temp

def lista_variables():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Lista variables"
    temp.sibling.append(fin())
    while(tokens[ig].token == ","):
        match(',')
        temp.sibling.append(fin())
    return temp

def lista_sentencias():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Lista Sentencias"
    temp.hijo[0] = sentencia()
    while temp.hijo[0] != None:
        temp.hijo[0].sibling.append(sentencia())
        if temp.hijo[0].sibling[len(temp.hijo[0].sibling)-1] == None:
            if (tokens[ig].token == "}" and ig < len(tokens)-1) or tokens[ig].token == "else" or tokens[ig].token == "end" or tokens[ig].token == "until" or ig == len(tokens)-1:
                break
            else:
                ig += 1
    return temp

def sentencia():
    global ig
    global tokens
    if  ig < len(tokens)-1 and (tokens[ig].token == 'if' or tokens[ig].token == 'while' or tokens[ig].token == 'do' or tokens[ig].token == 'cin' or tokens[ig].token == 'cout' or tokens[ig].token == '{' or tokens[ig].tokenType == 'identifier'):
        temp = Nodo()
        temp.nombre = "Sentencia"
        if tokens[ig].token == 'if':
            temp.hijo[0] = seleccion()
        elif tokens[ig].token == 'while':
            temp.hijo[0] = iteracion()
        elif tokens[ig].token == 'do':
            temp.hijo[0] = repeticion()
        elif tokens[ig].token == 'cin':
            temp.hijo[0] = sent_cin()
        elif tokens[ig].token == 'cout':
            temp.hijo[0] = sent_cout()
        elif tokens[ig].token == '{':
            temp.hijo[0] = bloque()
        elif tokens[ig].tokenType == 'identifier':
            temp.hijo[0] = asignacion()
        return temp

def seleccion():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Seleccion"
    match('if')
    match('(')
    temp.hijo[0] = expresion()
    match(')')
    match('then')
    temp.hijo[1] = bloque()
    if tokens[ig].token == "else":
        match('else')
        temp.hijo[2] = bloque()
    match('end')
    return temp
    
def iteracion():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Iteracion"
    match('while')
    match('(')
    temp.hijo[0] = expresion()
    match(')')
    temp.hijo[1] = bloque()
    return temp

def repeticion():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Do"
    match('do')
    temp.hijo[0] = bloque()
    match('until')
    match('(')
    temp.hijo[1] = expresion()
    match(')')
    match(';')
    return temp

def sent_cin():
    global ig
    global tokens
    temp = Nodo()
    nuevo = Nodo()
    temp.nombre = "Cin"
    match('cin')
    nuevo.nombre = "identifier"
    nuevo.dato = tokens[ig].token
    temp.hijo[0] = nuevo
    if ig < len(tokens)-1:
        ig += 1
    else:
        error(1,"Error. Main inconcluso, falta cerrar llave.", tokens[ig-1].line)
    match(';')
    return temp

def sent_cout():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Cout"
    match('cout')
    temp.hijo[0] = expresion()
    match(';')
    return temp

def bloque():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Bloque"
    match('{')
    temp.hijo[0] = lista_sentencias()
    match('}')
    return temp

def asignacion():
    global ig
    global tokens
    nuevo = Nodo()
    temp = Nodo()
    temp.nombre = "Variable"
    temp.dato = tokens[ig].token
    if ig < len(tokens)-1:
        ig += 1
    else:
        error(1,"Error. Main inconcluso, falta cerrar llave.", tokens[ig-1].line)
    if tokens[ig].token == ":=" or (tokens[ig].token != "++" and tokens[ig].token != "--"):
        match(':=')
        nuevo.nombre = "Asignacion"
        nuevo.hijo[0] = temp
        nuevo.hijo[1] = expresion()
        temp = nuevo
        match(';')
    elif tokens[ig].token == "++" or tokens[ig].token == "--":
        if tokens[ig].token == "++":
            match('++')
            nuevo.nombre = "++"
            nuevo.hijo[0] = temp
            #nuevo.dato = str(temp.dato) + "+1"
            temp = nuevo
        else:
            match('--')
            nuevo.nombre = "--"
            nuevo.hijo[0] = temp
            #nuevo.dato = str(temp.dato) + "-1"
            temp = nuevo
        match(';')
    else:
        error(1,"Error sintactico.",tokens[ig-1].line)
    return temp

def expresion():
    global ig
    global tokens
    nuevo = Nodo()
    temp = expresion_simple()
    if(tokens[ig].token == '<=' or tokens[ig].token == '<' or tokens[ig].token == '>=' or tokens[ig].token == '>' or tokens[ig].token == '==' or tokens[ig].token == '!='):
        if tokens[ig].token == '<=':
            match('<=')  
            nuevo.nombre = "<="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple()
            '''
            if (temp.dato <= nuevo.hijo[1].dato): 
                nuevo.dato = True
            else: 
                nuevo.dato = False
            '''
            temp = nuevo
        elif tokens[ig].token == '<':
            match('<')  
            nuevo.nombre = "<"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple()
            '''
            if (temp.dato < nuevo.hijo[1].dato): 
                nuevo.dato = True
            else: 
                nuevo.dato = False
            '''
            temp = nuevo
        elif tokens[ig].token == '>':
            match('>')  
            nuevo.nombre = ">"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple()
            '''
            if (temp.dato > nuevo.hijo[1].dato): 
                nuevo.dato = True
            else: 
                nuevo.dato = False
            '''
            temp = nuevo
        elif tokens[ig].token == '>=':
            match('>=')  
            nuevo.nombre = ">="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple()
            '''
            if (temp.dato >= nuevo.hijo[1].dato): 
                nuevo.dato = True
            else: 
                nuevo.dato = False
            '''
            temp = nuevo
        elif tokens[ig].token == '==':
            match('==')  
            nuevo.nombre = "=="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple()
            '''
            if (temp.dato == nuevo.hijo[1].dato): 
                nuevo.dato = True
            else: 
                nuevo.dato = False
            '''
            temp = nuevo
        elif tokens[ig].token == '!=':
            match('!=')  
            nuevo.nombre = "!="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple()
            '''
            if (temp.dato != nuevo.hijo[1].dato): 
                nuevo.dato = True
            else: 
                nuevo.dato = False
            '''
            temp = nuevo
    return temp

def expresion_simple():
    global ig
    global tokens
    temp = termino()
    while(tokens[ig].token == '+' or tokens[ig].token == '-'):
        nuevo = Nodo()
        if tokens[ig].token == '+':
            match('+')  
            nuevo.nombre = "+"
            nuevo.hijo[0] = temp
            #nuevo.dato = temp.dato
            nuevo.hijo[1] = termino()
            '''
            if (type(nuevo.dato) == int or type(nuevo.dato) == float) and (type(nuevo.hijo[1].dato) == int or type(nuevo.hijo[1].dato) == float):
                nuevo.dato = float(nuevo.dato)
                nuevo.dato += float(nuevo.hijo[1].dato)
            else:
                nuevo.dato = str(nuevo.dato)
                nuevo.dato += "+" + str(nuevo.hijo[1].dato)
            '''
            temp = nuevo
        elif tokens[ig].token == '-':
            match('-')  
            nuevo.nombre = "-"
            nuevo.hijo[0] = temp
            #nuevo.dato = temp.dato
            nuevo.hijo[1] = termino()
            '''
            if (type(nuevo.dato) == int or type(nuevo.dato) == float) and (type(nuevo.hijo[1].dato) == int or type(nuevo.hijo[1].dato) == float):
                nuevo.dato = float(nuevo.dato)
                nuevo.dato -= float(nuevo.hijo[1].dato)
            else:
                nuevo.dato = str(nuevo.dato)
                nuevo.dato += "-" + str(nuevo.hijo[1].dato)
            '''
            temp = nuevo
    return temp

def termino():
    global ig
    global tokens
    temp = factor()
    while(tokens[ig].token == '*' or tokens[ig].token =='/' or tokens[ig].token == '%'):
        nuevo = Nodo()
        if tokens[ig].token == '*':
            match('*')  
            nuevo.nombre = "*"
            nuevo.hijo[0] = temp
            #nuevo.dato = temp.dato
            nuevo.hijo[1] = termino()
            '''
            if (type(nuevo.dato) == int or type(nuevo.dato) == float) and (type(nuevo.hijo[1].dato) == int or type(nuevo.hijo[1].dato) == float):
                nuevo.dato = float(nuevo.dato)
                nuevo.dato *= float(nuevo.hijo[1].dato)
            else:
                nuevo.dato = str(nuevo.dato)
                nuevo.dato += "*" + str(nuevo.hijo[1].dato)
            '''
            temp = nuevo
        elif tokens[ig].token == '/':
            match('/')  
            nuevo.nombre = "/"
            nuevo.hijo[0] = temp
            #nuevo.dato = temp.dato
            nuevo.hijo[1] = termino()
            '''
            if (type(nuevo.dato) == int or type(nuevo.dato) == float) and (type(nuevo.hijo[1].dato) == int or type(nuevo.hijo[1].dato) == float):
                nuevo.dato = float(nuevo.dato)
                nuevo.dato /= float(nuevo.hijo[1].dato)
            else:
                nuevo.dato = str(nuevo.dato)
                nuevo.dato += "/" + str(nuevo.hijo[1].dato)
            '''
            temp = nuevo
        elif tokens[ig].token == '%':
            match('%')  
            nuevo.nombre = "%"
            nuevo.hijo[0] = temp
            #nuevo.dato = temp.dato
            nuevo.hijo[1] = termino()
            '''
            if (type(nuevo.dato) == int or type(nuevo.dato) == float) and (type(nuevo.hijo[1].dato) == int or type(nuevo.hijo[1].dato) == float):
                nuevo.dato = float(nuevo.dato)
                nuevo.dato %= float(nuevo.hijo[1].dato)
            else:
                nuevo.dato = str(nuevo.dato)
                nuevo.dato += "%" + str(nuevo.hijo[1].dato)
            '''
            temp = nuevo
    return temp

def factor():
    global ig
    global tokens
    temp = fin()
    while(tokens[ig].token == '^'):
        nuevo = Nodo()
        match('^')  
        nuevo.nombre = "^"
        nuevo.hijo[0] = temp
        #nuevo.dato = temp.dato
        nuevo.hijo[1] = termino()
        '''
        if (type(nuevo.dato) == int or type(nuevo.dato) == float) and (type(nuevo.hijo[1].dato) == int or type(nuevo.hijo[1].dato) == float):
            nuevo.dato = float(nuevo.dato)
            nuevo.dato **= float(nuevo.hijo[1].dato)
        else:
            nuevo.dato = str(nuevo.dato)
            nuevo.dato += "^" + str(nuevo.hijo[1].dato)
        '''
        temp = nuevo
    return temp

def fin():
    global ig
    global tokens
    temp = Nodo()
    if tokens[ig].token == '(':
        match('(')
        temp = expresion()
        match(')')
    elif tokens[ig].tokenType == "integer" or tokens[ig].tokenType == "float":
        temp.nombre = tokens[ig].tokenType
        if tokens[ig].tokenType == "integer":
            temp.dato = int (tokens[ig].token)
        elif tokens[ig].tokenType == "float":
            temp.dato = float (tokens[ig].token)
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error. Main inconcluso, falta cerrar llave.", tokens[ig-1].line)
    elif tokens[ig].tokenType == "identifier":
        temp.nombre = tokens[ig].tokenType
        temp.dato = tokens[ig].token
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error. Main inconcluso, falta cerrar llave.", tokens[ig-1].line)
    else:
        error(1,"Error sintactico", tokens[ig-1].line)
    return temp

def error(op, token, line):
    global errors, ig
    if op == 0:
        errors.append("Error. Se esperaba '" + token + "'. En la linea " + line)
        #print("Error. Se esperaba '" + token + "'. En la linea " + line)
    else:
        errors.append(token + " En la linea " + line)
        #print(token + " En la linea " + line)

def verNodo(nodo):
    if(nodo != None):
        print("Nodo-> " + str(nodo.nombre))
        print("Valor-> " + str(nodo.dato))
        for s in nodo.sibling:
            verNodo(s)
        verNodo(nodo.hijo[0])
        verNodo(nodo.hijo[1])
        verNodo(nodo.hijo[2])
    return

if __name__== "__main__":
    raiz = programa()
    verNodo(raiz)
    