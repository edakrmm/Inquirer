from cryptography.fernet import Fernet, InvalidToken
import os
from os import walk

from tkinter import *
from tkinter.ttk import *
import mysql.connector
from tkinter.messagebox import showinfo

# Generate Key and Store

# key = Fernet.generate_key()
# with open("fernet_key.key", "wb") as f:
#     f.write(key)


mydb = mysql.connector.connect(user="r3ader", password="Masasandalye1", host="localhost", database="testdb")
cursor = mydb.cursor()

query = "SELECT * FROM file_paths"
insertQuery = "INSERT INTO file_paths(path) VALUES (%s)"
deleteRowQuery = "DELETE FROM file_paths WHERE path="


class App(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master['bg']='black'
        self.master.title("Security Check for Intruders")
        self.master.geometry("650x340")
        self.p_label = Label(self, text="Enter Password Within 1 Minute:")
        self.p_label.pack()
        self.p_entry = Entry(self, width=30, show="*")
        self.p_entry.pack(padx=20, pady=1)
        self.p_entry.focus()
        self.enterPasswordButton = Button(self, text="Enter", width=10, command= self.check)
        self.enterPasswordButton.pack(padx=20, pady=1)
        self.label = Label(self, text="Enter file path to encrypt: ")
        self.label.pack()
        self.entry = Entry(self, state='disabled')
        self.entry.pack(fill=X, padx=20)
        self.tree = self.create_tree()
        self.tree.pack(fill=X, padx=20, pady = 10, expand = False )
        self.enterPathButton = Button(self, text="Enter", command= self.enter_path, state='disabled')
        self.exitButton= Button(self, text="Quit", command=self.exit_app, state='disabled')
        self.enterDeleteButton = Button(self, text="Delete", command=self.delete_rows, state='disabled')
        self.enterPathButton.pack(fill=X, padx=20, pady=1)
        self.enterDeleteButton.pack(fill=X,padx=20, pady=1)
        self.exitButton.pack(fill=X, padx=20, pady=1)

        self.master.after(60000, self.check)
        
        
    def create_tree(self):

        tv = Treeview(self, columns=(1,), show="headings", height=5)
        tv.heading(1, text="Path",anchor=S)
        scrollbar = Scrollbar(self, orient=VERTICAL, command=tv.yview)
        tv.configure(yscroll=scrollbar.set)
        tv.bind('<<TreeviewSelect>>', self.get_selected_row)

        return tv


    def update_tree(self):
        for items in self.tree.get_children():
            self.tree.delete(items)

        cursor.execute(query)
        entries = cursor.fetchall()

        for entry in entries:
            self.tree.insert('','end', values = entry)


    def enter_path(self):
        
        value = (str(self.entry.get()),)

        if len(self.entry.get()) != 0:
            try:
                cursor.execute(insertQuery,value)
                mydb.commit()
            except:
                showinfo(title='Information', message="Path Already Exists")


        self.entry.delete(0, 'end')
        self.update_tree()


    def exit_app(self):
        self.master.destroy()


    def get_selected_row(self, event):
        global item
        selected_item = self.tree.selection()
        item = str(self.tree.item(selected_item, 'values')).strip('(),')


    def delete_rows(self):
        cursor.execute(deleteRowQuery+item)
        mydb.commit()

        self.update_tree()
        
    
    def check(self):
        if self.p_entry.get()=="password":
            self.enterPathButton["state"] = "NORMAL"
            self.enterDeleteButton["state"] = "NORMAL"
            self.exitButton["state"] = "NORMAL"
            self.entry["state"] = "NORMAL"
            self.p_entry["state"] = "disabled"
            self.enterPasswordButton['state'] = "disabled"

            self.update_tree()
            try:
            #Get the key
                with open("fernet_key.key", "rb") as f:
                    key = f.read()

                cursor.execute(query)
                entries = cursor.fetchall()
            
                # #Decrypt Files
                for entry in entries:
                    for (dirpath, dirnames, filenames) in walk(entry[0]+"\\"):
                        for i in filenames:
                            with open(dirpath+i,"rb") as f:
                                data = f.read() 
                                fernet = Fernet(key) 
                                decrypted = fernet.decrypt(data)
                                with open(dirpath+i,"wb") as g:
                                    g.write(decrypted)
                showinfo(title='Information', message="Files are Decrypted!")
            except InvalidToken:
                pass
            
        else:
            try:
                #Get the key
                with open("fernet_key.key", "rb") as f:
                    key = f.read()

                cursor.execute(query)
                entries = cursor.fetchall()
                
                #Encrypt Files
                for entry in entries:
                    for (dirpath, dirnames, filenames) in walk(entry[0]+"\\"):
                        for i in filenames:
                            with open(dirpath+i,"rb") as f:
                                data = f.read()
                                fernet = Fernet(key)   
                                encrypted = fernet.encrypt(data)
                                with open(dirpath+i,"wb") as g:
                                    g.write(encrypted)
                showinfo(title='Information', message="Files are Encrypted!")
            except:
                showinfo(title='Error', message="Exception Occured During the Encyrption")
            

def main():
    root = Tk()
    App(root).pack(expand=True, fill='both')
    root.mainloop()

if __name__ == "__main__":
    main()
