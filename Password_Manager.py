import sqlite3, hashlib
from tkinter import *

window = Tk()

window.title('Password Manager')


def firstscreen():
    window.geometry('300x100')

    lbl = Label(window, text='Create Master Key')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20)
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
            pass
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

def checkpassword():
    password = 'Pword'

    if password == txt.get():
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
    window.geometry('800x400')

    lbl = Label(window, text='Password Storage')
    lbl.config(anchor=CENTER)
    lbl.pack()




firstscreen()
window.mainloop()