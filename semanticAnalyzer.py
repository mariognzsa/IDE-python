tokens = []
errors = []
tree = []
EOF = False
hash = [None] * 211

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
        self.tipo = None
        self.valor = None

def getPosition(name):
    temp = 0
    i = 0
    if(name == None):
        return temp
    for caracter in name:
        temp = ((temp << 32) + ord(caracter[i])) % 211
    return temp

def setHash(variable, tipo, valor, linea,proviene):
    global hash
    position = getPosition(variable)
    l =  hash[position]
    if l == None and proviene != 0:
        hash[position] = [variable,tipo,valor,[linea]]
        return 1
    elif l == None and proviene == 0:
        error(1,"[Error] - La variable \"" + variable + "\" no ha sido declarada",str(linea))
        return -2#hubo un error y ya fue declarada
    elif (l[1] != tipo and proviene != 0) or (linea in l[3] != tipo and proviene != 0):
        error(1,"[Error] - La variable \"" + variable + "\" ya ha sido declarada",str(l[3][0]))
        return -1#hubo un error y ya fue declarada
    else:
        return 2#ya existe en la tabla y podríamos añadir una linea

def getHash(variable,linea):
    global hash
    position = getPosition(variable)
    l =  hash[position]
    if l == None:
        if variable != None:
            error(1,"[Error] - La variable \"" + variable + "\" no ha sido declarada",linea)
        return []
    else:
        return l

def setHashValue(variable,valor,linea):
    global hash
    position = getPosition(variable)
    l =  hash[position]
    if l == None:
        error(1,"[Error] - La variable \"" + variable + "\" no ha sido declarada", str(linea))
    else:
        hash[position] = [l[0],l[1],valor,l[3]]
       
def setHashLine(variable, linea):
    position = getPosition(variable)
    l = hash[position]
    if l == None:
        error(1,"[Error] - La variable \"" + variable + "\" no ha sido declarada", str(linea))
    else:
        l[3].append(linea)
        hash[position] = [l[0], l[1], l[2], l[3]]

def match(tokensActual):
    global ig
    global tokens
    global EOF
    if tokens[ig].token == tokensActual:
        if ig < len(tokens)-1:
            ig += 1
        else:
            EOF = True
    # else:
        #print(tokens[ig].token)
        # error(0, tokensActual, tokens[ig].line)    

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
        error(1,"[Error] - Main inconcluso, falta cerrar llave.", tokens[ig].line)
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
        temp.hijo[1] = lista_variables(temp.hijo[0].dato)
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

def lista_variables(tipo):
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Lista variables"
    temp.hijo[0]=fin(tipo,1)
    while(tokens[ig].token == ","):
        match(',')
        temp.hijo[0].sibling.append(fin(tipo,1))
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
    tipoHash = getHash(tokens[ig].token, tokens[ig].line)
    if len(tipoHash) > 0:
        # nuevo.nombre = "identifier"
        # nuevo.dato = tokens[ig].token
        nuevo = fin(tipoHash[1])
        temp.hijo[0] = nuevo
        match(';')
        return temp
    else:
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error en el fin del programa.",tokens[ig].line)
        return None

