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
            self.getOptionsBasedOffAuthenticationKey()
        except ValueError:
            messagebox.showerror(title='Invalid ObjectID', message='Object ID has to be an integer')
        except YubiHsmConnectionError:
            messagebox.showerror(title='Connection Error', message='Can not communicate with YubiHSM. Check connection.')
        except YubiHsmAuthenticationError:
            messagebox.showerror(title='Invalid Credentials', message='The username or password is incorrect')

    def getOptionsBasedOffAuthenticationKey(self):
        pass

if __name__ == '__main__':
    app = Application()