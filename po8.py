import sys
import argparse
import os
version = '0.0.1'
parser = argparse.ArgumentParser(description='Reads a disk and returns it\'s text. For Finkbine\'s class.')
parser.add_argument('-v', action='version', version='Disk Reader is {0}'.format(version), help='Version for the program')
parser.add_argument("--file", help='Path of disk to read')
args = parser.parse_args()
preformattedArray = []
def parseText(fileText):
    for line in preformattedArray:
        print(line)
ourDict = {}
if sys.stdin.isatty():
    print("Using --file!")  
    args = parser.parse_args()
    try:
        f = open(args.file)
        header1 = f.readline().rstrip() #header
        header2 = f.readline().rstrip() #more useless
        for line in f:
            preformattedArray.append(line.rstrip())
    except:
       print("File not found! Location @ {0}".format(args.file))             
else:
    firstLine = True
    secondLine = False
    for line in sys.stdin:
        if(secondLine):
            header2 = line.rstrip()
            secondLine = False
        if(firstLine):
            header1 = line.rstrip()
            firstLine = False
            secondLine = True
        else:
            preformattedArray.append(line.rstrip())
    
for thing in preformattedArray:
    x = thing.split(":")
    if(x[0] != ""):
        ourDict[x[0]] = x[1]
print(header1)
print(header2)
for thing in ourDict:
    print(ourDict[thing])







