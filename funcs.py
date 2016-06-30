def getAverage(values):
    valuesSum = 0
    for item in values:
        valuesSum += item
    return valuesSum/len(values)

def getZeroLine(curva):
    zeroLinePoints = 100
    pointCount = len(curva)
    averagePointList = list(curva[pointCount-zeroLinePoints:])
    return getAverage(averagePointList)

def createPosDFLLists(filePath):

    sourceFile = open(filePath)
    fileLines = sourceFile.readlines()
    positions, deflectionValues = [],[]

    for count,item in enumerate(fileLines):
        if item[:2] == 'X\t':
            headerLine = count
            break

    curveCount = int(fileLines[headerLine].count('\t'))

    for count,line in enumerate(fileLines[headerLine+1:]):
        index = line.find('\t')
        positions.append(float(line[:index]))
        fileLines[headerLine+1+count] = line[index+1:]

    dataLines = fileLines[headerLine+1:]

    for i in range(curveCount):
        DFLList = []
        for count,line in enumerate(dataLines):
            index = line.find('\t')
            DFLList.append(float(line[:index]))
            dataLines[count] = line[index+1:]
        deflectionValues.append(DFLList)    

    return positions,deflectionValues

def getSlope(posList,DFLList):
    m = [0]

    for index,item in enumerate(DFLList[0]):
        if (index+1) < len(DFLList[0]):
            # m = y2-y1/x2-x1
            m.append(((DFLList[0][index+1]-item)/(posList[index+1]-posList[index])))

    slopePoints = []

    for index,item in enumerate(m):
        #Si la pendiente es negativa, y la DFL > 0, para tomar la recta mas precisa
        if item < 0 and item > -0.5 and DFLList[0][index] > 0:
            slopePoints.append(item)

    return getAverage(slopePoints)

def getForceList(DFLList,springK,slope):
    F = []

    for item in DFLList:
        F.append(springK*(item/abs(slope)))

    return F

def getJKRmodelK(ForceList,posList,zeroF,radius):

    lowestF = min(ForceList)
    lowestFPos = posList[ForceList.index(lowestF)]
    increasingFValues = []

    for index,item in enumerate(ForceList):
        if posList[index] < 0 and item < zeroF:
            increasingFValues.append(item)

    zeroF = max(increasingFValues)
    zeroFValuePos = posList[ForceList.index(zeroF)]

    #K = -((1+(16**(1/3)))/3)**(3/2) * F1/sqrt(R(d0-d1)

    constValue = ((1+(16**(1/3)))/3)**(3/2)
    return (constValue*(lowestF/(radius*(((zeroFValuePos*(-1))-(lowestFPos*(-1)))**3))**(1/2)))*(-1)

def getHertzAverageF(forceList):
    averageForce = []
    for outerCount,i in enumerate(range(len(forceList[0]))):
        values = []
        for innerCount,column in enumerate(forceList):
            if innerCount%2 != 0:
                values.append(column[outerCount])
        averageForce.append(getAverage(values))
    return averageForce

def getHertzE(force,pos,radius):
    return (3*force*0.75)/(4*(radius**(1/2))*(abs(pos)**(3/2)))
