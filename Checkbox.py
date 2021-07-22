import tkinter as tk

def getChecboxNames(filePath):
    with open(filePath) as checkboxNames:
        return checkboxNames.readlines()



class Checkbox:
    def __init__(self, page):
        self.guiPage = page
        self.DOMAINS_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/textfiles/domains.txt"
        self.CAPABILITIES_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/textfiles/capabilities.txt"

    def generateDomainCheckboxes(self,startx,starty,incrementx,incrementy,numRows):
        variableCount = 0
        listOfDomains = getChecboxNames(self.DOMAINS_PATH)
        xposition = startx
        yposition = starty
        self.variableForDomainsCheckbox = []
        for domain in listOfDomains:
            var = tk.IntVar()
            domainCheckbox = tk.Checkbutton(self.guiPage,text=domain.strip(),variable=var)
            domainCheckbox.place(x=xposition,y=yposition)
            variableCount += 1
            if variableCount == numRows:
                xposition += incrementx
                yposition =  starty
                variableCount = 0
            else:
                yposition += incrementy
            self.variableForDomainsCheckbox.append(var)
        

    def generateCapabilitiesCheckboxes(self,startx,starty,incrementx,incrementy,numRows):
        variableCount = 0
        listOfCapabilities = getChecboxNames(self.CAPABILITIES_PATH)
        xposition = startx
        yposition = starty
        self.variablesForCapabilitiesCheckbox = []
        for capabilities in listOfCapabilities:
            var = tk.IntVar()
            capabilitiesCheckbox = tk.Checkbutton(self.guiPage, text=capabilities.strip(), variable=var)
            capabilitiesCheckbox.place(x=xposition,y=yposition)
            variableCount += 1
            if variableCount == numRows:
                xposition += incrementx
                yposition = starty
                variableCount = 0
            else:
                yposition += incrementy
            self.variablesForCapabilitiesCheckbox.append(var)
