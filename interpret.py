import argparse
from pickle import NONE
import sys
import xml.etree.ElementTree as ET

from numpy import trim_zeros


class frame:
    types={
        0: "GF",
        1: "LF",
        2: "TF"
    }

    def __init__(self, type):
        self.type = type
        self.items={}
        self.len = 0

class symtableClass:
    TF = None
    
    def __init__(self):
        self.frames = []
        self.frames.append(frame("GF"))
        self.maxIndex = 0

    def popFrame(self):
        if self.maxIndex < 1:
            print("Error - Unexisted LF frame", file = sys.stderr)
            exit(55)

        popedFrame = self.frames.pop()
        popedFrame.type = "TF"
        self.TF = popedFrame
        self.maxIndex = self.maxIndex - 1
    
    def createFrame(self):
        self.TF = frame("TF")

    def pushFrame(self, frame):
        frame.type = "LF"
        self.frames.append(frame)
        self.TF = None
        self.maxIndex = self.maxIndex + 1

    def findItem(self, item):
        varSplit = item.split("@")
        frame = varSplit[0]
        if frame == "GF":
            try:
                return self.frames[0].items[varSplit[1]]
            except:
                return False
        elif frame == "LF":
            if self.maxIndex < 1:
                print("Error - Unexisted LF frame", file = sys.stderr)
                exit(55)

            try:
                return self.frames[self.maxIndex].items[varSplit[1]]
            except:
                return False
        elif frame == "TF":
            if self.TF == None:
                print("Error - Unexisted TF frame", file = sys.stderr)
                exit(55)
            try:
                return self.TF.items[varSplit[1]]
            except:
                return False
        else:
            print("Internal ERROR", file = sys.stderr)
            exit(99)

    def updateItem(self, item, newValue, newDataType):
        varSplit = item.split("@")
        frame = varSplit[0]
        variableName = varSplit[1]
        if frame == "LF":
            self.TF.items[variableName] = [newValue, newDataType]
        elif frame == "GF":
            self.frames[0].items[variableName] = [newValue, newDataType]
        else:
            self.frames[self.maxIndex].items[variableName] = [newValue, newDataType]



    def appendItem(self,item):
        varSplit = item.split("@")
        if not self.findItem(item):
            if varSplit[0] == "GF":
                self.frames[0].items[varSplit[1]] = [None, None]                
            elif varSplit[0] == "LF":
                self.frames[self.maxIndex].items[varSplit[1]] = [None, None]                
            else:
                self.TF.items[varSplit[1]] = [None, None]                
        
        else:
            print("Error - Redefinition of variable", file = sys.stderr)
            exit(52)



