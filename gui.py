from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from rc4 import RC4

root = Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)


def raise_frame(frame):
    frame.tkraise()


def load_file():
    fname = askopenfilename(filetypes=(("Text files", "*.txt"),
                                       ("All files", "*.*")))


tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='RC4')
tabControl.add(tab2, text='Steganografi')
tabControl.pack(expand=1, fill="both")

# Adjust size
root.geometry("400x400")

# set minimum window size value
root.minsize(400, 400)

# set maximum window size value
root.maxsize(400, 400)

text_frame = ttk.Frame(tab1)
text_frame.grid(row=3, column=0, sticky='news', columnspan=20)
text_label = Label(
    text_frame, text="Text").grid(row=4, column=0)
text = Entry(text_frame)
text.grid(row=4, column=1)
key_label = Label(
    text_frame, text="Key").grid(row=5, column=0)
key = Entry(text_frame)
key.grid(row=5, column=1)
out = ""


def encryptText():
    global out
    txt = text.get()
    k = key.get()
    out = RC4.encrypt(txt.encode("utf-8"), k)
    print(RC4.decrypt(out, k))
    output_txt.insert(END, out)


def decryptText():
    global out
    txt = text.get()
    k = key.get()
    out = RC4.decrypt(txt.encode("utf-8"), k)
    output_txt.insert(END, out)


enc_bt = Button(text_frame, text="Encrypt", command=encryptText)
enc_bt.grid(row=6, column=0)
dec_bt = Button(text_frame, text="Decrypt", command=decryptText)
dec_bt.grid(row=6, column=1)
output_txt = Text(text_frame)
output_txt.grid(row=7, column=0, columnspan=10)

file_frame = ttk.Frame(tab1)
file_frame.grid(row=3, column=0, sticky='news', columnspan=20)
file_label = Label(
    file_frame, text="File").grid(row=4, column=0)
file = Button(file_frame, text="Browse", command=load_file, width=10)
file.grid(row=4, column=1, sticky=W)
keyf_label = Label(
    file_frame, text="Key").grid(row=5, column=0)
key_f = Entry(file_frame).grid(row=5, column=1)


def encryptFile():
    global out
    txt = text.get()
    k = key.get()
    out = RC4.encrypt(txt.encode("utf-8"), k)
    print(RC4.decrypt(out, k))
    output_txt.insert(END, out)


def decryptFile():
    global out
    txt = text.get()
    k = key.get()
    out = RC4.decrypt(txt.encode("utf-8"), k)
    output_txt.insert(END, out)


encf_bt = Button(file_frame, text="Encrypt")
encf_bt.grid(row=6, column=0)
decf_bt = Button(file_frame, text="Decrypt")
decf_bt.grid(row=6, column=1)
output = Text(file_frame)
output.grid(row=7, column=0, columnspan=10)


def on_field_change(index, value, op):
    if (typebox.get() == "Text"):
        print("text")
        raise_frame(text_frame)
    elif (typebox.get() == "File"):
        print("file")
        raise_frame(file_frame)
    else:
        print("error")


# label
ttk.Label(tab1, text="Select Type:",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=2)

# Combobox creation
v = StringVar()
v.trace('w', on_field_change)
typebox = ttk.Combobox(tab1, width=27, textvariable=v)

# Adding combobox drop down list
typebox['values'] = ('Text', 'File')

typebox.grid(column=1, row=2, columnspan=2)
typebox.current(0)


root.mainloop()
