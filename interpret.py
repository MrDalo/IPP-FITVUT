import sys
import xml.etree.ElementTree as ET
import re



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
            sys.exit(55)

        popedFrame = self.frames.pop()
        popedFrame.type = "TF"
        self.TF = popedFrame
        self.maxIndex = self.maxIndex - 1
    
    def createFrame(self):
        self.TF = frame("TF")

    def pushFrame(self, frame):
        if frame == None:
            print("Error - Unexisted TF frame", file = sys.stderr)
            sys.exit(55)

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
                sys.exit(55)

            try:
                return self.frames[self.maxIndex].items[varSplit[1]]
            except:
                return False
        elif frame == "TF":
            if self.TF == None:
                print("Error - Unexisted TF frame", file = sys.stderr)
                sys.exit(55)
            try:
                return self.TF.items[varSplit[1]]
            except:
                return False
        else:
            print("Internal ERROR", file = sys.stderr)
            sys.exit(99)

    def updateItem(self, item, newValue, newDataType):
        varSplit = item.split("@")
        frame = varSplit[0]
        variableName = varSplit[1]
        if frame == "TF":
            self.TF.items[variableName] = [newValue, newDataType]
        elif frame == "GF":
            self.frames[0].items[variableName] = [newValue, newDataType]
        else:
            self.frames[self.maxIndex].items[variableName] = [newValue, newDataType]



    def appendItem(self,item):
        varSplit = item.split("@")
        if not self.findItem(item):
            if varSplit[0] == "GF":
                self.frames[0].items[varSplit[1]] = ["", None]                
                self.frames[0].len+=1   
            elif varSplit[0] == "LF":
                self.frames[self.maxIndex].items[varSplit[1]] = ["", None]                
                self.frames[self.maxIndex].len+=1               
            else:
                self.TF.items[varSplit[1]] = ["", None]                
                self.TF.len += 1    
        
        else:
            print("Error - Redefinition of variable", file = sys.stderr)
            sys.exit(52)



