# Class dedicated for Wrap Key Operations
import tkinter as tk
import PIL
import os
from PIL import ImageTk
from PIL import Image
import yubihsm
from yubihsm.defs import OBJECT
from tkinter import messagebox

class WrapKey:
    def __init__(self, session, title):
        self.session = session
        self.page = tk.Toplevel()
        self.page.title(title)
        self.page.resizable(0,0)
        self.page.geometry("700x300")
        self.wrapKeyNameToObjectIDMap = {}
        self.getListOfWrapKeys()
        self.wrapKeyListBox = tk.Listbox(self.page, height=8, width=30)
        for wrapKey in self.wrapKeyNameToObjectIDMap.keys():
            self.wrapKeyListBox.insert("end", wrapKey)
        self.dataEntry = tk.Entry(self.page)
        self.dataInstructions = tk.Label(self.page,text="Enter Data or File Path")
        self.wrapKeyInstructions = tk.Label(self.page, text="Choose Available Wrap Key")
        self.wrapKeyInstructions.place(x=240,y=0)
        self.wrapKeyListBox.place(x=240,y=20)
        self.dataInstructions.place(x=240,y=200)
        self.dataEntry.place(x=240,y=220)             

    def getListOfWrapKeys(self):
        wrapKeyList = self.session.list_objects(object_type=OBJECT.WRAP_KEY)
        for wrapKeys in wrapKeyList:
            wrapKeyInfo = wrapKeys.get_info()
            self.wrapKeyNameToObjectIDMap[wrapKeyInfo.label] = wrapKeyInfo.id

    def addSubmitButton(self, isEncrypt, xpos, ypos):
        if isEncrypt == True:
            self.submitButtonForWrap = tk.Button(self.page, text="Submit", command=self.encryptDataWithWrap)
        else:
            self.submitButtonForWrap = tk.Button(self.page, text="Submit", command=self.decryptDataWithWrap)
        self.submitButtonForWrap.place(x=xpos,y=ypos)

    def encryptDataWithWrap(self):
        data = self.dataEntry.get()
        objectLabel = self.wrapKeyListBox.get(tk.ANCHOR)
        wrapKey = self.session.get_object(object_id=self.wrapKeyNameToObjectIDMap[objectLabel], object_type=OBJECT.WRAP_KEY)
        try:
            encryptedData = wrapKey.wrap_data(data.encode('utf-8'))
            print(encryptedData)
            print(type(encryptedData))
            print(encryptedData.decode('latin-1'))
            encryptedDataFile = open("encryptedOutput.txt","w+")
            encryptedDataFile.write(encryptedData.decode('latin-1'))
            encryptedDataFile.close()
        except Exception as exceptionText:
            messagebox.showerror(title='Unexpected Error', message=exceptionText)

    def decryptDataWithWrap(self):
        data = self.dataEntry.get()
        objectLabel = self.wrapKeyListBox.get(tk.ANCHOR)
        wrapKey = self.session.get_object(object_id=self.wrapKeyNameToObjectIDMap[objectLabel], object_type=OBJECT.WRAP_KEY)
        try:
            decryptedData = wrapKey.unwrap_data(data.encode('utf-8'))
            print(decryptedData)
            print(decryptedData.decode('latin-1'))
            print(decryptedData.decode('utf-8'))
            decryptedDataFile = open("decryptedOutput.txt", "w+")
            decryptedDataFile.write(str(decryptedData.decode('latin-1')))
            decryptedDataFile.close()
        except Exception as exceptionText:
            messagebox.showerror(title='Unexpected Error', message=exceptionText)