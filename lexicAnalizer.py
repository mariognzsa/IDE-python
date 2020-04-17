# LexicAnalizer v1.0

class Token:
    def __init__(self, id, tokenType, token, start, end):
        self.id = id
        self.tokenType = tokenType
        self.token = token
        self.start = start
        self.end = end

class LexicAnalizer:
    def __init__(self):
        self.tokens = []

    def analizeCode(self, inputCode, *args):
        state = 0
        restricted = [  # List of restricted words
            'main', 
            'if', 
            'then', 
            'else', 
            'end',
            'do', 
            'while', 
            'cin', 
            'cout', 
            'real', 
            'int', 
            'boolean',
            'float',
            'char'
        ]
        charset = 'abcdefghijklmnopqrstuvwxyz' # array permitted for identifier's first character
        charsetExtended = 'abcdefghijklmnopqrstuvwxyz_1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        operators = '+-<>=|!/*'
        spacesAndStuff = ' \n'  # Pls rename later
        self.tokens = []  # Array of found tokens
        currentToken = ''
        tokenStart = 0
        tokenEnd = 0
        cIndex = 0   # index for current character
        tkIndex = 0 #  index for the current token
        while cIndex < len(inputCode):
            # print('char: ' + inputCode[cIndex] + ' state: ' + str(state))  #debug current character and the state

            if state == 0:
                if inputCode[cIndex] in charset: # Checking for identifier (frst letter lowercase)
                    currentToken += inputCode[cIndex]
                    tokenStart = cIndex
                    cIndex += 1
                    while inputCode[cIndex] in charsetExtended: # Checking on extended charset w / uppercase and numbers
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                    tokenType = 'identifier'
                    tokenEnd = cIndex
                    cIndex -= 1

                elif inputCode[cIndex] in numbers: # Checking for number appearances
                    currentToken += inputCode[cIndex]
                    tokenStart = cIndex
                    cIndex += 1
                    number = True
                    floatingNumber = False
                    decimalPoints = 0
                    while number and decimalPoints <= 1:  # Loop just for numbers and one decimalpoint max
                        if inputCode[cIndex] in numbers:
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                        elif inputCode[cIndex] == '.':
                            if decimalPoints < 1 and inputCode[cIndex+1] in numbers: # Turns on a flag to differenciate int and float
                                currentToken += inputCode[cIndex]
                                floatingNumber = True                          
                            cIndex += 1
                            decimalPoints += 1
                            
                        else:
                            number = False
                    if floatingNumber:
                        tokenType = 'float'
                    else:
                        tokenType = 'integer'
                    tokenEnd = cIndex
                    cIndex -= 1
                    
                elif inputCode[cIndex] == '/' and (inputCode[cIndex+1] == '/' or inputCode[cIndex+1] == '*'): # Checking for commentary lines
                    tokenStart = cIndex
                    cIndex += 1
                    if inputCode[cIndex] == '/': # case // for one line comments
                        cIndex += 1
                        while inputCode[cIndex] != '\n':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                        tokenType = 'oneline_commentary'
                    elif inputCode[cIndex] == '*': # case /* for multiline comments
                        cIndex += 1
                        commentary = False
                        while commentary == False and cIndex < len(inputCode): # Loop multiline comments
                            if inputCode[cIndex] != '*':
                                currentToken += inputCode[cIndex]
                                cIndex += 1
                            else:
                                if inputCode[cIndex+1] == '/':
                                    cIndex += 1
                                    commentary = True
                                else:
                                    currentToken += inputCode[cIndex]
                                    cIndex += 1

                        tokenType = 'multiline_commentary'
                    tokenEnd = cIndex

                elif inputCode[cIndex] in operators: # Checking if is an operator, btw unnecessary cases lol
                    tokenStart = cIndex
                    if inputCode[cIndex] == '<':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '>':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '=':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '!':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '+':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=' or inputCode[cIndex] == '+': # special cases for ++ and +=, considering them as operators
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '-':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=' or inputCode[cIndex] == '-':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    else:                                       # if not one of above, no need in checking for further chars
                        currentToken += inputCode[cIndex]
                    tokenType = 'operator'
                    tokenEnd = cIndex
                    cIndex -= 1
                    
                elif inputCode[cIndex] not in charsetExtended and inputCode[cIndex] not in numbers and inputCode[cIndex] not in operators and inputCode[cIndex] not in spacesAndStuff:
                    # Considered special character if not in the above alphabets
                    tokenStart = cIndex
                    tokenEnd = cIndex+1
                    currentToken += inputCode[cIndex]
                    tokenType = 'special_character'

                if len(currentToken) > 0 and tokenType != '': # Checking token and tokentype not empty
                    if currentToken in restricted: # If the token content is a restricted word we manage it
                        tokenType = 'restricted_word'
                    tokenInfo = Token(tkIndex, tokenType, currentToken, tokenStart, tokenEnd)
                    self.tokens.append(tokenInfo)
                    tokenType = ''
                    currentToken = ''
                    tkIndex += 1
            cIndex += 1

