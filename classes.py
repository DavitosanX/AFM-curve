import tkinter as tk
import pygame as pg
from funcs import *

class Options:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Curve analysis")
        self.calibFileName = ""
        self.testFileName = ""
        self.modelName = ""
        self.calibText = tk.StringVar()
        self.testText = tk.StringVar()
        self.k = 0
        self.radius = 0

        self.folder = tk.PhotoImage(file=".\\Folder.png")
        self.calibLabel = tk.Label(self.root, text="Calibration file: ")
        self.calibLabel.grid(row=0,pady=5,padx=5)
        self.calibEntry = tk.Entry(self.root,state="disabled",textvariable=self.calibText)
        self.calibEntry.grid(column=1,row=0)
        self.chooseCalibButton = tk.Button(self.root, image=self.folder, command=self.getCalibFileName)
        self.chooseCalibButton.grid(row=0,column=2,padx=5,pady=5)
        self.testLabel = tk.Label(self.root, text="Test file:")
        self.testLabel.grid(row=1,pady=5,padx=5)
        self.testEntry = tk.Entry(self.root,state="disabled",textvariable=self.testText)
        self.testEntry.grid(column=1,row=1)
        self.chooseTestButton = tk.Button(self.root, image=self.folder, command=self.getTestFileName)
        self.chooseTestButton.grid(row=1,column=2,padx=5,pady=5)
        self.kLabel = tk.Label(self.root,text="Spring constant:")
        self.kLabel.grid(row=2,pady=5,padx=5)
        self.kEntry = tk.Entry(self.root,width=5)
        self.kEntry.grid(column=1,row=2)
        self.kUnitsLabel = tk.Label(self.root,text="N/m")
        self.kUnitsLabel.grid(column=2,row=2)
        self.radiusLabel = tk.Label(self.root,text="Tip radius:")
        self.radiusLabel.grid(row=3,pady=5,padx=5)
        self.radiusEntry = tk.Entry(self.root,width=5)
        self.radiusEntry.grid(column=1,row=3)
        self.radiusUnitsLabel = tk.Label(self.root,text="nm")
        self.radiusUnitsLabel.grid(column=2,row=3)
        self.modelLabel = tk.Label(self.root,text="Data analysis model")
        self.modelLabel.grid(row=4,pady=5,padx=5)
        self.modelList = tk.Listbox(self.root,height=2)
        self.modelList.grid(column=1,row=4)
        self.modelList.insert(0,"Hertz")
        self.modelList.insert(1,"JKR")
        self.goButton = tk.Button(self.root,text="Go!",command=self.getKRadiusModel)
        self.goButton.grid(column=1,row=5,pady=20)
        self.root.mainloop()

    def getCalibFileName(self):
        self.calibFileName = tk.filedialog.askopenfilename()
        self.calibText.set(self.calibFileName)

    def getTestFileName(self):
        self.testFileName = tk.filedialog.askopenfilename()
        self.testText.set(self.testFileName)

    def getKRadiusModel(self):
        self.k = int(self.kEntry.get())
        self.radius = int(self.radiusEntry.get())
        selected = self.modelList.curselection()[0]
        self.modelName = self.modelList.get(selected)
        self.root.destroy()

class line:

    def __init__(self,xpos,ypos,color):
        self.startPos = (xpos,0)
        self.endPos = (xpos,ypos)
        self.vicinity = {'x1':(xpos-5),'y1':0,'x2':(xpos+5),'y2':ypos}
        self.width = 1
        self.color = color

    def move(self,mousePosX,limit,color):
        if color == "blue" and mousePosX < limit:
            self.startPos = (mousePosX,0)
            self.endPos = (mousePosX,self.endPos[1])
            self.vicinity = {'x1':(mousePosX-5),'y1':0,'x2':(mousePosX+5),'y2':self.endPos[1]}
        elif color == "red" and mousePosX > limit:
            self.startPos = (mousePosX,0)
            self.endPos = (mousePosX,self.endPos[1])
            self.vicinity = {'x1':(mousePosX-5),'y1':0,'x2':(mousePosX+5),'y2':self.endPos[1]}

    def changeWidth(self,width):
        self.width = width

class regressionLine:

    def __init__(self,posSource,DFLSource,drawPos,drawDFL,start,end,height,ymax):
        try:
            startIndex = drawPos.index(start)
            endIndex = drawPos.index(end)
        except:
            startIndex = 0
            endIndex = 999
        self.ymax = ymax
        self.DFLList = DFLSource
        self.height = height
        self.x1 = posSource[startIndex]
        self.x2 = posSource[endIndex]
        self.drawX1 = drawPos[startIndex]
        self.drawX2 = drawPos[endIndex]
        self.narrowList = [posSource[startIndex:endIndex],DFLSource[startIndex:endIndex]]
        self.slope = 0
        self.intersect = 0
        self.rSquare = 0
        self.startDrawPos = (0,0)
        self.endDrawPos = (0,0)

    def minSquares(self):
        n = len(self.narrowList[0])
        x = self.narrowList[0]
        y = self.narrowList[1]
        avgX = getAverage(x)
        avgY = getAverage(y)
        xTimesY = []
        for count,pos in enumerate(self.narrowList[0]):
            xTimesY.append(pos*self.narrowList[1][count])
        xSquare = []
        for pos in self.narrowList[0]:
            xSquare.append(pos**2)
        self.slope = ((n*sum(xTimesY))-(sum(x)*sum(y)))/((n*sum(xSquare))-(sum(x)**2))
        self.intersect = avgY-(self.slope*avgX)
        SrTerms = []
        for count,pos in enumerate(x):
            SrTerms.append((y[count]-self.intersect-(self.slope*pos))**2)
        StTerms = []
        for DFL in y:
            StTerms.append((DFL-avgY)**2)
        self.rSquare = (sum(StTerms)-sum(SrTerms))/sum(StTerms)

    def getLinePos(self):
        y1 = (self.slope*self.x1)+self.intersect
        y2 = (self.slope*self.x2)+self.intersect
        drawY1 = ((y1-min(self.DFLList))*self.height)/max(self.DFLList)
        drawY2 = ((y2-min(self.DFLList))*self.height)/max(self.DFLList)
        self.startDrawPos = (self.drawX1,(self.ymax-drawY1))
        if (self.ymax-drawY2) < self.ymax:
            self.endDrawPos = (self.drawX2,(self.ymax-drawY2))
        else:
            self.endDrawPos = (self.drawX2,self.ymax)

