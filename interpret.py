import argparse
from pickle import NONE
import sys
import xml.etree.ElementTree as ET



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

class symtable:
    LF = None
    
    def __init__(self):
        self.items = []
        self.items.append(frame("0"))
        self.maxIndex = 0
    
    
    def appendItem(self, itemKey, itemValue, itemDataType):
        self.items[self.maxIndex].items[itemKey] = [itemValue,itemDataType]

    def popFrame(self):
        popedFrame = self.items.pop()
        popedFrame.type = 2
        return popedFrame

    def pushFrame(self, frame):
        frame.type = 1
        self.items.append(frame)

    def findItem(self, item, frame):
        if frame == 0:
            try:
                return self.items[0].items[item]
            except:
                return False
        elif frame == 1:
            try:
                return self.items[self.maxIndex].items[item]
            except:
                return False
        elif frame == 2:
                try:
                    return self.LF.items[item]
                except:
                    return False
        else:
            print("Internal ERROR", file = sys.stderr)
            exit(99)



class interpreter:
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

    def __init__(self):
        pass

    def instructionOpeartions(self, opcode):
        #print(self.instructions.keys())
        if opcode == list(self.instructions.keys())[0]:
            pass
        elif opcode == list(self.instructions.keys())[1]:
            pass
        elif opcode == list(self.instructions.keys())[2]:
            pass
        elif opcode == list(self.instructions.keys())[3]:
            pass
        elif opcode == list(self.instructions.keys())[4]:
            pass
        elif opcode == list(self.instructions.keys())[5]:
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
    interpret = interpreter()
    listOfInstructions=[]

    
        # Checking correct XML structure
    reader.isXMLCorrect()



        # Creating listOfInstrucitons
    for instruction in reader.root.iter('instruction'):
        listOfInstructions.append(instruction)
    
        # Sorting of instructions and check order
    listOfInstructions.sort(key=sortingCriteria)

    arrayOfLabels=[]
    for instruction in listOfInstructions:
        reader.orderChecker(instruction.attrib.get('order'))
            # check redefinition of LABEL
        if((instruction.attrib.get('opcode').upper()) == "LABEL"):
            if instruction.find('arg1').text in arrayOfLabels:
                print("Error - redefinition of LABEL", file = sys.stderr)
                exit(52)
                # append LABEL to the arrayOFLabels
            arrayOfLabels.append(instruction.find('arg1').text)

    print(arrayOfLabels)        
    # TODO  Prechadzanie instrukcii


if __name__ == '__main__':
    sourceFile, inputFile = arguments()
    print(sourceFile, inputFile)
    programmeRunner(sourceFile)




