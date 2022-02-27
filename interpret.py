import argparse
#from pickle import NONE
import sys
import xml.etree.ElementTree as ET

from cv2 import insertChannel



class xmlReader:

    instrucionOrder = 1

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
        if self.instrucionOrder == externalOrder:
            ++self.instrucionOrder
            return True
        else:
            print("Error - invalide instruction order", file = sys.stderr)
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


def programmeRunner(sourceFile):
    reader = xmlReader(sourceFile)
    
    for instruction in reader.root.iter('instruction'):
        reader.orderChecker(instruction.attrib.get('order'))
            
        


if __name__ == '__main__':
    sourceFile, inputFile = arguments()
    print(sourceFile, inputFile)
    programmeRunner(sourceFile)




