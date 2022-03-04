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
        self.items = []
        self.items.append(frame("GF"))
        self.maxIndex = 0

    def popFrame(self):
        if self.maxIndex < 1:
            print("Error - Unexisted LF frame", file = sys.stderr)
            exit(55)

        popedFrame = self.items.pop()
        popedFrame.type = "TF"
        self.TF = popedFrame
        self.maxIndex = self.maxIndex - 1
    
    def createFrame(self):
        self.TF = frame("TF")

    def pushFrame(self, frame):
        frame.type = "LF"
        self.items.append(frame)
        self.TF = None
        self.maxIndex = self.maxIndex + 1

    def findItem(self, item):
        varSplit = item.split("@")
        frame = varSplit[0]
        if frame == "GF":
            try:
                return self.items[0].items[varSplit[1]]
            except:
                return False
        elif frame == "LF":
            if self.maxIndex < 1:
                print("Error - Unexisted LF frame", file = sys.stderr)
                exit(55)

            try:
                return self.items[self.maxIndex].items[varSplit[1]]
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
            self.items[0].items[variableName] = [newValue, newDataType]
        else:
            self.items[self.maxIndex].items[variableName] = [newValue, newDataType]




    #TODO prerobit, nesedi to napr pri tvorbe GF premennej, treba asi rozifovat
    def appendItem(self, itemKey, itemValue, itemDataType, frame):
        newVariable = frame+"@"+itemKey
        if not self.findItem(newVariable):
            self.items[self.maxIndex].items[itemKey] = [itemValue,itemDataType]
        else:
            print("Error - redefinition of variable", file = sys.stderr)
            exit(52)



class interpreter:
    
    def __init__(self, arrayOfLabels):
        self.symtable = symtableClass()
        self.arrayOfLabels = arrayOfLabels


    instructions ={
        "MOVE": ["var", "symb"],
        "CREATEFRAME": [None],
        "PUSHFRAME": [None],
        "POPFRAME": [None],
        "DEFVAR": ["var"],
        "CALL": ["label"],
        "RETURN": [None],
        "PUSHS": ["symb"],
        "POPS": ["var"],
        "ADD": ["var", "symb", "symb"],
        "SUB": ["var", "symb", "symb"],
        "MUL": ["var", "symb", "symb"],
        "IDIV": ["var", "symb", "symb"],
        "LT": ["var", "symb", "symb"],
        "GT": ["var", "symb", "symb"],
        "EQ": ["var", "symb", "symb"],
        "AND": ["var", "symb", "symb"],
        "OR": ["var", "symb", "symb"],
        "NOT": ["var", "symb", "symb"],
        "INT2CHAR": ["var", "symb"],
        "STRI2INT": ["var", "symb", "symb"],
        "READ": ["var", "type"],
        "WRITE": ["symb"],
        "CONCAT": ["var", "symb", "symb"],
        "STRLEN": ["var", "symb"],
        "GETCHAR": ["var", "symb", "symb"],
        "SETCHAR": ["var", "symb", "symb"],
        "TYPE": ["var", "symb"],
        "LABEL": ["label"],
        "JUMP": ["label"],
        "JUMPIFEQ": ["label", "symb", "symb"],
        "JUMPIFNEQ": ["label", "symb", "symb"],
        "EXIT": ["symb"],
        "DPRINT": ["symb"],
        "BREAK": [None]
    }

    def isVariable(arg):
        if arg.attrib.get('type').text == "var":
            return True
        else:
            return False   

    def isLabel(arg):
        if arg.attrib.get('type').text == "label":
            return True
        else:
            return False   

    def isConstant(arg):
        if arg.attrib.get('type').text == "string" or arg.attrib.get('type').text == "bool" or arg.attrib.get('type').text == "nil" or arg.attrib.get('type').text == "int":
            return True
        else:
            return False  

    def isString(arg):
        if arg.attrib.get('type').text == "string":
            return True
        else:
            return False 


    def instructionOpeartions(self, opcode,instruction, i):
        #print(self.instructions.keys())
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
                symbDataType = instruction.find('arg2').attrib.get('type').text

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
            pass
        elif opcode == list(self.instructions.keys())[5]:#CALL
            pass
        elif opcode == list(self.instructions.keys())[6]:
            pass
        elif opcode == list(self.instructions.keys())[7]:
            pass
        elif opcode == list(self.instructions.keys())[8]:
            pass
        elif opcode == list(self.instructions.keys())[10]:
            pass
        elif opcode == list(self.instructions.keys())[11]:
            pass
        elif opcode == list(self.instructions.keys())[12]:
            pass
        elif opcode == list(self.instructions.keys())[13]:
            pass
        elif opcode == list(self.instructions.keys())[14]:
            pass
        elif opcode == list(self.instructions.keys())[15]:
            pass
        elif opcode == list(self.instructions.keys())[16]:
            pass
        elif opcode == list(self.instructions.keys())[17]:
            pass
        elif opcode == list(self.instructions.keys())[18]:
            pass
        elif opcode == list(self.instructions.keys())[19]:
            pass
        elif opcode == list(self.instructions.keys())[20]:
            pass
        elif opcode == list(self.instructions.keys())[21]:
            pass
        elif opcode == list(self.instructions.keys())[22]:
            pass
        elif opcode == list(self.instructions.keys())[23]:
            pass
        elif opcode == list(self.instructions.keys())[24]:
            pass
        elif opcode == list(self.instructions.keys())[25]:
            pass
        elif opcode == list(self.instructions.keys())[26]:
            pass
        elif opcode == list(self.instructions.keys())[27]:
            pass
        elif opcode == list(self.instructions.keys())[28]:
            pass
        elif opcode == list(self.instructions.keys())[29]:
            pass
        elif opcode == list(self.instructions.keys())[30]:
            pass
        elif opcode == list(self.instructions.keys())[31]:
            pass
        elif opcode == list(self.instructions.keys())[32]:
            pass
        elif opcode == list(self.instructions.keys())[33]:
            pass
        elif opcode == list(self.instructions.keys())[34]:
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




