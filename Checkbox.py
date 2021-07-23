import tkinter as tk

def getChecboxNames(filePath):
    with open(filePath) as checkboxNames:
        return checkboxNames.readlines()



class Checkbox:
    def __init__(self, page):
        self.guiPage = page
        self.DOMAINS_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/textfiles/domains.txt"
        self.CAPABILITIES_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/textfiles/capabilities.txt"
        self.domainDictionary = {}
        self.capabilitiesDictionary = {}
        self.configureCheckboxesAndValues()

    def configureCheckboxesAndValues(self):
        self.listOfDomains = getChecboxNames(self.DOMAINS_PATH)
        self.listOfCapabilities = getChecboxNames(self.CAPABILITIES_PATH)
        self.convertCheckboxEntriesToDictionary(self.listOfDomains, self.domainDictionary)
        self.convertCheckboxEntriesToDictionary(self.listOfCapabilities, self.capabilitiesDictionary)

    def convertCheckboxEntriesToDictionary(self, checkboxEntry, dictionary):
        n = 0
        for entry in checkboxEntry:
            dictionary[entry.strip()] = 2 ** n
            n+=1

    def generateDomainCheckboxes(self,startx,starty,incrementx,incrementy,numRows):
        variableCount = 0
        xposition = startx
        yposition = starty
        self.variableForDomainsCheckbox = []
        for domain in self.listOfDomains:
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
        xposition = startx
        yposition = starty
        self.variablesForCapabilitiesCheckbox = []
        for capabilities in self.listOfCapabilities:
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

    def generateDelegatedCapabilitiesCheckboxes(self,startx,starty,incrementx,incrementy,numRows):
        variableCount = 0
        xposition = startx
        yposition = starty
        self.variablesForDelegatedCapabilitiesCheckbox = []
        for capabilities in self.listOfCapabilities:
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
            self.variablesForDelegatedCapabilitiesCheckbox.append(var)


    def convertDomainCheckboxToInt(self):
        sum = 0
        for index in range(len(self.variableForDomainsCheckbox)):
            isCheckboxPressed = self.variableForDomainsCheckbox[index].get()
            if isCheckboxPressed == 1:
                domain = self.listOfDomains[index].strip()
                value = self.domainDictionary[domain]
                sum += value
        return sum
            
    def convertCapabilitiesCheckboxToInt(self):
        sum = 0
        for index in range(len(self.variablesForCapabilitiesCheckbox)):
            isCheckboxPressed = self.variablesForCapabilitiesCheckbox[index].get()
            if isCheckboxPressed == 1:
                capability = self.listOfCapabilities[index].strip()
                value = self.capabilitiesDictionary[capability]
                sum += value
        return sum

    def convertDelegatedCapabilitiesCheckboxToInt(self):
        sum = 0
        for index in range(len(self.variablesForDelegatedCapabilitiesCheckbox)):
            isCheckboxPressed = self.variablesForDelegatedCapabilitiesCheckbox[index].get()
            if isCheckboxPressed == 1:
                capability = self.listOfCapabilities[index].strip()
                value = self.capabilitiesDictionary[capability]
                sum += value
        return sum
