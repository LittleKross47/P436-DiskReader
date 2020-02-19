import sys
import argparse
import os
import re
version = '0.1.0'
parser = argparse.ArgumentParser(description='Reads a disk and returns it\'s text. For Finkbine\'s class.')
parser.add_argument('-v', action='version', version='Disk Reader is {0}'.format(version), help='Version for the program')
parser.add_argument("--file", help='Path of disk to read')
args = parser.parse_args()
preformattedArray = []
header1 = ""
header2 = ""
def parseHex(s):
    return bytearray.fromhex(s).decode()
def parseText(fileText):
    for line in preformattedArray:
        print(line)
def run():
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
    #print(header1)
    #print(header2)
    readFolders(ourDict)

def readFolders(d):
    firstLine = d.get("00")
    nextLineIndex = firstLine[1:3]
    volumeIndex = firstLine[5:7]
    volumeName = firstLine[7:63]
    while nextLineIndex != "00":
        nextLine = d.get(nextLineIndex)
        nextLineIndex = nextLine[1:3]
        #print(nextLine)
    nextLineIndex = volumeIndex
    #print(firstLine[6:63])
    while nextLineIndex != "00":
        nextLine = d.get(nextLineIndex)
        nextLineIndex = nextLine[1:3]
        print(parseHex(nextLine[3:63]))

if __name__ == "__main__":
    run()
    