class window:

    def __init__(self,caption,resolution,posList,DFLList):
        pg.init()
        self.screen = pg.display.set_mode(resolution)
        pg.display.set_caption(caption)
        self.running = True
        self.DFL = DFLList[0]
        self.pos = posList
        self.plotHeight = 300
        self.ymax = 350
        self.xmin = 100
        self.drawDFL = self.createDrawDFLList(self.DFL)
        self.drawPos = self.createDrawPosList(posList)
        self.blueLine = line(self.drawPos[0],self.ymax,(0,0,200))
        self.redLine = line(self.drawPos[999],self.ymax,(200,0,0))
        self.selectedLine = "none"
        self.limit = 0
        self.slope = 0
        self.choice = {'blue':self.blueLine.move,'red':self.redLine.move,'none':self.dummy}
        self.font = pg.font.SysFont("arialblack",16)
        self.instructions = self.font.render("Elija dos puntos en la grafica arrastrando las dos barras.",False,(0,0,0))
        self.eqText = self.font.render("",False,(0,0,0))
        self.r2Text = self.font.render("",False,(0,0,0))
        self.mainloop()
        pg.quit()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def createDrawPosList(self,posList):
        targetList = []
        pos = self.xmin
        for item in posList:
            targetList.append(pos/2)
            pos += 1
        return targetList

    def createDrawDFLList(self,DFLList):
        zeroValue = min(DFLList)
        maxValue = max(DFLList)
        targetList = []
        for item in DFLList:
            targetList.append(((item-zeroValue)*self.plotHeight)/maxValue)
        return targetList

    def dummy(self,a,b,c):
        pass

    def mouseInput(self):            
        if pg.mouse.get_pressed()[0]:
            self.choice[self.selectedLine](pg.mouse.get_pos()[0],self.limit,self.selectedLine)
            try:
                self.posText = self.font.render(str(self.pos[self.drawPos.index(pg.mouse.get_pos()[0])]),False,(0,0,0))
            except:
                self.posText = self.font.render("",False,(0,0,0))

    def mouseOver(self):
        if not pg.mouse.get_pressed()[0]:
            if pg.mouse.get_pos()[0] >= self.blueLine.vicinity['x1'] and pg.mouse.get_pos()[0] <= self.blueLine.vicinity['x2']:
                if pg.mouse.get_pos()[1] >= self.blueLine.vicinity['y1'] and pg.mouse.get_pos()[1] <= self.blueLine.vicinity['y2']:
                    self.selectedLine = "blue"
                    self.limit = self.redLine.startPos[0]-6
                    self.blueLine.width = 2
            elif pg.mouse.get_pos()[0] >= self.redLine.vicinity['x1'] and pg.mouse.get_pos()[0] <= self.redLine.vicinity['x2']:
                if pg.mouse.get_pos()[1] >= self.redLine.vicinity['y1'] and pg.mouse.get_pos()[1] <= self.redLine.vicinity['y2']:
                    self.selectedLine = "red"
                    self.limit = self.blueLine.startPos[0]+6
                    self.redLine.width = 2
            else:
                self.redLine.width = 1
                self.blueLine.width = 1
                self.selectedLine = "none"

    def mainloop(self):
        while self.running:
            self.screen.fill((200,200,200))
            for count,item in enumerate(self.drawDFL):
                posTuple = (self.drawPos[count],(self.ymax-item))
                pg.draw.line(self.screen,(0,0,200),posTuple,posTuple,1)
            pg.draw.line(self.screen,self.blueLine.color,self.blueLine.startPos,self.blueLine.endPos,self.blueLine.width)
            pg.draw.line(self.screen,self.redLine.color,self.redLine.startPos,self.redLine.endPos,self.redLine.width)
            self.screen.blit(self.instructions,(20,self.ymax+20))
            self.screen.blit(self.eqText,(20,self.ymax+40))
            self.screen.blit(self.r2Text,(20,self.ymax+60))
            self.regression = regressionLine(self.pos,self.DFL,self.drawPos,self.drawDFL,self.blueLine.startPos[0],self.redLine.endPos[0],self.plotHeight,self.ymax)
            self.regression.minSquares()
            self.slope = self.regression.slope
            eqString = "Ecuacion: "+str(self.regression.slope)[:7]+" x + "+str(self.regression.intersect)[:7]
            self.eqText = self.font.render(eqString,False,(0,0,0))
            r2String = "Coeficiente de determinacion (r^2): "+str(self.regression.rSquare)
            self.r2Text = self.font.render(r2String,False,(0,0,0))
            self.regression.getLinePos()
            pg.draw.line(self.screen,(0,0,0),self.regression.startDrawPos,self.regression.endDrawPos,1)
            pg.display.flip()
            self.checkEvents()
            self.mouseOver()
            self.mouseInput()
