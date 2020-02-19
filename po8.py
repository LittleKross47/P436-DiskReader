import sys
import argparse
import os
import re
version = '0.1.0'
parser = argparse.ArgumentParser(description='Reads a disk and returns it\'s text. For Finkbine\'s class.')
parser.add_argument('-?', action='help')
parser.add_argument('-v', action='version', version='Disk Reader is {0}'.format(version), help='Version for the program')
parser.add_argument("--file", help='Path of disk to read')
if sys.stdin.isatty():
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
args = parser.parse_args()
preformattedArray = []
header1 = ""
header2 = ""
def readFolders(d):
    try:
        firstLine = d.get("00")
        nextLineIndex = firstLine[1:3]
        volumeIndex = firstLine[5:7]
        volumeName = firstLine[7:63]
        nextLineIndex = volumeIndex
        #print(firstLine[6:63])
        print("Volume:"+parseHex(volumeName))
        while nextLineIndex != "00":
            nextLine = d.get(nextLineIndex)
            nextLineIndex = nextLine[1:3]
            folderName = re.sub("00.*","",nextLine[5:63])
            print("     Folder:"+parseHex(folderName))
            #print(parseHex(folderName))
    except:
        "Something wrong with disk! Try again."
def parseHex(s):
    return bytearray.fromhex(s).decode()
def parseText(fileText):
    for line in preformattedArray:
        print(line)
def run():
    try:
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
        print(ourDict.pop())
    except:
        "File broke! Try a different disk"



if __name__ == "__main__":
    run()
    





