import matplotlib.pyplot as mp
from funcs import *
from classes import *

options = Options()

calibPos,calibDFL = createPosDFLLists(options.calibFileName)
testPos,testDFL = createPosDFLLists(options.testFileName)

slopeSelect = window("Curve Selection",(640,480),calibPos,calibDFL)

slope = slopeSelect.slope
print("Calibration curve slope value:",slope)

forceList = []
averageForceList = []

for count,column in enumerate(testDFL):
    forceList.append(getForceList(testDFL[count],options.k,slope))

if options.modelName == "Hertz":
    deltaHertz = 200
    label = 0
    for count,column in enumerate(forceList):
        if count%2 != 0:
            label += 1
            print("Young's modulus of curve",label,":",getHertzE(forceList[count][deltaHertz],testPos[deltaHertz],options.radius))
    averageForceList = getHertzAverageF(forceList)
    print("Mean Young's modulus value:",getHertzE(averageForceList[deltaHertz],testPos[deltaHertz],options.radius)) 
elif options.modelName == "JKR":
    pass#getJKRmodelE(F)
