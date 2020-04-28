import sys
import argparse
import os
import re
def diskUsage(d):
    firstLine = d.get("00")
    usedCount = 0
    freeCount = 0
    badCount = 0
    for thing in d:
        #print(d[thing][5:7])
        if d[thing][5:7] != "00":
            usedCount=usedCount+1
        else:
            freeCount=freeCount+1
        if(d[thing][0:1]) == "2":
            badCount = badCount+1
    print("STATE    COUNT   PERCENT")
    print("USED     "+str(usedCount)+"       "+str(usedCount/len(d)))
    print("AVAIL    "+str(freeCount)+"       "+str(freeCount/len(d)))
    print("BAD      "+str(badCount)+"       "+str(badCount/len(d)))
    print("Total Number of Clusters: " + str(len(d)))
    print("Total Number of Used: " + str(usedCount))
    if(freeCount == 0):
        print("***Disk Full***")
def readFolders(d,v=False):
    try:
        firstLine = d.get("00")
        nextLineIndex = firstLine[1:3]
        volumeIndex = firstLine[5:7]
        volumeName = firstLine[7:63]
        nextLineIndex = volumeIndex
        #print(firstLine[6:63])
        if(v):
            print("Volume:"+parseHex(volumeName))
            while nextLineIndex != "00":
                nextLine = d.get(nextLineIndex)
                nextLineIndex = nextLine[1:3]
                folderName = re.sub("00.*","",nextLine[5:63])

                print("     Folder:"+parseHex(folderName))
                
                #print(parseHex(folderName))
    except:
        "Something wrong with disk! Try again."
def readFile(d, name,v=False):
    #print(name)
    firstLine = d.get("00")
    nextLineIndex = firstLine[1:3]
    volumeIndex = firstLine[5:7]
    volumeName = firstLine[7:63]
    nextLineIndex = volumeIndex
    #print(firstLine[6:63])
    #print("Volume:"+parseHex(volumeName))
    if(v):
        found = False
        while nextLineIndex != "00":
            nextLine = d.get(nextLineIndex)
            nextLineIndex = nextLine[1:3]
            folderName = re.sub("00.*","",nextLine[5:63])
            fileName = re.sub("00.*","", nextLine[7+(len(folderName)):63])
            nextTrigger = nextLine[3:5]
            rowType = nextLine[0:1]
            #print('ree')

            if(name == parseHex(folderName)):
                print("     Folder:"+parseHex(folderName))
                print("         Contents:"+parseHex(fileName))   
                found = True
                while nextTrigger != "00":
                    nextLine = d.get(nextTrigger)
                    extraText = re.sub("00.*","",nextLine[3:63])
                    print("         "+parseHex(extraText))
                    nextTrigger = nextLine[1:3]
        if(not found):
            print("Error file named:" + name + " not found")
def parseHex(s):
    return bytearray.fromhex(s).decode()
def parseText(fileText):
    for line in preformattedArray:
        print(line)
def run():
    version = '0.2.1'
    parser = argparse.ArgumentParser(description='Reads a disk and returns it\'s text. For Finkbine\'s class.')
    parser.add_argument('-?', action='help')
    parser.add_argument('-v', action='version', version='Disk Reader is {0}'.format(version), help='Version for the program')
    parser.add_argument("--file", help='Path of disk to read')
    parser.add_argument("--type", help='Contents of folder')
    parser.add_argument("-du", action='store_true',help="Displays total usage of disk from txt file")
    if sys.stdin.isatty():
        if len(sys.argv)==1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    args = parser.parse_args()
    preformattedArray = []
    header1 = ""
    header2 = ""
    try:
        ourDict = {}
        if sys.stdin.isatty():
            #print("Using --file!")  
            args = parser.parse_args()
            try:
                f = open(args.file)
                header1 = f.readline().rstrip() #header
                header2 = f.readline().rstrip() #more useless
                for line in f:
                    preformattedArray.append(line.rstrip())
            except:
                #print("File not found! Location @ {0}".format(args.file))             
                print()
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
        if(args.file):
            readFolders(ourDict)
        if(args.type):
            readFile(ourDict, args.type, True)
        if(args.du):
            diskUsage(ourDict)
        print(ourDict.pop())
    except:
        "File broke! Try a different disk"

if __name__ == "__main__":
    run()
