import _pickle as pkl
import ast

MyFirstDict = { "hat": 7, "carpet": 5 }
MySecondDict = { "syrup":15, "yogurt": 18 }
test = {"1":1, "2":2}

MyDicts = [MyFirstDict, MySecondDict]

outputFile = open( "myDicts.txt", "w")
outputFile.write(str(MyDicts))
outputFile.flush()
outputFile.close()



inputFile = open( "myDicts.txt", "r")
lines = inputFile.readlines()

objects = []
for line in lines:
    objects.append( ast.literal_eval(line) )

myDicts = objects[0]

print(myDicts[0]['hat'])

myDicts[0] = test