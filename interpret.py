import argparse
from pickle import NONE
import sys
import xml.etree.ElementTree as ET


class symtable:
    
    def __init__(self):
        pass


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


    
        



def arguments():
    parser = argparse.ArgumentParser(add_help=False, description="IPP interpret.py by Dalibor Kralik")
        # TODO poriesit kombinciu --help a dalsich argumentov
    parser.add_argument('--help', action='help', help='source file of program')
    parser.add_argument('--source', help='source file of program')
    parser.add_argument('--input', help='input file of program')
    args = parser.parse_args()
    

    source = args.source
    input = args.input
    if (source == None and input==None):
        print("Error in arguments", file = sys.stderr)
        exit(10)


    return source, input


def sortingCrit(instruction):
    return instruction.attrib.get('order')


def programmeRunner(sourceFile):
    reader = xmlReader(sourceFile)
    interpret = interpreter()
    listOfInstructions=[]

    
        # Checking correct XML structure
    reader.isXMLCorrect()

        # Creating listOfInstrucitons
        # TODO osetrit chyba 31
    for instruction in reader.root.iter('instruction'):
        listOfInstructions.append(instruction)
    
        # Sorting of instructions and check order
    listOfInstructions.sort(key=sortingCrit)
    for instruction in listOfInstructions:
        reader.orderChecker(instruction.attrib.get('order'))
            
        


if __name__ == '__main__':
    sourceFile, inputFile = arguments()
    print(sourceFile, inputFile)
    programmeRunner(sourceFile)




