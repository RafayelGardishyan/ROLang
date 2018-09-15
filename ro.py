from sys import *
from time import gmtime, strftime

symbols = {}

def file_opener(file):
    read = open(file, 'r').read()
    # import pdb; pdb.set_trace()
    return read + "<EOF>"

def lexer(content):
    string = 0
    token = ""
    num = 0
    exp = 0
    tokens = []
    for letter in content:
        # import pdb; pdb.set_trace()
        # if "6 is equal to variable SIX$" in token:
        #     import pdb; pdb.set_trace()
        token += letter
        if token == " " and string != 1 and exp != 1:
            token = ""
        elif token == "\n" or token == "\r":
            token = ""
        elif token == "\t":
            token = ""
        elif token == "<EOF>":
            token == ""
        elif "$" in token and string == 0:
            if string != 1 and num != 1 and exp != 1:
                tokens.append("VAR:" + token[:-1])
                token = ""
        elif token == "=":
            tokens.append("EQUALS")
            token = ""
        elif num == 1:
            if "ENDINT" in token:
                tokens.append("NUM:" + token[:-7])
                token = ""
                num = 0
        elif exp == 1:
            if "ENDEXP" in token:
                tokens.append("EXP:" + token[:-7])
                token = ""
                exp = 0
        elif string == 1:
            if '"' in token:
                tokens.append("STRING:" + '"' + token[:-1] + '"')
                token = ""
                string = 0
        elif token == "IF":
            tokens.append(token)
            token = ""
        elif token == "THEN":
            tokens.append(token)
            token = ""
        elif token == "ENDIF":
            tokens.append(token)
            token = ""
        elif token == "DISPLAY":
            tokens.append(token)
            token = ""
        elif token == "INPUT":
            tokens.append(token)
            token = ""
        elif token == '"':
            if string == 0:
                string = 1
                token = ""
        elif token == "INT" and string != 1:
            if num == 0:
                num = 1
                token = ""
        elif token == "EXP" and string != 1:
            if exp == 0:
                exp = 1
                token = ""

    # print(tokens)
    #return ''
    return tokens

def evalResult(value):
    return eval(value)

def doAssign(varname,varvalue):
    symbols[varname] = varvalue

def doAssignVar(varname,varvalue):
    symbols[varname] = varvalue

def getInput(text):
    inputS = input(text + " ")
    return inputS

def doPrint(value):
    if len(value) >= 6:
        if value[0:6] == "STRING":
            print(value[7:])
        elif value[0:3] == "NUM":
            print(value[4:])
        elif value[0:3] == "EXP":
            print(evalResult(value[4:]))
        elif value[0:3] == "VAR":
            print(symbols[value[4:]])

    else:
        if value[0:3] == "NUM":
            print(value[4:])
        elif value[0:3] == "EXP":
            print(evalResult(value[4:]))
        elif value[0:3] == "VAR":
            print(symbols[value[4:]])

def parse(toks):
    for i in range(5):
        toks.append("<EOF>")
    i = 0
    IF = 0
    while i < len(toks):
        if toks[i] == "<EOF>":
            break
        elif IF == 0 and toks[i] + " " + toks[i + 1][0:6] == "DISPLAY STRING" or toks[i] + " " + toks[i + 1][0:3] == "DISPLAY NUM" or toks[i] + " " + toks[i + 1][0:3] == "DISPLAY EXP" or toks[i] + " " + toks[i + 1][0:3] == "DISPLAY VAR":
            doPrint(toks[i+1])
            i += 2
        elif IF == 0 and toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING":
            doAssign(toks[i][4:], toks[i+2][7:])
            i += 3
        elif IF == 0 and toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM":
            doAssign(toks[i][4:], toks[i+2][4:])
            i += 3
        elif IF == 0 and toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS EXP":
            doAssign(toks[i][4:], evalResult(toks[i+2][4:]))
            i += 3
        elif IF == 0 and toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            doAssign(toks[i][4:], symbols[toks[i+2][4:]])
            i += 3
        elif IF == 0 and toks[i][0:5] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
            doAssign(toks[i+2][4:], getInput(toks[i+1][7:]))
            i += 3
        elif IF == 0 and toks[i][0:5] + " " + toks[i+1][0:3] + " " + toks[i+2][0:3] == "INPUT NUM VAR":
            doAssign(toks[i+2][4:], getInput(toks[i+1][4:]))
            i += 3
        elif IF == 0 and toks[i][0:5] + " " + toks[i+1][0:3] + " " + toks[i+2][0:3] == "INPUT EXP VAR":
            doAssign(toks[i+2][4:], getInput(evalResult(toks[i+1][4:])))
            i += 3
        elif toks[i] == "IF":
            IF = 1
            if toks[i+1][0:3] == "NUM":
                # print(toks[i+1])
                first = toks[i+1][4:]
            elif toks[i+1][0:3] == "EXP":
                first = evalResult(toks[i+1][4:])
            elif toks[i+1][0:3] == "VAR":
                first = symbols[toks[i+1][4:]]
            elif toks[i+1][0:6] == "STRING":
                first = toks[i+1][7:]
            if toks[i+3][0:3] == "NUM":
                # print(toks[i+3])
                second = toks[i+3][4:]
            elif toks[i+3][0:3] == "EXP":
                second = evalResult(toks[i+3][4:])
            elif toks[i+3][0:3] == "VAR":
                second = symbols[toks[i+3][4:]]
            elif toks[i+3][0:3] == "STRING":
                second = toks[i+3][7:]

            if first == second:
                # print(first, second)
                IF = 0

            i += 4
        elif toks[i] == "ENDIF":
            IF = 0
            i += 1
        else:
            i +=1


def run(file=None):
    if file != None:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " RO Compiler ==> running: " + file + "\n")
        tokens = lexer(file_opener(file))
        parse(tokens)
    else:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " RO Shell ==> running inline commands \n")
        while(True):
            inp = input("->> ")
            if inp == "EXIT":
                quit()
            tokens = lexer(inp + " <EOF>")
            parse(tokens)
            #print(symbols)

if len(argv) > 1:
    run(argv[1])
else:
    run()
