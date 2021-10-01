import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

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


def on_field_change(index, value, op):
    if (typebox.get() == "Text"):
        print("text")
    elif (typebox.get() == "File"):
        print("file")
    else:
        print("error")


# label
ttk.Label(tab1, text="Select Type:",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=5, padx=10, pady=25)

# Combobox creation
v = tk.StringVar()
v.trace('w', on_field_change)
typebox = ttk.Combobox(tab1, width=27, textvariable=v)

# Adding combobox drop down list
typebox['values'] = ('Text', 'File')

typebox.grid(column=1, row=5)
typebox.current(0)


root.mainloop()
