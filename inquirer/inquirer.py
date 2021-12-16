from cryptography.fernet import Fernet
from watchdog.events import FileSystemEventHandler
import os
from tkinter import *


# Generate Key and Store

# key = Fernet.generate_key()
# with open("fernet_key.key", "wb") as f:
#     f.write(key)


# Get the key
with open("fernet_key.key", "rb") as f:
    key = f.read()



#Encrypt File
with open("Kıbrıs Çağrı Açma.PNG","rb") as f:
    data = f.read()
    fernet = Fernet(key)   
    encrypted = fernet.encrypt(data)
    with open("Kıbrıs Çağrı Açma.PNG","wb") as g:
        g.write(encrypted)

# def enter_path():
#     filePaths.append(E1.get())
#     print(filePaths)

# def exit_app():
#     top.destroy




class App(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.entry = Entry(self)
        self.entry.focus()
        self.entry.pack()
        self.enterPathButton = Button(self, text="Enter", width=10, command=self.enter_path)
        self.exitButton= Button(self, text="Quit", width=10, command=self.exit_app)
        self.exitButton.pack(side = BOTTOM)
        self.enterPathButton.pack(side = BOTTOM)
        self.filePaths = []

    def enter_path(self):
        self.filePaths.append(self.entry.get())
        self.entry.delete(0, 'end')
        print(self.filePaths)

    def exit_app(self):
        self.master.destroy()


def main():
    root = Tk()
    App(root).pack(expand=True, fill='both')
    root.after(10000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()


class MyHandler(FileSystemEventHandler):
    def on_modified(self,event):
        print("asd")

#Decrypt File
with open("Kıbrıs Çağrı Açma.PNG","rb") as f:
    data = f.read() 
    decrypted = fernet.decrypt(data)
    with open("Kıbrıs Çağrı Açma.PNG","wb") as g:
        g.write(decrypted)