class interpreter:
    
    def __init__(self, arrayOfLabels, inputFile):
        self.symtable = symtableClass()
        self.arrayOfLabels = arrayOfLabels
        self.stack = []
        self.numberOfInstructions = 0
        self.inputFile = inputFile
        if self.inputFile != None:
            try:
                self.inputFile = open(self.inputFile, "r")
            except:
                print("Error - invalid file name or unable to open inputfile for reading", file = sys.stderr)
                sys.exit(11)

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
    
    def isType(self, arg):
        if arg.attrib.get('type') == "type":
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

    def isVarNone(self, value):
        if value == None:
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
                sys.exit(54)
            else:
                symbDataType = symtableItem[1]
                symbValue = symtableItem[0]

        elif self.isConstant(instruction.find(argNumber)):
            symbIsVar = False
            symbValue = instruction.find(argNumber).text
            symbDataType = instruction.find(argNumber).attrib.get('type')

        else:
            print("Error - bad operand type", file = sys.stderr)
            sys.exit(53)
        return symbIsVar, symbValue, symbDataType

    def stringConversion(self, value):
        
        try:
            value = re.sub('&lt;', '<', value)
            value = re.sub('&gt;', '>', value)
            value = re.sub('&amp;', '&', value)
            value = re.sub('&quot;', '"', value)
            value = re.sub('&apos;', '\'', value)

            while re.search('\\\\\d{3}',value):
                value = re.sub('\\\\\d{3}',chr(int(re.search('\\\\\d{3}',value)[0][1:])),value, count= 1 )
        except:
            return value
        return value


    def instructionOpeartions(self, opcode,instruction, i):
        self.numberOfInstructions += 1
        
        if opcode == list(self.instructions.keys())[0]: #MOVE

            if self.isVariable(instruction.find('arg1')):

                var = instruction.find('arg1').text
                symtableItem = self.symtable.findItem(var)

                if not symtableItem:
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
                else:
                    varDataType = symtableItem[1]

            else:
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)

            symbIsVar = False
            if self.isVariable(instruction.find('arg2')):
                symbIsVar = True
                symb = instruction.find('arg2').text
                symtableItem = self.symtable.findItem(symb)

                if not symtableItem:
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
                else:
                    symbDataType = symtableItem[1]
                    symbValue = symtableItem[0]

            elif self.isConstant(instruction.find('arg2')):
                symbIsVar = False
                symb = instruction.find('arg2').text
                symbDataType = instruction.find('arg2').attrib.get('type')

            else:
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            
            if symb == None:
                symb = ""
            if symbIsVar:
                if self.isVarNone(symbDataType):
                    print("Error - None in variable, empty variable", file = sys.stderr)
                    sys.exit(56)
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
                sys.exit(53)


        elif opcode == list(self.instructions.keys())[5]:#CALL
            self.stack.append([i, 'int'])
            if self.isLabel(instruction.find('arg1')):
                try:
                    print(f'Before after: {i}')
                    i = int(self.arrayOfLabels[instruction.find('arg1').text])
                except:
                    print("Error - Undefined LABEL call", file = sys.stderr)
                    sys.exit(52)

            else:
                print("Error - Call without valid LABEL", file = sys.stderr)
                sys.exit(53)

            print(f'Call after: {i}')

        elif opcode == list(self.instructions.keys())[6]:#RETURN
            if len(self.stack) > 0:
                poppedValue = self.stack.pop()
                if poppedValue[1] != 'int':
                    print("Error - NOT int value in poppedValue", file = sys.stderr)
                    sys.exit(57)
                try:
                    i = int(poppedValue[0])
                except:
                    print("Error - Bad XML structure INT conversion", file = sys.stderr)
                    sys.exit(32)

                #Check bolo tu: i = poppedValue[0]
            else:
                print("Error - Empty stack", file = sys.stderr)
                sys.exit(56)
            
            print(f'RETURN: {i}')




        elif opcode == list(self.instructions.keys())[7]:#PUSHS
            symbIsVar, symbValue, symbDataType = self.isSymb(instruction, 'arg1')
            if symbValue == None:
                symbValue = ""

            if self.isVarNone(symbDataType):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)
            
            self.stack.append([symbValue, symbDataType])



        elif opcode == list(self.instructions.keys())[8]:#POPS
            if len(self.stack) > 0:
                if self.isVariable(instruction.find('arg1')):
                    if not self.symtable.findItem(instruction.find('arg1').text):
                        print("Error - Unexisted variable", file = sys.stderr)
                        sys.exit(54)
                    poppedValue = self.stack.pop()
                    self.symtable.updateItem(instruction.find('arg1').text, poppedValue[0], poppedValue[1])
                else:
                    print("Error - bad operand type", file = sys.stderr)
                    sys.exit(53)

            else:
                print("Error - Empty stack", file = sys.stderr)
                sys.exit(56)



        elif opcode == list(self.instructions.keys())[9]:#ADD
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            
            

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            
            try:
                result = int(symbValue1) + int(symbValue2)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            
            self.symtable.updateItem(instruction.find('arg1').text, str(result), 'int')



        elif opcode == list(self.instructions.keys())[10]:#SUB
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)

            try:
                result = int(symbValue1) - int(symbValue2)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            self.symtable.updateItem(instruction.find('arg1').text, str(result), 'int')




        elif opcode == list(self.instructions.keys())[11]:#MUL
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)

            try:
                result = int(symbValue1) * int(symbValue2)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            
            self.symtable.updateItem(instruction.find('arg1').text, str(result), 'int')




        elif opcode == list(self.instructions.keys())[12]:#IDIV
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'int' or symbDataType2 != 'int':
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            if symbValue2 == '0':
                print("Error - Dividing by 0", file = sys.stderr)
                sys.exit(57)
            

            try:
                result = int(symbValue1) // int(symbValue2)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            self.symtable.updateItem(instruction.find('arg1').text, str(result), 'int')




        elif opcode == list(self.instructions.keys())[13]:#LT
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue1 == None:
                symbValue1 = ""
            if symbValue2 == None:
                symbValue2 = ""

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != symbDataType2 or symbDataType1 == 'nil' or symbDataType2 == 'nil':
                print("Error - 1Not same operands types", file = sys.stderr)
                sys.exit(53)

            if symbDataType1 == 'string' and symbDataType2 == 'string':
                symbValue1 = self.stringConversion(symbValue1)
                symbValue2 = self.stringConversion(symbValue2)

            if symbDataType1 == 'int':
                if int(symbValue1) < int(symbValue2):
                    self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
                else:
                    self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')
            else:
                if symbValue1 < symbValue2:
                    self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
                else:
                    self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')



        elif opcode == list(self.instructions.keys())[14]:#GT
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue1 == None:
                symbValue1 = ""
            if symbValue2 == None:
                symbValue2 = ""

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != symbDataType2 or symbDataType1 == 'nil' or symbDataType2 == 'nil':
                print("Error - 2Not same operands types", file = sys.stderr)
                sys.exit(53)

            if symbDataType1 == 'string' and symbDataType2 == 'string':
                symbValue1 = self.stringConversion(symbValue1)
                symbValue2 = self.stringConversion(symbValue2)

            if symbDataType1 == 'int':
                if int(symbValue1) > int(symbValue2):
                    self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
                else:
                    self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')
            else:
                if symbValue1 > symbValue2:
                    self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
                else:
                    self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')



        elif opcode == list(self.instructions.keys())[15]:#EQ
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue1 == None:
                symbValue1 = ""
            if symbValue2 == None:
                symbValue2 = ""

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != symbDataType2 and symbDataType1 != 'nil' and symbDataType2 != 'nil':
                print("Error - Not same operands types", file = sys.stderr)
                sys.exit(53)

            if symbDataType1 == 'string' and symbDataType2 == 'string':
                symbValue1 = self.stringConversion(symbValue1)
                symbValue2 = self.stringConversion(symbValue2)

            if symbDataType1 == 'int' and symbDataType1 != 'nil' and symbDataType2 != 'nil':
                if int(symbValue1) == int(symbValue2):
                    self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
                else:
                    self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')
            else:
                if symbValue1 == symbValue2:
                    self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
                else:
                    self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')



        elif opcode == list(self.instructions.keys())[16]:#AND
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue1 == None:
                symbValue1 = ""
            if symbValue2 == None:
                symbValue2 = ""

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'bool'  or symbDataType2 != 'bool':
                print("Error - Not bool operands types", file = sys.stderr)
                sys.exit(53)

            if symbValue1 == 'true' and symbValue2 == 'true':
                self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
            else:
                self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')



        elif opcode == list(self.instructions.keys())[17]:#OR
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue1 == None:
                symbValue1 = ""
            if symbValue2 == None:
                symbValue2 = ""

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'bool'  or symbDataType2 != 'bool':
                print("Error - Not bool operands types", file = sys.stderr)
                sys.exit(53)

            if symbValue1 == 'true' or symbValue2 == 'true':
                self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')
            else:
                self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')



        elif opcode == list(self.instructions.keys())[18]:#NOT
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            

            if self.isVarNone(symbDataType1):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'bool':
                print("Error - Not bool operands types", file = sys.stderr)
                sys.exit(53)

            if symbValue1 == 'true':
                self.symtable.updateItem(instruction.find('arg1').text, 'false', 'bool')
            else:
                self.symtable.updateItem(instruction.find('arg1').text, 'true', 'bool')



        elif opcode == list(self.instructions.keys())[19]:#INT2CHAR
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')


            if self.isVarNone(symbDataType1):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'int':
                print("Error - Not bool operands types", file = sys.stderr)
                sys.exit(53)

            try:
                character = chr(int(symbValue1))
            except:
                print("Error - Invalid number in int2cahr conversion", file = sys.stderr)
                sys.exit(58)

            self.symtable.updateItem(instruction.find('arg1').text, character, 'string')

        elif opcode == list(self.instructions.keys())[20]:#STRI2INT
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue2 == None:
                symbValue2 = ""

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'string' or symbDataType2 != 'int':
                print("Error - 4Not same operands types", file = sys.stderr)
                sys.exit(53)
            
            try:
                symbValue2 = int(symbValue2)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            
            symbValue1 = self.stringConversion(symbValue1)
            
            if symbValue2 > len(symbValue1) - 1 or symbValue2 < 0:
                print("Error - Bad indexing", file = sys.stderr)
                sys.exit(58)

            self.symtable.updateItem(instruction.find('arg1').text, str(ord(symbValue1[symbValue2])), 'int')


        elif opcode == list(self.instructions.keys())[21]:#READ
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)

            typeValue =  instruction.find('arg2').text
            if not self.isType(instruction.find('arg2')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)

            
            if self.inputFile == None:
                value = input()
            else:
                value = self.inputFile.readline().replace('\n', "")

            if typeValue == "int":
                try:
                    value = int(value)
                except:
                    value = 'nil'
                    typeValue = 'nil'
            elif typeValue == 'bool':
                if value.lower() == 'true':
                    value = 'true'
                else:
                    value = 'false'
            elif typeValue == 'string' and value != None:
                value = self.stringConversion(value)
            
            if value == None:
                value = ""
                typeValue = "nil"

            self.symtable.updateItem(instruction.find('arg1').text, value, typeValue)



        elif opcode == list(self.instructions.keys())[22]:#WRITE
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg1')
            if symbValue1 == None:
                symbValue1 = ""
            
            if self.isVarNone(symbDataType1):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)
            if symbDataType1 == 'string':
                symbValue1 = self.stringConversion(symbValue1)

            if symbDataType1 != "nil":
                print(symbValue1,end='')



        elif opcode == list(self.instructions.keys())[23]:#CONCAT
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue2 == None:
                symbValue2 = ""

            if  symbDataType1 == None or symbDataType2 == None:
                sys.exit(56)

            if symbDataType1 != 'string'  or symbDataType2 != 'string':
                print("Error - Not string operands types", file = sys.stderr)
                sys.exit(53)
            
            self.symtable.updateItem(instruction.find('arg1').text, symbValue1+symbValue2, 'string')


        elif opcode == list(self.instructions.keys())[24]:#STRLEN
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbValue1 = self.stringConversion(symbValue1)

            if self.isVarNone(symbDataType1):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)
            
            if symbDataType1 != 'string':
                print("Error - Not string operands types", file = sys.stderr)
                sys.exit(53)

            self.symtable.updateItem(instruction.find('arg1').text, str(len(symbValue1)), 'int')
            
        elif opcode == list(self.instructions.keys())[25]:#GETCHAR
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue2 == None:
                symbValue2 = ""

            if  symbDataType1 == None or symbDataType2 == None:
                sys.exit(56)

            if symbDataType1 != 'string'  or symbDataType2 != 'int':
                print("Error - Not string or integer operands types", file = sys.stderr)
                sys.exit(53)

            try:
                symbValue2 = int(symbValue2)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            symbValue1 = self.stringConversion(symbValue1)

            if symbValue2 > len(symbValue1) - 1 or symbValue2 < 0:
                print("Error - Bad indexing", file = sys.stderr)
                sys.exit(58)

            self.symtable.updateItem(instruction.find('arg1').text, symbValue1[symbValue2], 'string')



        elif opcode == list(self.instructions.keys())[26]:#SETCHAR
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
                else:
                    newVariable = self.symtable.findItem(instruction.find('arg1').text)
                    varDataType = newVariable[1]
                    if not newVariable[1] == "string" and not newVariable[1] == None:
                        print("Error - bad operand type", file = sys.stderr)
                        sys.exit(53)
                    if self.isVarNone(newVariable[1]):
                        print("Error - None in variable", file = sys.stderr)
                        sys.exit(56)
                    newVariable = newVariable[0]

            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue2 == None:
                print("Error - empty string", file = sys.stderr)
                sys.exit(58)

            if self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2) or self.isVarNone(varDataType):
                print("Error - None in variable, empty variable", file = sys.stderr)
                sys.exit(56)

            if symbDataType1 != 'int'  or symbDataType2 != 'string':
                print("Error - Not string or integer operands types", file = sys.stderr)
                sys.exit(53)

            try:
                symbValue1 = int(symbValue1)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(32)
            symbValue2 = self.stringConversion(symbValue2)
            newVariable = self.stringConversion(newVariable)

            if symbValue1 > len(newVariable) - 1 or symbValue1 < 0:
                print("Error - Bad indexing", file = sys.stderr)
                sys.exit(58)

            newVariable=newVariable[:symbValue1] +symbValue2[0]+ newVariable[symbValue1+1:]
            
            self.symtable.updateItem(instruction.find('arg1').text, newVariable, 'string')


        elif opcode == list(self.instructions.keys())[27]:#TYPE
            if not self.isVariable(instruction.find('arg1')):
                print("Error - bad operand type", file = sys.stderr)
                sys.exit(53)
            else:
                if not self.symtable.findItem(instruction.find('arg1').text):
                    print("Error - Unexisted variable", file = sys.stderr)
                    sys.exit(54)
            
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            if symbDataType1 == None:
                self.symtable.updateItem(instruction.find('arg1').text, '', 'string')
            else:    
                self.symtable.updateItem(instruction.find('arg1').text, symbDataType1, 'string')


        elif opcode == list(self.instructions.keys())[28]:#LABEL
            pass


        elif opcode == list(self.instructions.keys())[29]:#JUMP
            
            if self.isLabel(instruction.find('arg1')):
                try:
                    i = int(self.arrayOfLabels[instruction.find('arg1').text])
                    
                except:
                    print("Error - Undefined LABEL call", file = sys.stderr)
                    sys.exit(52)

            else:
                print("Error - Call without valid LABEL", file = sys.stderr)
                sys.exit(53)
        
        
        elif opcode == list(self.instructions.keys())[30]:#JUMPIFEQ
            if not self.isLabel(instruction.find('arg1')):
                print("Error - Call without valid LABEL", file = sys.stderr)
                sys.exit(53)
            
            try:
                newPosition = int(self.arrayOfLabels[instruction.find('arg1').text])
            except:
                print("Error - Undefined LABEL call", file = sys.stderr)
                sys.exit(52)

            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue2 == None:
                symbValue2 = ""
            
            if symbDataType1 == 'string' and symbDataType2 == 'string':
                symbValue1 = self.stringConversion(symbValue1)
                symbValue2 = self.stringConversion(symbValue2)
            
            if  symbDataType1 == None or symbDataType2 == None:
                sys.exit(56)
                
            if (symbDataType1 != symbDataType2 and symbDataType1 != 'nil' and symbDataType2 != 'nil'):
                print("Error - 5Not same type or nil operands type", file = sys.stderr)
                sys.exit(53)
            

            if symbValue1 == symbValue2:
                i = newPosition
            
            

        elif opcode == list(self.instructions.keys())[31]:#JUMPIFNEQ
            if not self.isLabel(instruction.find('arg1')):
                print("Error - Call without valid LABEL", file = sys.stderr)
                sys.exit(53)
            
            try:
                newPosition = int(self.arrayOfLabels[instruction.find('arg1').text])
            except:
                print("Error - Undefined LABEL call", file = sys.stderr)
                sys.exit(52)

            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg2')
            if symbValue1 == None:
                symbValue1 = ""
            symbIsVar2, symbValue2, symbDataType2 = self.isSymb(instruction, 'arg3')
            if symbValue2 == None:
                symbValue2 = ""

            if symbDataType1 == 'string' and symbDataType2 == 'string':
                symbValue1 = self.stringConversion(symbValue1)
                symbValue2 = self.stringConversion(symbValue2)

            if  self.isVarNone(symbDataType1) or self.isVarNone(symbDataType2):
                sys.exit(56)

            if (symbDataType1 != symbDataType2 and symbDataType1 != 'nil' and symbDataType2 != 'nil'):
                print("Error - 6Not same type or nil operands type", file = sys.stderr)
                sys.exit(53)
            
            print(f'prva: {symbValue1}, druha: {symbValue2}')
            if symbValue1 != symbValue2:
                print(f'INSIDE, {newPosition}, {i}')
                i = newPosition
        
        elif opcode == list(self.instructions.keys())[32]:#EXIT
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg1')
            if symbValue1 == "":
                sys.exit(56)
    

            try:    
                symbValue1 = int(symbValue1)
            except:
                print("Error - Bad XML structure INT conversion", file = sys.stderr)
                sys.exit(53)
            if symbValue1 < 0 or symbValue1 > 49:
                print("Error - Bad EXIT value", file = sys.stderr)
                sys.exit(57)
            else:
                sys.exit(symbValue1)


        elif opcode == list(self.instructions.keys())[33]:#DPRINT
            symbIsVar1, symbValue1, symbDataType1 = self.isSymb(instruction, 'arg1')
            if symbValue1 == None:
                symbValue1 = ""
            print(symbValue1, file = sys.stderr)
        elif opcode == list(self.instructions.keys())[34]:#BREAK
            print(f'Position in code: {i}, content of frame: {self.stack}, number of executed instructions: {self.numberOfInstructions}', file = sys.stderr)
        else:
            print("Error - Bad Operation code", file = sys.stderr)
            sys.exit(22)

        return i


