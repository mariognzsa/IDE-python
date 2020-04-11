# Analizador Lexico

import sys, getopt

def main(argv):
    
    inputCode = argv[0] # Getting first argument as the whole string of code
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
        'boolean'
    ]
    charset = 'abcdefghijklmnopqrstuvwxyz' # array permitted for identifier's first character
    charsetExtended = 'abcdefghijklmnopqrstuvwxyz_1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    tokens = []  # Array of founded tokens
    currentToken = ''
    cIndex = 0   # index for current character
    tkIndex = 0 #  index for the current token
    while cIndex < len(inputCode):
        # print('char: ' + inputCode[cIndex] + ' state: ' + str(state))  #debug current character and the state

        if state == 0:
            if inputCode[cIndex] in charset: # Checking for identifier (frst letter lowercase)
                currentToken += inputCode[cIndex]
                cIndex += 1
                while inputCode[cIndex] in charsetExtended: # Checking on extended charset w / uppercase and numbers
                    currentToken += inputCode[cIndex]
                    cIndex += 1
                tokenType = 'identifier'

            elif inputCode[cIndex] == '/': # Checking for commentary lines
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
                        if inputCode[cIndex] == '*':
                            cIndex += 1
                            if inputCode[cIndex] == '/':
                                cIndex += 1
                                commentary = True
                            else:
                                cIndex += 1
                                currentToken += '*'
                        else:
                            currentToken += inputCode[cIndex]
                            cIndex += 1
                    tokenType = 'multiline_commentary'

            if len(currentToken) > 0 and tokenType != '': # Checking token and tokentype not empty
                if currentToken in restricted: # If the token content is a restricted word we manage it
                    tokenType = 'restricted_word'
                tokenInfo = [tkIndex, currentToken, tokenType]
                tokens.append(tokenInfo)
                tokenType = ''
                currentToken = ''
                tkIndex += 1
        cIndex += 1    
            
    for token in tokens:
        print(str(token))

    
if __name__ == "__main__":
    main(sys.argv[1:])