def sent_cout():
    global ig
    global tokens
    temp = Nodo()
    temp.nombre = "Cout"
    match('cout')
    tipoHash = getHash(tokens[ig].token, tokens[ig].line)
    if len(tipoHash) > 0:
        temp.hijo[0] = expresion(tipoHash[1])
        match(';')
        return temp
    else:
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error en el fin del programa.",tokens[ig].line)
        return None

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
    global hash
    nuevo = Nodo()
    temp = Nodo()
    tipoHash = getHash(tokens[ig].token, tokens[ig].line)
    
    if len(tipoHash) > 0:
        # temp.nombre = "Variable"
        # temp.dato = tokens[ig].token
        # temp.valor = tipoHash[2]
        # if ig < len(tokens)-1:
        #     ig += 1
        # else:
        #     error(1,"Error en el fin del programa.",tokens[ig].line)
        temp = fin(tipoHash[1])
        
        if tokens[ig].token == ":=" or (tokens[ig].token != "++" and tokens[ig].token != "--"):
            match(':=')
            nuevo.nombre = "Asignacion"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion(temp.tipo)

            if tipoHash[1] == nuevo.hijo[1].tipo:
                nuevo.valor = nuevo.hijo[1].valor
                nuevo.tipo = nuevo.hijo[0].tipo
                setHashValue(temp.dato, nuevo.hijo[1].valor, tokens[ig].line)
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
            match(';')

            #nuevo.valor = nuevo.hijo[1].valor
            #setHashValue(temp.dato, nuevo.hijo[1].valor, tokens[ig].line)
            #temp = nuevo
            #match(';')

        elif tokens[ig].token == "++" or tokens[ig].token == "--":
            if tokens[ig].token == "++":
                match(':=')
                nuevo.nombre = "++"
                nuevo.hijo[0] = temp
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.dato = str(temp.dato) + str("+1")
                if temp.valor != '' and temp.valor != None:
                    nuevo.valor = str(float(temp.valor) + 1)
                    if tipoHash[1] == 'int':
                        nuevo.valor = str(int(temp.valor) + 1)
                    setHashValue(temp.dato, nuevo.valor, tokens[ig].line)
                else:
                    error(1,"[Error] - Sin valor la variable: \""+ temp.dato +'"',tokens[ig].line)
                    while (tokens[ig].token != ';'):
                        if ig < len(tokens)-1:
                            ig += 1
                        else:
                            error(1,"Error en el fin del programa.",tokens[ig].line)
                    if ig < len(tokens)-1:
                        ig += 1
                    else:
                        error(1,"Error en el fin del programa.",tokens[ig].line)
                temp = nuevo
            else:
                match('--')
                nuevo.nombre = ":="
                nuevo.hijo[0] = temp
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.dato = str(temp.dato) + str("-1")
                if temp.valor != ''and temp.valor != None:
                    nuevo.valor = str(float(temp.valor) - 1)
                    if tipoHash[1] == 'int':
                        nuevo.valor = str(int(temp.valor) - 1)
                    setHashValue(temp.dato, nuevo.valor, tokens[ig].line)
                else:
                    error(1,"[Error] - Sin valor la variable: \""+ temp.dato +'"',tokens[ig].line)
                    while (tokens[ig].token != ';'):
                        if ig < len(tokens)-1:
                            ig += 1
                        else:
                            # print(tokens[ig].line)
                            error(1,"Error en el fin del programa.",tokens[ig].line)
                    if ig < len(tokens)-1:
                        ig += 1
                    else:
                        error(1,"Error en el fin del programa.",tokens[ig].line)
                temp = nuevo
            match(';')
        return temp
    else:
        while (tokens[ig].token != ';'):
            if ig < len(tokens)-1:
                ig += 1
            else:
                error(1,"Error en el fin del programa.",tokens[ig].line)
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error en el fin del programa.",tokens[ig].line)
        return None