class interpreter:
    
    def __init__(self, arrayOfLabels):
        self.symtable = symtableClass()
        self.arrayOfLabels = arrayOfLabels
        self.stack = []


    instructions ={
        "MOVE": ["var", "symb"],#0
        "CREATEFRAME": [None],#1
        "PUSHFRAME": [None],#2
        "POPFRAME": [None],#3
        "DEFVAR": ["var"],#4
        "CALL": ["label"],#5
        "RETURN": [None],#6
        "PUSHS": ["symb"],#7
        "POPS": ["var"],#8
        "ADD": ["var", "symb", "symb"],#9
        "SUB": ["var", "symb", "symb"],#10
        "MUL": ["var", "symb", "symb"],#11
        "IDIV": ["var", "symb", "symb"],#12
        "LT": ["var", "symb", "symb"],#13
        "GT": ["var", "symb", "symb"],#14
        "EQ": ["var", "symb", "symb"],#15
        "AND": ["var", "symb", "symb"],#16
        "OR": ["var", "symb", "symb"],#17
        "NOT": ["var", "symb", "symb"],#18
        "INT2CHAR": ["var", "symb"],#19
        "STRI2INT": ["var", "symb", "symb"],#20
        "READ": ["var", "type"],#21
        "WRITE": ["symb"],#22
        "CONCAT": ["var", "symb", "symb"],#23
        "STRLEN": ["var", "symb"],#24
        "GETCHAR": ["var", "symb", "symb"],#25
        "SETCHAR": ["var", "symb", "symb"],#26
        "TYPE": ["var", "symb"],#27
        "LABEL": ["label"],#28
        "JUMP": ["label"],#29
        "JUMPIFEQ": ["label", "symb", "symb"],#30
        "JUMPIFNEQ": ["label", "symb", "symb"],#31
        "EXIT": ["symb"],#32
        "DPRINT": ["symb"],#33
        "BREAK": [None]#34
    }

    def isVariable(self, arg):
        if arg.attrib.get('type') == "var":
            return True
        else:
            return False   

    def isLabel(self, arg):
        if arg.attrib.get('type') == "label":
            return True
        else:
            return False   

    def isConstant(self, arg):
        if arg.attrib.get('type') == "string" or arg.attrib.get('type') == "bool" or arg.attrib.get('type') == "nil" or arg.attrib.get('type') == "int":
            return True
        else:
            return False  

    def isString(self, arg):
        if arg.attrib.get('type') == "string":
            return True
        else:
            return False 

    def isSymb(self, instruction, argNumber):
        if self.isVariable(instruction.find(argNumber)):
            symbIsVar = True
            symb = instruction.find(argNumber).text
            symtableItem = self.symtable.findItem(symb)

            if not symtableItem:
                print("Error - Unexisted variable", file = sys.stderr)
                exit(54)
            else:
                symbDataType = symtableItem[1]
                symbValue = symtableItem[0]

        elif self.isConstant(instruction.find(argNumber)):
            symbIsVar = False
            symbValue = instruction.find(argNumber).text
            symbDataType = instruction.find(argNumber).attrib.get('type')

        else:
            print("Error - bad operand type", file = sys.stderr)
            exit(53)
        return symbIsVar, symbValue, symbDataType


    def instructionOpeartions(self, opcode,instruction, i):
        
        if opcode == list(self.instructions.keys())[0]: #MOVE

            if self.isVariable(instruction.find('arg1')):

                var = instruction.find('arg1').text
                symtableItem = self.symtable.findItem(var)

                if not symtableItem:
                    print("Error - Unexisted variable", file = sys.stderr)
                    exit(54)
                else:
                    varDataType = symtableItem[1]

            else:
                print("Error - bad operand type", file = sys.stderr)
                exit(53)

            symbIsVar = False
            if self.isVariable(instruction.find('arg2')):
                symbIsVar = True
                symb = instruction.find('arg2').text
                symtableItem = self.symtable.findItem(symb)

                if not symtableItem:
                    print("Error - Unexisted variable", file = sys.stderr)
                    exit(54)
                else:
                    symbDataType = symtableItem[1]
                    symbValue = symtableItem[0]

            elif self.isConstant(instruction.find('arg2')):
                symbIsVar = False
                symb = instruction.find('arg2').text
                symbDataType = instruction.find('arg2').attrib.get('type')

            else:
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            
            if symbIsVar:
                self.symtable.updateItem(var,symbValue, symbDataType)
            else:
                self.symtable.updateItem(var,symb, symbDataType)

            
        elif opcode == list(self.instructions.keys())[1]:#CRETEFRAME
            self.symtable.createFrame()

        elif opcode == list(self.instructions.keys())[2]:#PUSHFRAME
            self.symtable.pushFrame(self.symtable.TF)

        elif opcode == list(self.instructions.keys())[3]:#POPFRAME
            self.symtable.popFrame()

        elif opcode == list(self.instructions.keys())[4]:#DEFVAR
            if self.isVariable(instruction.find('arg1')):
                var = instruction.find('arg1').text
                self.symtable.appendItem(var)

            else:
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
        elif opcode == list(self.instructions.keys())[5]:#CALL
            self.stack.append([i, 'label'])
            if self.isLabel(instruction.find('arg1')):
                try:
                    i = self.arrayOfLabels[instruction.find('arg1').text]
                except:
                    print("Error - Undefined LABEL call", file = sys.stderr)
                    exit(52)

            else:
                print("Error - Call without valid LABEL", file = sys.stderr)
                exit(53)

        elif opcode == list(self.instructions.keys())[6]:#RETURN
            if len(self.stack) > 0:
                poppedValue = self.stack.pop()
                i = poppedValue[0]
            else:
                print("Error - Empty stack", file = sys.stderr)
                exit(56)


        elif opcode == list(self.instructions.keys())[7]:#PUSHS
            symbIsVar, symbValue, symbDataType = self.isSymb(instruction, 'arg1')
            #TODO osetrit None ak sa jedna o premennu, treba poriesit co s praznou premennou v symtable
            self.stack.append([symbValue, symbDataType])

        elif opcode == list(self.instructions.keys())[8]:#POPS
            if len(self.stack) > 0:
                if self.isVariable(instruction.find('arg1')):
                    poppedValue = self.stack.pop()
                    self.symtable.updateItem(instruction.find('arg1').text, poppedValue[0], poppedValue[1])
                else:
                    print("Error - bad operand type", file = sys.stderr)
                    exit(53)

            else:
                print("Error - Empty stack", file = sys.stderr)
                exit(56)

        elif opcode == list(self.instructions.keys())[9]:#ADD
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            result = symbValue1 + symbValue2
            self.symtable.updateItem(self.symtable.findItem(instruction.find('arg1').text), result, 'int')

        elif opcode == list(self.instructions.keys())[10]:#SUB
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            result = symbValue1 - symbValue2
            self.symtable.updateItem(self.symtable.findItem(instruction.find('arg1').text), result, 'int')

            
        elif opcode == list(self.instructions.keys())[11]:#MUL
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            result = symbValue1 * symbValue2
            self.symtable.updateItem(self.symtable.findItem(instruction.find('arg1').text), result, 'int')

            
        elif opcode == list(self.instructions.keys())[12]:#IDIV
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                exit(53)
            if symbValue2 == '0':
                print("Error - Dividing by 0", file = sys.stderr)
                exit(57)
            
            result = symbValue1 // symbValue2
            self.symtable.updateItem(self.symtable.findItem(instruction.find('arg1').text), result, 'int')

            
        elif opcode == list(self.instructions.keys())[13]:#LT
            pass
        elif opcode == list(self.instructions.keys())[14]:#GT
            pass
        elif opcode == list(self.instructions.keys())[15]:#EQ
            pass
        elif opcode == list(self.instructions.keys())[16]:#AND
            pass
        elif opcode == list(self.instructions.keys())[17]:#OR
            pass
        elif opcode == list(self.instructions.keys())[18]:#NOT
            pass
        elif opcode == list(self.instructions.keys())[19]:#INT2CHAR
            pass
        elif opcode == list(self.instructions.keys())[20]:#STRI2INT
            pass
        elif opcode == list(self.instructions.keys())[21]:#READ
            pass
        elif opcode == list(self.instructions.keys())[22]:#WRITE
            pass
        elif opcode == list(self.instructions.keys())[23]:#CONCAT
            pass
        elif opcode == list(self.instructions.keys())[24]:#STRLEN
            pass
        elif opcode == list(self.instructions.keys())[25]:#GETCHAR
            pass
        elif opcode == list(self.instructions.keys())[26]:#SETCHAR
            pass
        elif opcode == list(self.instructions.keys())[27]:#TYPE
            pass
        elif opcode == list(self.instructions.keys())[28]:#LABEL
            pass
        elif opcode == list(self.instructions.keys())[29]:#JUMP
            pass
        elif opcode == list(self.instructions.keys())[30]:#JUMPIFEQ
            pass
        elif opcode == list(self.instructions.keys())[31]:#JUMPIFNEQ
            pass
        elif opcode == list(self.instructions.keys())[32]:#EXIT
            pass
        elif opcode == list(self.instructions.keys())[33]:#DPRINT
            pass
        elif opcode == list(self.instructions.keys())[34]:#BREAK
            pass
        return i+1