class xmlReader:

    instructionOrder = 0

    def __init__(self, sourceFile):
        if(sourceFile != None):
            try:
                tree = ET.parse(sourceFile)

            except: 
                print("Error - invalid file name or unable to open file for reading", file = sys.stderr)
                sys.exit(11)

            try:
                self.root = tree.getroot()
            except:
                print("Error - invalid format of xml", file = sys.stderr)
                sys.exit(31)

        else:
            tree = input()
            try:
                self.root = ET.fromstring(tree)
            except:
                print("Error - invalid format of xml", file = sys.stderr)
                sys.exit(31)




    def orderChecker(self, externalOrder):
        if externalOrder == None:
            print("Error - missing instruction order", file = sys.stderr)
            sys.exit(32)

        if int(self.instructionOrder) < int(externalOrder):
            self.instructionOrder = externalOrder
            return True
        else:
            print("Error - invalide instruction order", file = sys.stderr)
            sys.exit(32)

    def getOpcode(self, instruction):
        return instruction.attrib.get('opcode')

    def isXMLCorrect(self):
        if self.root.findall('arg1') or self.root.findall('arg2') or self.root.findall('arg3') :
            print("Error - invalid XML", file = sys.stderr)
            sys.exit(32)

        if self.root.tag != "program" or self.root.attrib.get('language') != "IPPcode22":
            print("Error - invalid XML program attribute", file = sys.stderr)
            sys.exit(31)

        # TODO check xml version and encoding


    

