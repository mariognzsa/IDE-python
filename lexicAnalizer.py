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
        operators = '+-<>=|!/*:;'
        spacesAndStuff = ' \n'  # Pls rename later
        specialCharacters = '}{)(][%,'
        self.tokens = []  # Array of found tokens
        currentToken = ''
        tokenType = ''
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
                    tokenError = False
                    decimalPoints = 0
                    while number and decimalPoints <= 1:  # Loop just for numbers and one decimalpoint max
                        if inputCode[cIndex] in numbers:
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                        elif inputCode[cIndex] == '.':
                            if decimalPoints < 1 and inputCode[cIndex+1] in numbers: # Turns on a flag to differenciate int and float
                                currentToken += inputCode[cIndex]
                                floatingNumber = True
                            else:
                                tokenError = True                   
                            cIndex += 1
                            decimalPoints += 1
                            
                        else:
                            number = False
                    if tokenError:
                        tokenType = 'error'
                    else:
                        if floatingNumber:
                            tokenType = 'float'
                        else:
                            tokenType = 'integer'
                    tokenEnd = cIndex
                    cIndex -= 1

                elif inputCode[cIndex] in operators: # Checking if is an operator, btw unnecessary cases lol
                    tokenStart = cIndex
                    if inputCode[cIndex] == '<':
                        tokenType = 'operator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '>':
                        tokenType = 'operator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '=': # changed to work only with ==
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            tokenType = 'operator'
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                        else:
                            tokenType = 'error'

                    elif inputCode[cIndex] == '!':
                        tokenType = 'operator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '+':
                        tokenType = 'operator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=' or inputCode[cIndex] == '+': # special cases for ++ and +=, considering them as operators
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '-':
                        tokenType = 'operator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=' or inputCode[cIndex] == '-':
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    elif inputCode[cIndex] == '*':
                        tokenType = 'operator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                    elif inputCode[cIndex] == '/':
                        tokenType = 'operator'
                        cIndex += 1
                        if inputCode[cIndex] != '/' and inputCode[cIndex] != '*':
                            currentToken += inputCode[cIndex-1]
                        if inputCode[cIndex] == '/': # case // for one line comments
                            cIndex += 1
                            if inputCode[cIndex] == '\n':
                                currentToken = ' '
                            while inputCode[cIndex] != '\n':
                                currentToken += inputCode[cIndex]
                                cIndex += 1
                            tokenType = 'oneline_commentary'
                        elif inputCode[cIndex] == '*': # case /* for multiline comments
                            cIndex += 1
                            commentary = False
                            if inputCode[cIndex] == '\n':
                                currentToken = ' '
                            while commentary == False and cIndex < len(inputCode): # Loop multiline comments
                                if inputCode[cIndex] != '*':
                                    currentToken += inputCode[cIndex]
                                    cIndex += 1
                                else:
                                    if inputCode[cIndex+1] == '/':
                                        cIndex += 2
                                        currentToken += inputCode[cIndex]
                                        if currentToken == '\n':
                                            currentToken = ' \n'
                                        commentary = True
                                    else:
                                        currentToken += inputCode[cIndex]
                                        cIndex += 1
                            currentToken = currentToken[0:len(currentToken)-1]
                            tokenType = 'multiline_commentary'
                    
                    elif inputCode[cIndex] == ':':
                        currentToken += inputCode[cIndex]
                        cIndex += 1
                        if inputCode[cIndex] == '=':
                            tokenType = 'operator'
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                        else:
                            tokenType = 'error'

                    elif inputCode[cIndex] == ';':
                        tokenType = 'end_sentence'
                        currentToken += inputCode[cIndex]
                        cIndex += 1

                    elif inputCode[cIndex] == ',':
                        tokenType = 'separator'
                        currentToken += inputCode[cIndex]
                        cIndex += 1

                    else:                                       # if not one of above, no need in checking for further chars
                        currentToken += inputCode[cIndex]
                    tokenEnd = cIndex
                    cIndex -= 1

                #elif inputCode[cIndex] not in charsetExtended and inputCode[cIndex] not in numbers and inputCode[cIndex] not in operators and inputCode[cIndex] not in spacesAndStuff:
                    # Considered special character if not in the above alphabets
                    # Deprecated
                elif inputCode[cIndex] in specialCharacters: # 
                    tokenStart = cIndex
                    tokenEnd = cIndex+1
                    currentToken += inputCode[cIndex]
                    tokenType = 'special_character'
                
                elif inputCode[cIndex] not in spacesAndStuff: 
                    # if it doesnt enter any if above and its not a space or line break it's an error????:0
                    #print('hell')
                    tokenStart = cIndex
                    tokenEnd = cIndex+1
                    tokenType = 'error'
                    currentToken += inputCode[cIndex]
                    #cIndex += 1
                    tokenError = False
                    #This part manages another kind of errors such as an Uppercase letter at the beginning of a word

                if len(currentToken) > 0 and tokenType != '': # Checking token and tokentype not empty
                    if currentToken in restricted: # If the token content is a restricted word we manage it
                        tokenType = 'restricted_word'
                    tokenInfo = Token(tkIndex, tokenType, currentToken, tokenStart, tokenEnd)
                    self.tokens.append(tokenInfo)
                    tokenType = ''
                    currentToken = ''
                    tkIndex += 1

                #if tokenType == '' or tokenError:
                #    tokenType = 'error'
                #    currentToken += inputCode[cIndex]
                #    currentToken = currentToken[0:len(currentToken)-1]
                #    tokenError = False

            cIndex += 1

