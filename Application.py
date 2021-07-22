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


class Application:
    
    def __init__(self):
        self.GUI_GEOMETRY = "700x300"
        self.IMAGE_PATH = "/home/naimul/NaimulRepo/YubiHSM2Tool/LC.png"
        self.HSM_URL = "http://127.0.0.1:12345"
        self.hsm = YubiHsm.connect(self.HSM_URL)
        self.createLoginPage()
        pass

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
        self.commandsList = tk.Listbox(self.commandsPage,height=5,width=10)
        scrollbarForCommands = tk.Scrollbar(self.commandsPage)
        for values in range(100):
            self.commandsList.insert("end", values)
        self.commandsList.config(yscrollcommand = scrollbarForCommands.set)
        scrollbarForCommands.config(command = self.commandsList.yview)
        self.commandsList.place(x=250,y=20)
        panel.place(x=70,y=200)
        self.commandsPage.mainloop()


if __name__ == '__main__':
    app = Application()