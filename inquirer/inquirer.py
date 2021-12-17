from cryptography.fernet import Fernet
from watchdog.events import FileSystemEventHandler
import os

from tkinter import *
from tkinter.ttk import *
import mysql.connector
from tkinter.messagebox import showinfo

# Generate Key and Store

# key = Fernet.generate_key()
# with open("fernet_key.key", "wb") as f:
#     f.write(key)


# Get the key
# with open("fernet_key.key", "rb") as f:
#     key = f.read()



# #Encrypt File
# with open("Kıbrıs Çağrı Açma.PNG","rb") as f:
#     data = f.read()
#     fernet = Fernet(key)   
#     encrypted = fernet.encrypt(data)
#     with open("Kıbrıs Çağrı Açma.PNG","wb") as g:
#         g.write(encrypted)

mydb = mysql.connector.connect(user="r3ader", password="Masasandalye1", host="localhost", database="testdb")
cursor = mydb.cursor()

query = "SELECT * FROM file_paths"

insertQuery = "INSERT INTO file_paths(path) VALUES (%s)"

deleteRowQuery = "DELETE FROM file_paths WHERE path="


class App(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.master.title("Security Check for Intruders")
        self.master.geometry("650x300")

        self.entry = Entry(self)
        self.entry.focus()
        self.entry.pack()
        self.enterPathButton = Button(self, text="Enter", width=10, command= self.enter_path)
        self.exitButton= Button(self, text="Quit", width=10, command=self.exit_app)
        self.enterDeleteButton = Button(self, text="Delete", width=10, command=self.delete_rows)
        self.enterDeleteButton.pack(side = BOTTOM)
        self.exitButton.pack(side = BOTTOM)
        self.enterPathButton.pack(side = BOTTOM)
        self.tree = self.create_tree()
        self.tree.pack(fill=X, padx=20)
        
        
    def create_tree(self):
        cursor.execute(query)
        entries = cursor.fetchall()

        tv = Treeview(self, columns=(1,), show="headings")
        tv.heading(1, text="path",anchor=S)
        scrollbar = Scrollbar(self, orient=VERTICAL, command=tv.yview)
        tv.configure(yscroll=scrollbar.set)
        tv.bind('<<TreeviewSelect>>', self.get_selected_row)

        for entry in entries:
            tv.insert('','end', values = entry)

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
        
        
def main():
    root = Tk()
    App(root).pack(expand=True, fill='both')
    #root.after(10000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()


class MyHandler(FileSystemEventHandler):
    def on_modified(self,event):
        print("asd")

# #Decrypt File
# with open("Kıbrıs Çağrı Açma.PNG","rb") as f:
#     data = f.read() 
#     decrypted = fernet.decrypt(data)
#     with open("Kıbrıs Çağrı Açma.PNG","wb") as g:
#         g.write(decrypted)