def expresion(tipo = 'bool'):
    global ig
    global tokens
    nuevo = Nodo()
    temp = expresion_simple(tipo)
    #temp.tipo = "bool"
    nuevo.valor = temp.valor
    nuevo.tipo = temp.tipo
    if(tokens[ig].token == '<=' or tokens[ig].token == '<' or tokens[ig].token == '>=' or tokens[ig].token == '>' or tokens[ig].token == '==' or tokens[ig].token == '!='):
        if tokens[ig].token == '<=':
            match('<=')  
            nuevo.nombre = "<="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple(tipo)
            nuevo.tipo = 'bool'
            # REGLA 1:int <= int = int
            # REGLA 3:float <= float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo:
                if nuevo.hijo[0].tipo == 'int':
                    if int(nuevo.hijo[0].valor) <= int(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
                else:
                    if float(nuevo.hijo[0].valor) <= float(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
            # REGLA 5:float <= int//Error
            # REGLA 7:int <= float//Error
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
        elif tokens[ig].token == '<':
            match('<')  
            nuevo.nombre = "<"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple(tipo)
            nuevo.tipo = 'bool'
            # REGLA 1:int < int = int
            # REGLA 3:float < float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo:
                if nuevo.hijo[0].tipo == 'int':
                    if int(nuevo.hijo[0].valor) < int(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
                else:
                    if float(nuevo.hijo[0].valor) < float(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
            # REGLA 5:float < int//Error
            # REGLA 7:int < float//Error
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
        elif tokens[ig].token == '>':
            match('>')  
            nuevo.nombre = ">"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple(tipo)
            nuevo.tipo = 'bool'
            # REGLA 1:int > int = int
            # REGLA 3:float > float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo:
                if nuevo.hijo[0].tipo == 'int':
                    if int(nuevo.hijo[0].valor) > int(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
                else:
                    if float(nuevo.hijo[0].valor) > float(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
            # REGLA 5:float > int//Error
            # REGLA 7:int > float//Error
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
        elif tokens[ig].token == '>=':
            match('>=')  
            nuevo.nombre = ">="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple(tipo)
            nuevo.tipo = 'bool'
            # REGLA 1:int >= int = int
            # REGLA 3:float >= float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo:
                if nuevo.hijo[0].tipo == 'int':
                    if int(nuevo.hijo[0].valor) >= int(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
                else:
                    if float(nuevo.hijo[0].valor) >= float(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
            # REGLA 5:float >= int//Error
            # REGLA 7:int >= float//Error
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
        elif tokens[ig].token == '==':
            match('==')  
            nuevo.nombre = "=="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple(tipo)
            nuevo.tipo = 'bool'
            # REGLA 1:int == int = int
            # REGLA 3:float == float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo:
                if nuevo.hijo[0].tipo == 'int':
                    if int(nuevo.hijo[0].valor) == int(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
                else:
                    if float(nuevo.hijo[0].valor) == float(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
            # REGLA 5:float == int//Error
            # REGLA 7:int == float//Error
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
        elif tokens[ig].token == '!=':
            match('!=')  
            nuevo.nombre = "!="
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = expresion_simple(tipo)
            nuevo.tipo = 'bool'
            # REGLA 1:int != int = int
            # REGLA 3:float != float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo:
                if nuevo.hijo[0].tipo == 'int':
                    if int(nuevo.hijo[0].valor) != int(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
                else:
                    if float(nuevo.hijo[0].valor) != float(nuevo.hijo[1].valor):
                        nuevo.valor = 'True'
                    else:
                        nuevo.valor = 'False'
            # REGLA 5:float != int//Error
            # REGLA 7:int != float//Error
            else:
                error(1,"[Error] - Datos incompatibles",tokens[ig].line)
            temp = nuevo
    return temp

def expresion_simple(tipo):
    global ig
    global tokens
    global hash
    temp = termino(tipo)
    while(tokens[ig].token == '+' or tokens[ig].token == '-'):
        nuevo = Nodo()
        if tokens[ig].token == '+':
            match('+')  
            nuevo.nombre = "+"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = termino(tipo)
            nuevo.tipo = tipo

            # REGLA 1:int + int = int
            # REGLA 2:float + float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo and nuevo.hijo[0].tipo == 'int':
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.valor = int(nuevo.hijo[0].valor) + int(nuevo.hijo[1].valor)                
            # REGLA 3:float + int = float
            # REGLA 4:int + float = float
            else:
                nuevo.tipo = 'float'
                nuevo.valor = float(nuevo.hijo[0].valor) + float(nuevo.hijo[1].valor)
            temp = nuevo

        elif tokens[ig].token == '-':
            match('-')  
            nuevo.nombre = "-"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = termino(tipo)
            nuevo.tipo = tipo

            # REGLA 1:int - int = int
            # REGLA 2:float - float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo and nuevo.hijo[0].tipo == 'int':
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.valor = int(nuevo.hijo[0].valor) - int(nuevo.hijo[1].valor)
            # REGLA 3:float - int = float
            # REGLA 4:int - float = float
            else:
                nuevo.tipo = 'float'
                nuevo.valor = float(nuevo.hijo[0].valor) - float(nuevo.hijo[1].valor)
            temp = nuevo
    return temp

def termino(tipo):
    global ig
    global tokens
    temp = factor(tipo)
    while(tokens[ig].token == '*' or tokens[ig].token =='/' or tokens[ig].token == '%'):
        nuevo = Nodo()
        if tokens[ig].token == '*':
            match('*')  
            nuevo.nombre = "*"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = factor(tipo)
            nuevo.tipo = tipo
            
            # REGLA 1:int * int = int
            # REGLA 2:float * float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo and nuevo.hijo[0].tipo == 'int':
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.valor = int(nuevo.hijo[0].valor) * int(nuevo.hijo[1].valor)
            # REGLA 3:float * int = float
            # REGLA 4:int * float = float
            else:
                nuevo.tipo = 'float'
                nuevo.valor = float(nuevo.hijo[0].valor) * float(nuevo.hijo[1].valor)
            temp = nuevo

        elif tokens[ig].token == '/':
            match('/')  
            nuevo.nombre = "/"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = factor(tipo)
            nuevo.tipo = tipo

            # REGLA 1:int / int = int
            # REGLA 2:float / float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo and nuevo.hijo[0].tipo == 'int':
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.valor = int(int(nuevo.hijo[0].valor) / int(nuevo.hijo[1].valor))
            # REGLA 3:float / int = float
            # REGLA 4:int / float = float
            else:
                nuevo.tipo = 'float'
                nuevo.valor = float(nuevo.hijo[0].valor) / float(nuevo.hijo[1].valor)
            temp = nuevo

        elif tokens[ig].token == '%':
            match('%')  
            nuevo.nombre = "%"
            nuevo.hijo[0] = temp
            nuevo.hijo[1] = factor(tipo)
            nuevo.tipo = tipo

            # REGLA 1:int % int = int
            # REGLA 2:float % float = float
            if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo and nuevo.hijo[0].tipo == 'int':
                nuevo.tipo = nuevo.hijo[0].tipo
                nuevo.valor = int(nuevo.hijo[0].valor) % int(nuevo.hijo[1].valor)
            # REGLA 3:float % int = float
            # REGLA 4:int % float = float
            else:
                nuevo.tipo = 'float'
                nuevo.valor = float(nuevo.hijo[0].valor) % float(nuevo.hijo[1].valor)
            temp = nuevo

    return temp

def factor(tipo):
    global ig
    global tokens
    temp = fin(tipo)
    while(tokens[ig].token == '^'):
        nuevo = Nodo()
        match('^')  
        nuevo.nombre = "^"
        nuevo.hijo[0] = temp
        nuevo.hijo[1] = fin(tipo)
        nuevo.tipo = tipo

        # REGLA 1:int ** int = int
        # REGLA 2:float ** float = float
        if nuevo.hijo[0].tipo == nuevo.hijo[1].tipo and nuevo.hijo[0].tipo == 'int':
            nuevo.tipo = nuevo.hijo[0].tipo
            nuevo.valor = int(nuevo.hijo[0].valor) ** int(nuevo.hijo[1].valor)
        # REGLA 3:float ** int = float
        # REGLA 4:int ** float = float
        else:
            nuevo.tipo = 'float'
            nuevo.valor = float(nuevo.hijo[0].valor) ** float(nuevo.hijo[1].valor)
        temp = nuevo

    return temp

def fin(tipo,proviene = 0):
    global ig
    global tokens
    global hash
    temp = Nodo()
    if tokens[ig].token == '(':
        match('(')
        temp = expresion(tipo)
        match(')')
    elif tokens[ig].tokenType == "integer":
        temp.nombre = tokens[ig].tokenType
        temp.dato = tokens[ig].token
        temp.tipo = "int"
        # temp.valor = temp.dato
        '''if tipo == 'int':
            if temp.tipo == 'float':
                temp.valor = str(int(float(tokens[ig].token)))
            else:
                temp.valor = str(int(tokens[ig].token))
        else:
            if temp.tipo == 'int':
                temp.valor = str(float(int(tokens[ig].token)))
            else:
                temp.valor = str(float(tokens[ig].token))'''
        temp.valor = str(int(tokens[ig].token))
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error en el fin del programa.",tokens[ig].line)

    elif tokens[ig].tokenType == "float":
        temp.nombre = tokens[ig].tokenType
        temp.dato = tokens[ig].token
        temp.tipo = "float"
        # temp.valor = temp.dato
        '''if tipo == 'int':
            if temp.tipo == 'float':
                temp.valor = str(int(float(tokens[ig].token)))
            else:
                temp.valor = str(int(tokens[ig].token))
        else:
            if temp.tipo == 'int':
                temp.valor = str(float(int(tokens[ig].token)))
            else:
                temp.valor = str(float(tokens[ig].token))'''
        temp.valor = str(float(tokens[ig].token))
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error en el fin del programa.",tokens[ig].line)
    elif tokens[ig].tokenType == "identifier":
        temp.nombre = tokens[ig].tokenType
        temp.dato = tokens[ig].token
        bandera =setHash(temp.dato, tipo, "", tokens[ig].line, proviene)
        if bandera == 1:#apenas se creo
            temp.tipo = tipo
        elif bandera == 2:#podemos llenar otra linea
            setHashLine(temp.dato,tokens[ig].line)
            tipohash = getHash(temp.dato, tokens[ig].line)
            temp.tipo = tipohash[1]
            temp.valor = tipohash[2]
        elif bandera == -1:
            temp = None
        if ig < len(tokens)-1:
            ig += 1
        else:
            error(1,"Error en el fin del programa.",tokens[ig].line)
    return temp

def error(op, token, line):
    global errors, ig
    if op == 0:
        errors.append("Error. Se esperaba '" + token + "' en la linea " + line)
        #print("Error. Se esperaba '" + token + "'. En la linea " + line)
    else:
        errors.append(token + " en la linea " + line)
        #print(token + " En la linea " + line)

def verNodo(nodo):
    if(nodo != None):
        print("Nodo-> " + str(nodo.nombre))
        print("Dato-> " + str(nodo.dato))
        print("Tipo-> " + str(nodo.tipo))
        print("Valor-> " + str(nodo.valor))
        print('\n')
        for s in nodo.sibling:
            verNodo(s)
        verNodo(nodo.hijo[0])
        verNodo(nodo.hijo[1])
        verNodo(nodo.hijo[2])
    return

if __name__== "__main__":
    raiz = programa()
    verNodo(raiz)

    for has in hash:
        if has != None:
            print(str(has[0]) + "#" + str(has[1]) + "#" + str(has[2]) + "#")
            print('|'.join(has[3]) + "\n")
