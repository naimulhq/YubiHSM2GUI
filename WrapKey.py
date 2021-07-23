# Class dedicated for Wrap Key Operations
import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from yubihsm.defs import OBJECT

class WrapKey:
    def __init__(self, session, title):
        self.page = tk.Toplevel()
        self.page.title(title)
        self.page.resizable(0,0)
        self.page.geometry("700x300")
        self.wrapKeyList = []
        self.wrapKeyList = self.getListOfWrapKeys(session)
        self.wrapKeyListBox = tk.Listbox(self.page, height=8, width=30)
        for wrapKey in self.wrapKeyList:
            self.wrapKeyListBox.insert("end", wrapKey)
        self.dataEntry = tk.Entry(self.page)
        self.dataInstructions = tk.Label(self.page,text="Enter Data or File Path")
        self.wrapKeyInstructions = tk.Label(self.page, text="Choose Available Wrap Key")
        self.wrapKeyInstructions.place(x=240,y=0)
        self.wrapKeyListBox.place(x=240,y=20)
        self.dataInstructions.place(x=240,y=200)
        self.dataEntry.place(x=240,y=220)             

    def getListOfWrapKeys(self,session):
        wrapKeyStringList = []
        wrapKeyList = session.list_objects(object_type=OBJECT.WRAP_KEY)
        for wrapKeys in wrapKeyList:
            wrapKeyInfo = wrapKeys.get_info()
            wrapKeyStringList.append(wrapKeyInfo.label)
        return wrapKeyStringList

    def addSubmitButton(self, isEncrypt, xpos, ypos):
        if isEncrypt == True:
            self.submitButtonForWrap = tk.Button(self.page, text="Submit", command=self.encryptDataWithWrap)
        else:
            self.submitButtonForWrap = tk.Button(self.page, text="Submit", command=self.decryptDataWithWrap)
        self.submitButtonForWrap.place(x=xpos,y=ypos)



    def encryptDataWithWrap():
        pass

    def decryptDataWithWrap():
        pass    