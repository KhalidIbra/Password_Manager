from tkinter import *
import sqlite3, hashlib
from tkinter import simpledialog
from functools import partial
with sqlite3.connect('Password_Storage.db') as db:
    cursor = db.cursor()

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
''')

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
URL TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
''')

def popupwindow(text):
    answer = simpledialog.askstring('Input String', text)
    return answer




window = Tk()

window.title('Password Manager')

def hashpassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

def firstscreen():
    window.geometry('350x200')

    lbl = Label(window, text='Create Master Key')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text='Re-Enter Password')
    lbl1.pack()

    txt1 = Entry(window, width=25, show='*')
    txt1.pack()
    txt1.focus()

    lbl2 = Label(window)
    lbl2.pack()

    def savepassword():
        if txt.get() == txt1.get():
            hashedpassword = hashpassword(txt.get().encode('utf-8'))
            insert_password = ''' INSERT INTO masterpassword(password)
            VALUES(?) '''
            cursor.execute(insert_password, [(hashedpassword)])
            db.commit()

            PasswordStorage()
        else:
            lbl2.config(text='Passwords do not match')

    btn = Button(window, text='Save', command=savepassword)
    btn.pack(pady=10)


def loginwindow():
    window.geometry('300x100')

    lbl3 = Label(window, text='Enter Master Key')
    lbl3.config(anchor=CENTER)
    lbl3.pack()

    txt = Entry(window, width=25, show='*')
    txt.pack()
    txt.focus()

    lbl4 = Label(window)
    lbl4.pack()

    def getMasterPassword():
        checkHashedPassword = hashpassword(txt.get().encode('utf-8'))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND password = ?', [(checkHashedPassword)])
        print(checkHashedPassword)
        return cursor.fetchall()

    def checkpassword():

        match = getMasterPassword()

        print(match)

        if match:
            PasswordStorage()
        else:
            txt.delete(0, 'end')
            lbl3.config(text='Invalid Password')

    btn = Button(window, text='Log in', command=checkpassword)
    btn.pack(pady=10)


# Code for Password Storage window
def PasswordStorage():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1='URL'
        text2= 'Username'
        text3= 'Password'

        URL = popupwindow(text1)
        Username = popupwindow(text2)
        Password = popupwindow(text3)

        insert_fields = '''INSERT INTO vault(URL,username,password)
        VALUES(?, ?, ?)'''

        cursor.execute(insert_fields, (URL, Username, Password))
        db.commit()

        PasswordStorage()

    def removeEntry(input):
        cursor.execute('DELETE FROM vault WHERE id = ?', (input, ))
        db.commit()

        PasswordStorage()


    window.geometry('800x400')



    lbl = Label(window, text='Password Storage')
    lbl.grid(column=1)


    btn = Button(window, text='Add', command=addEntry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text='URL')
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text='Username')
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text='Password')
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute('SELECT * FROM vault')
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute('SELECT * FROM vault')
            array = cursor.fetchall()

            lbl1 = Label(window, text=(array[i][1]), font=('Arial', 14))
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=('Arial', 14))
            lbl1.grid(column=1, row=i + 3)
            lbl1 = Label(window, text=(array[i][3]), font=('Arial', 14))
            lbl1.grid(column=2, row=i + 3)

            btn = Button(window, text='Delete', command=partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=i+3, pady=10)

            i = i+1

            cursor.execute('SELECT * FROM vault')
            if (len(cursor.fetchall()) <= i):
                break 




cursor.execute('SELECT * FROM masterpassword')
if cursor.fetchall():
    loginwindow()
else:
    firstscreen()
window.mainloop()
