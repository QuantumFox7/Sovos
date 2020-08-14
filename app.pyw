from base64 import urlsafe_b64encode
import os
from sys import exit as Exit
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from random import randint
from easygui import passwordbox, textbox, indexbox, enterbox, msgbox
from bcrypt import hashpw, gensalt, checkpw
from secrets import choice
from datafiles import * 

class Info:
    pwData = "password.data"
    infoData = "data.data"
    dataFile = "Sovos.data"
    dataFileName = "Sovos"
    dataFileVars = ["Password", "Data"]
    InfoPage = ""

class GUI:
    title = "Sovos"
    
    def PasswordBox(mode):
        if mode == 0: return passwordbox("Please enter your password.", GUI.title)
        elif mode == 1: return passwordbox("Incorrect Password, Please try again.", GUI.title)
        elif mode == 2: return passwordbox("Please enter your new password.", GUI.title)
    
    def EnterBox(info): return textbox("Information stored in system", GUI.title, info)

    def Menu(): return indexbox("Main Menu", GUI.title, ("Information", "Change Password", "Generate Password", "Info", "Exit"))

    def PWLen(): return enterbox("Please enter password length", GUI.title)

    def PWDis(password):
        if password == None: msgbox("Error Creating Password, Check that password length is a number.", GUI.title)
        else: msgbox(f"Your password is: {password}", GUI.title)

    def InfoPage(): msgbox(Info.InfoPage, GUI.title)

class Password:
    password = ""
    key = ""
    def Key():
        salt = b'h-94_jN@vAqzh&dex%pkf~'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        Password.key = urlsafe_b64encode(kdf.derive(Password.password))
        

    
    def Getter(mode):
        if Files.Read(Info.pwData,"r+") == "": mode = 2
        password = GUI.PasswordBox(mode)
        if password == "": sys.exit(0)
        Password.password = password.encode()
        if Files.Read(Info.pwData,"r+") == "": Files.Edit(Info.pwData, hashpw(Password.password, gensalt()).decode())
        Password.Checker()
        

    def Checker():
        if not checkpw(Password.password, Files.Read(Info.pwData, "rb")): Password.Getter(1)
        else:
            Password.Key()
            Data.Unlocked()

    def Change(UD):
        New = GUI.PasswordBox(2)
        if New == None: return
        Password.password = New.encode()
        Password.Key()
        Files.Edit(Info.pwData, hashpw(Password.password, gensalt()).decode())
        Files.Edit(Info.infoData, Encryption.Encrypt(UD.encode()).decode())
        
        
class Data:
    def CreateFiles():
        Dir = os.listdir()
        if not Info.dataFile in Dir: createDF(Info.dataFileName, Info.dataFileVars)
                
    def Unlocked():
        encrypted_data = Files.Read(Info.infoData, "r+").encode()
        if encrypted_data == b"":
            Data.Empty()
            encrypted_data = Files.Read(Info.infoData, "r+").encode()
        encrypted_data = Files.Read(Info.infoData, "r+").encode()
        unencrypted_data = str(Encryption.Decrypt(encrypted_data).decode())
        Data.MenuHandler(unencrypted_data)
        
    def Empty():
        Files.Edit(Info.infoData, Encryption.Encrypt(b"").decode())

    def MenuHandler(infor):
        Menu = GUI.Menu()
        if Menu == 0:
            GUIInfo = GUI.EnterBox(infor)
            if not GUIInfo == None: Files.Edit(Info.infoData, Encryption.Encrypt(GUIInfo.encode()).decode())
        elif Menu == 1: Password.Change(infor)
        elif Menu == 2: GUI.PWDis(Data.GenPassword(GUI.PWLen()))
        elif Menu == 3: GUI.InfoPage()
        elif Menu == 4: Exit()
        else: Exit()
        Data.Unlocked()

    def GenPassword(length):
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!_-£$!_-£$!_-£$"
        if not length.isdigit(): return
        else: length = int(length)
        n = ''.join(choice(string) for i in range(length))
        return n

class Encryption:
    def Encrypt(data):
        fernet = Fernet(Password.key)
        return fernet.encrypt(data)
    
    def Decrypt(data):
        fernet = Fernet(Password.key)
        return fernet.decrypt(data)
        
class Files:
    def Edit(file, text):
        if file == Info.pwData:
            writeVar(Info.dataFileName, "Password", text)
        if file == Info.infoData:
            writeVar(Info.dataFileName, "Data", text)
    
    def Read(file, Type):
        if file == Info.pwData:
            read = readVar(Info.dataFileName, "Password")
        if file == Info.infoData:
            read = readVar(Info.dataFileName, "Data")
        if Type == "rb":
            read = read.encode()
        return read

def Main():
    Data.CreateFiles()
    Info.InfoPage = f"Info Page\n\nVersion: 4\n\nPython Modules: Cryptography, OS, SYS, Base64, EasyGUI, BCrypt, Secrets, Random, DataFiles\n\nFiles: {Info.dataFile} (Stores Password)"
    Password.Getter(0)

Main()
