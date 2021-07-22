# GUI for YubiHSM
import os
import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
import struct
from tkinter import messagebox
from yubihsm import YubiHsm
from yubihsm.exceptions import YubiHsmAuthenticationError, YubiHsmConnectionError
from yubihsm.defs import OBJECT
from yubihsm.objects import AuthenticationKey

class Application:
    
    def __init__(self):
        self.GUI_GEOMETRY = "700x300"
        self.IMAGE_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/LC.png"
        self.HSM_URL = "http://127.0.0.1:12345"
        self.COMMANDS_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/commands.txt"
        self.commandToWindowMapping = {
            "Get Device Info": self.getDeviceInfoWindow
            "Put Authentication Key": self.putAuthKeyWindow}
        self.commandsForHSM = self.getHSMCommands()
        self.hsm = YubiHsm.connect(self.HSM_URL)
        self.createLoginPage()
        
    def getHSMCommands(self):
        self.failedToRetrieveCommands = False
        try:
            with open(self.COMMANDS_PATH) as commandsFile:
                return commandsFile.readlines()
        except Exception as exceptionText:
            self.exceptionText = exceptionText
            self.failedToRetrieveCommands = True
            

    def createLoginPage(self):
        self.loginPage = tk.Tk()
        self.loginPage.title('YubiHSM2 Tool')
        self.loginPage.resizable(0,0)
        self.loginPage.geometry(self.GUI_GEOMETRY)
        img = ImageTk.PhotoImage(Image.open(self.IMAGE_PATH))
        panel = tk.Label(self.loginPage,image=img)
        self.objectIDEntry = tk.Entry(self.loginPage)
        self.passwordEntry = tk.Entry(self.loginPage,show='*')
        self.objectIDInstructions = tk.Label(self.loginPage, text="Enter Object ID")
        self.passwordInstructions = tk.Label(self.loginPage, text="Enter Password")
        self.submitButtonForLogin = tk.Button(self.loginPage, text="Submit", command=self.checkLoginCredentials)
        if self.failedToRetrieveCommands is True:
            self.submitButtonForLogin['state'] = 'disabled'
            messagebox.showerror(title="File not Found", message=self.exceptionText)
        self.objectIDInstructions.pack()
        self.objectIDEntry.pack()
        self.passwordInstructions.pack()
        self.passwordEntry.pack()
        panel.place(x=70,y=200)
        self.submitButtonForLogin.place(x=600,y=100)
        self.loginPage.mainloop()

    def checkLoginCredentials(self):
        try:
            self.session = self.hsm.create_session_derived(int(self.objectIDEntry.get()), self.passwordEntry.get())
            self.chooseCommand()
        except ValueError:
            messagebox.showerror(title='Invalid ObjectID', message='Object ID has to be an integer')
        except YubiHsmConnectionError:
            messagebox.showerror(title='Connection Error', message='Can not communicate with YubiHSM. Check connection.')
        except YubiHsmAuthenticationError:
            messagebox.showerror(title='Invalid Credentials', message='The username or password is incorrect')

    def chooseCommand(self):
        self.commandsPage = tk.Toplevel()
        self.commandsPage.title('YubiHSM Commands')
        self.commandsPage.resizable(0,0)
        self.commandsPage.geometry(self.GUI_GEOMETRY)
        img = ImageTk.PhotoImage(Image.open(self.IMAGE_PATH))
        panel = tk.Label(self.commandsPage,image=img)
        self.commandsList = tk.Listbox(self.commandsPage,height=8,width=30)
        self.submitButtonForCommand = tk.Button(self.commandsPage, text="Submit", command=self.getWindowBasedOnCommand)
        scrollbarForCommands = tk.Scrollbar(self.commandsPage)
        for command in self.commandsForHSM:
            self.commandsList.insert("end", command.strip())
        self.commandsList.config(yscrollcommand = scrollbarForCommands.set)
        scrollbarForCommands.config(command = self.commandsList.yview)
        self.commandsList.place(x=240,y=20)
        self.submitButtonForCommand.place(x=600,y=100)
        panel.place(x=70,y=200)
        self.commandsPage.mainloop()
    
    def getWindowBasedOnCommand(self):
        command = self.commandsList.get(tk.ANCHOR)
        self.commandToWindowMapping[command]()

    def getDeviceInfoWindow(self):
        self.deviceInfoPage = tk.Toplevel()
        deviceInfo = self.hsm.get_device_info()
        self.commandsPage.title('Device Info')
        self.deviceInfoPage.resizable(0,0)
        self.deviceInfoPage.geometry(self.GUI_GEOMETRY)
        img = ImageTk.PhotoImage(Image.open(self.IMAGE_PATH))
        panel = tk.Label(self.deviceInfoPage,image=img)
        deviceVersion = getVersionString(deviceInfo.version) # Tuple -> String conversion
        deviceSerial = getSerialString(deviceInfo.serial)
        logSize = getLogSizeString(deviceInfo.log_size)
        logUsed = getLogUsedString(deviceInfo.log_used)
        supportedAlgorithms = getListOfSupportedAlgorithms(deviceInfo.supported_algorithms)
        scrollbar = tk.Scrollbar(self.deviceInfoPage)
        scrollbar.pack(side='right', fill='y')
        deviceInfoText = tk.Text(self.deviceInfoPage,width=10,height=10,yscrollcommand=scrollbar.set)
        deviceInfoText.insert("end",deviceVersion)
        deviceInfoText.insert("end",deviceSerial)
        deviceInfoText.insert("end",logSize)
        deviceInfoText.insert("end",logUsed)
        for algorithm in supportedAlgorithms:
            deviceInfoText.insert("end", algorithm)
            deviceInfoText.insert("end","\n")
        deviceInfoText.pack(side='top',fill='x')
        scrollbar.config(command=deviceInfoText.yview)
        panel.place(x=70,y=200)
        self.deviceInfoPage.mainloop()

    def putAuthKeyWindow(self):
        self.putAuthKeyPage = tk.Toplevel()
        self.putAuthKeyPage.title("Put Authentication Key")
        self.putAuthKeyPage.resizable(0,0)
        self.putAuthKeyPage.geometry(self.GUI_GEOMETRY)
        img = ImageTk.PhotoImage(Image.open(self.IMAGE_PATH))
        panel = tk.Label(self.putAuthKeyPage,image=img)
        instructionForPasswordEntry = tk.Label(self.putAuthKeyPage, text="Enter password for Auth Key:")
        instructionsForConfirmPasswordEntry = tk.Label(self.putAuthKeyPage, text="Confirm Password:")
        instructionsForObjectIDEntry = tk.Label(self.putAuthKeyPage,text="Enter Object ID (decimal format):")
        instructionsForLabel = tk.Label(self.putAuthKeyPage, text="Enter Label For Object")
        self.passwordEntry = tk.Entry(self.putAuthKeyPage, show='*')
        self.confirmPasswordEntry = tk.Entry(self.putAuthKeyPage, show='*')
        self.objectIDEntryForPutAuthKey = tk.Entry(self.putAuthKeyPage)
        self.labelForPutAuthKey = tk.Entry(self.putAuthKeyPage)
        instructionsForLabel.pack()
        self.labelForPutAuthKey.pack()
        instructionsForObjectIDEntry.pack()
        self.objectIDEntryForPutAuthKey.pack()
        instructionForPasswordEntry.pack()
        self.passwordEntry.pack()
        instructionsForConfirmPasswordEntry.pack()
        self.confirmPasswordEntry.pack()
        panel.place(x=70,y=200)
        self.putAuthKeyPage.mainloop()

def getVersionString(deviceVersion):
    versionString = "Device Version: "
    for number in deviceVersion:
        versionString += str(number) + "."
    return versionString + "\n"

def getSerialString(deviceSerial):
    return "Device Serial #: " + str(deviceSerial) + "\n"

def getLogSizeString(logSize):
    return "Log Size: " + str(logSize) + "\n"

def getLogUsedString(logUsed):
    return "Log Used: " + str(logUsed) + "\n"

def getListOfSupportedAlgorithms(supportedAlgorithms):
    listOfSupportedAlgorithms = []
    for algorithm in supportedAlgorithms:
        listOfSupportedAlgorithms.append(algorithm)
    return listOfSupportedAlgorithms

if __name__ == '__main__':
    app = Application()