
from Checkbox import *



class KeyGenerationCheckbox(Checkbox):
    def __init__(self,page):
        Checkbox.__init__(self,page)
        self.ALGORITHMS_PATH = '/home/naimul/NaimulRepo/YubiHSM2Tool/textfiles/algorithms.txt'
        self.algorithmsDictionary = {}
        self.convertAlgorithmsToDictionary()

    def convertAlgorithmsToDictionary(self):
        self.listOfAlgorithms = getChecboxNames(self.ALGORITHMS_PATH)
        self.convertCheckboxEntriesToDictionary(self.listOfAlgorithms,self.algorithmsDictionary)

    def convertCheckboxEntriesToDictionary(self,checkboxEntry,dictionary):
        n = 1
        for entry in checkboxEntry:
            dictionary[entry.strip()] = n
            n+=1

    def generateAlgorithmsCheckboxes(self,startx,starty,incrementx,incrementy,numRows):
        variableCount = 0
        xposition = startx
        yposition = starty
        self.variablesForAlgorithmsCheckbox = []
        for algorithms in self.listOfAlgorithms:
            var = tk.IntVar()
            algorithmsCheckbox = tk.Checkbutton(self.guiPage, text=algorithms.strip(), variable=var)
            algorithmsCheckbox.place(x=xposition,y=yposition)
            variableCount += 1
            if variableCount == numRows:
                xposition += incrementx
                yposition = starty
                variableCount = 0
            else:
                yposition += incrementy
            self.variablesForAlgorithmsCheckbox.append(var)