class xmlReader:

    instructionOrder = 0

    def __init__(self, sourceFile):
        if(sourceFile != None):
            try:
                tree = ET.parse(sourceFile)

            except: 
                print("Error - invalid file name or unable to open file for reading", file = sys.stderr)
                exit(11)

            self.root = tree.getroot()
        else:
            tree = input()
            self.root = ET.fromstring(tree)



    def orderChecker(self, externalOrder):
        if int(self.instructionOrder) < int(externalOrder):
            self.instructionOrder = externalOrder
            return True
        else:
            print("Error - invalide instruction order", file = sys.stderr)
            exit(32)

    def getOpcode(self, instruction):
        return instruction.attrib.get('opcode')

    def isXMLCorrect(self):
        if self.root.findall('arg1') or self.root.findall('arg2') or self.root.findall('arg3') :
            print("Error - invalid XML", file = sys.stderr)
            exit(32)

        if self.root.tag != "program" or self.root.attrib.get('language') != "IPPcode22":
            print("Error - invalid XML program attribute", file = sys.stderr)
            exit(31)

        # TODO check xml version and encoding


    

def arguments():    
    isHelp = False
    source= None
    input = None
    isProgram = False

    if len(sys.argv) > 3 :
        print("Error in arguments", file = sys.stderr)
        exit(10)
    for arg in sys.argv:
        if isProgram:
            if(arg.find('--source=') != -1):
                source = arg.replace('--source=', '')
            elif (arg.find('--input=') != -1):
                input = arg.replace('--input=', '')
            elif(arg.find('--help') != -1):
                isHelp = True
            else:
                print("Error in arguments", file = sys.stderr)
                exit(10)
        isProgram = True

    if isHelp and (source != None or input != None):
        print("Error in arguments", file = sys.stderr)
        exit(10)
    
    if isHelp:
        print("IPP interpret.py by Dalibor Kralik")
        print("")
        print("Optional arguments:")
        print("     --help              write help of the program")
        print("     --source  SOURCE    source file of the program")
        print("     --input   INPUT     input file of the program")
        exit(0)
    
    if source == None and input == None:
        print("Error in arguments", file = sys.stderr)
        exit(10)

    return source, input
    


