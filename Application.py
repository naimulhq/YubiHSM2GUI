# GUI for YubiHSM
import os
import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox


class Application:
    
    def __init__(self):
        self.GUI_GEOMETRY = "700x200"
        self.createLoginPage()
        pass

    def createLoginPage(self):
        self.loginPage = tk.Tk()
        self.loginPage.title('YubiHSM2 Tool')
        self.loginPage.resizable(0,0)
        self.loginPage.geometry(self.GUI_GEOMETRY)
        self.usernameEntry = tk.Entry(self.loginPage)
        self.objectIDEntry = tk.Entry(self.loginPage)
        self.passwordEntry = tk.Entry(self.loginPage,show='*')
        self.usernameInstructions = tk.Label(self.loginPage, text="Enter Username")
        self.objectIDInstructions = tk.Label(self.loginPage, text="Enter Object ID")
        self.passwordInstructions = tk.Label(self.loginPage, text="Enter Password")
        self.submitButtonForLogin = tk.Button(self.loginPage, text="Submit", command=self.checkLoginCredentials)
        self.usernameInstructions.pack()
        self.usernameEntry.pack()
        self.objectIDInstructions.pack()
        self.objectIDEntry.pack()
        self.passwordInstructions.pack()
        self.passwordEntry.pack()
        self.submitButtonForLogin.pack(side='right')
        self.loginPage.mainloop()

    def checkLoginCredentials(self):
        pass


    

if __name__ == '__main__':
    app = Application()