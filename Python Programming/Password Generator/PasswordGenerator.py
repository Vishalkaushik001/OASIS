import os.path
import random
import pyperclip
from tkinter import *
from tkinter.ttk import *

def low():
    entry.delete(0, END)
    length = var1.get()
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()"
    password = ""

    if var.get() == 1:
        for i in range(length):
            password += random.choice(lower)
    elif var.get() == 0:
        for i in range(length):
            password += random.choice(upper)
    elif var.get() == 3:
        for i in range(length):
            password += random.choice(digits)
    
    return password

def generate():
    password1 = low()
    entry.insert(10, password1)

def copy1():
    random_password = entry.get()
    pyperclip.copy(random_password)

def checkExistence():
    if not os.path.exists("info.txt"):
        with open("info.txt", 'w') as file:
            pass

def appendNew():
    with open("info.txt", 'a') as file:
        userName = entry1.get()
        Random_password = entry.get()
        file.write("---------------------------------\n")
        file.write(f"UserName: {userName}\n")
        file.write(f"Password: {Random_password}\n")
        file.write("---------------------------------\n\n")
    
    root.destroy()  # it destroy the window
    main()          # and it recreate the window

def readPasswords():
    try:
        with open("info.txt", 'r') as file:
            data = file.read().strip().split("---------------------------------")
            last_entries = [d.strip() for d in data if d.strip()][-4:] 
    except FileNotFoundError:
        last_entries = ["No passwords stored yet."]

    top = Toplevel()
    top.title("Last 4 Saved Passwords")
    top.geometry("400x250")
    
    label = Label(top, text="Recent Passwords:", font=("Arial", 12, "bold"))
    label.pack(pady=10)

    for block in last_entries:
        Label(top, text=block, justify=LEFT, wraplength=350).pack(anchor="w", padx=10, pady=2)


def main():
    global root, entry1, entry, var, var1

    checkExistence()
    root = Tk()
    root.title("Python Password Manager")
    root.geometry("700x250")

    var = IntVar()
    var1 = IntVar()

    Label(root, text="Length").grid(row=0, column=0, padx=10, pady=10)

    combo = Combobox(root, textvariable=var1, width=10)
    combo['values'] = tuple(range(8, 33)) + ("Length",)
    combo.current(0)
    combo.grid(row=0, column=1, padx=10)

    radio_low = Radiobutton(root, text="Low", variable=var, value=1)
    radio_low.grid(row=0, column=2, padx=10)
    radio_middle = Radiobutton(root, text="Medium", variable=var, value=0)
    radio_middle.grid(row=0, column=3, padx=10)
    radio_strong = Radiobutton(root, text="Strong", variable=var, value=3)
    radio_strong.grid(row=0, column=4, padx=10)

    generate_button = Button(root, text="Generate", command=generate)
    generate_button.grid(row=1, column=2, pady=10, padx=10)

    Label(root, text="Enter Username").grid(row=2, column=0, padx=10, pady=10)
    entry1 = Entry(root, width=30)
    entry1.grid(row=2, column=1, columnspan=2, padx=10)

    Label(root, text="Generated Password").grid(row=3, column=0, padx=10, pady=10)
    entry = Entry(root, width=30)
    entry.grid(row=3, column=1, columnspan=2, padx=10)

    save_button = Button(root, text="Save", command=appendNew)
    save_button.grid(row=4, column=1, pady=10, padx=10)
    show_button = Button(root, text="Show All Passwords", command=readPasswords)
    show_button.grid(row=4, column=2, pady=10, padx=10)

    copy_button = Button(root, text="Copy Password", command=copy1)
    copy_button.grid(row=4, column=3, pady=10, padx=10)


    root.mainloop()


main()