def sortingCriteria(instruction):
    return int(instruction.attrib.get('order'))



def programmeRunner(sourceFile):
    reader = xmlReader(sourceFile)
    listOfInstructions=[]

    
        # Checking correct XML structure
    reader.isXMLCorrect()
    arrayOfLabels = {}


        # Creating listOfInstrucitons
    for instruction in reader.root.iter('instruction'):
        listOfInstructions.append(instruction)
    
        # Sorting of instructions and check order
    listOfInstructions.sort(key=sortingCriteria)
    
    counterIndex = -1
    for instruction in listOfInstructions:
        counterIndex = counterIndex + 1
        reader.orderChecker(instruction.attrib.get('order'))

            # check redefinition of LABEL
        if((instruction.attrib.get('opcode').upper()) == "LABEL"):
            try:
                if(arrayOfLabels[instruction.find('arg1').text]):
                    print("Error - redefinition of LABEL", file = sys.stderr)
                    exit(52)
            except:
                arrayOfLabels[instruction.find('arg1').text] = counterIndex 


    #print(arrayOfLabels)        
    # TODO ak budem kontrolovat existenciu LABELu, pouzi pole arrayOfLabels cez try-except a hlada kluc
    # TODO  Prechadzanie instrukcii

    interpret = interpreter(arrayOfLabels)
    for i in range(len(listOfInstructions)):
        i = interpret.instructionOpeartions(listOfInstructions[i].attrib.get('opcode').upper(),listOfInstructions[i], i)
    



if __name__ == '__main__':
    sourceFile, inputFile = arguments()
    print(sourceFile, inputFile)
    programmeRunner(sourceFile)