def arguments():    
    isHelp = False
    source= None
    input = None
    isProgram = False

    if len(sys.argv) > 3 :
        print("Error in arguments", file = sys.stderr)
        sys.exit(10)
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
                sys.exit(10)
        isProgram = True

    if isHelp and (source != None or input != None):
        print("Error in arguments", file = sys.stderr)
        sys.exit(10)
    
    if isHelp:
        print("IPP interpret.py by Dalibor Kralik")
        print("")
        print("Optional arguments:")
        print("     --help              write help of the program")
        print("     --source  SOURCE    source file of the program")
        print("     --input   INPUT     input file of the program")
        sys.exit(0)
    
    if source == None and input == None:
        print("Error in arguments", file = sys.stderr)
        sys.exit(10)

    return source, input
    


def sortingCriteria(instruction):
    return int(instruction.attrib.get('order'))



def programmeRunner(sourceFile, inputFile):
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
    
    counterIndex = 0
    for instruction in listOfInstructions:
        reader.orderChecker(instruction.attrib.get('order'))

            # check redefinition of LABEL
        if((instruction.attrib.get('opcode').upper()) == "LABEL"):
            if instruction.find('arg1').text in arrayOfLabels:
                    print("Error - redefinition of LABEL", file = sys.stderr)
                    exit(52)
            else:
                arrayOfLabels[instruction.find('arg1').text] = counterIndex 
        
        counterIndex = counterIndex + 1

      
    # TODO ak budem kontrolovat existenciu LABELu, pouzi pole arrayOfLabels cez try-except a hlada kluc
    

    interpret = interpreter(arrayOfLabels, inputFile)
    iteration = 0
    while iteration < len(listOfInstructions):

        iteration = interpret.instructionOpeartions(listOfInstructions[iteration].attrib.get('opcode').upper(),listOfInstructions[iteration], iteration)
        iteration += 1



if __name__ == '__main__':
    sourceFile, inputFile = arguments()
    programmeRunner(sourceFile, inputFile)




