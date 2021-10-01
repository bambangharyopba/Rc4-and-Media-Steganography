from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from rc4 import RC4
import wave
from wav_stego import WavStego
from img_stego import imgStego, is_grey_scale
import sys
import PIL
from psnr import psnr

root = Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)


def raise_frame(frame):
    frame.tkraise()


fname = ""
fnameS = ""


def load_file():
    global fname
    fname = askopenfilename(filetypes=(("Text files", "*.txt"),
                                       ("All files", "*.*")))


def load_fileS():
    global fnameS
    fnameS = askopenfilename(filetypes=(("Text files", "*.txt"),
                                        ("All files", "*.*")))


tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='RC4')
tabControl.add(tab2, text='Steganografi')
tabControl.add(tab3, text='PSNR')
tabControl.pack(expand=1, fill="both")

# Adjust size
root.geometry("400x400")

# set minimum window size value
root.minsize(500, 500)

# set maximum window size value
root.maxsize(500, 500)

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
    f = open("encrypted", "wb")
    f.write(out)
    f.close()
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
keyf = Entry(file_frame)
keyf.grid(row=5, column=1)


def encryptFile():
    global out
    f = open(fname, "rb")
    bin = f.read()
    f.close()
    k = keyf.get()
    out = RC4.encrypt(bin, k)
    if (len(fname.split(".")) > 1):
        f = open("{}-encrypted.{}".format(fname.split(".")
                 [0], fname.split(".")[1]), "wb")
        f.write(out)
        f.close()
    else:
        f = open("{}-encrypted".format(fname), "wb")
        f.write(out)
        f.close()
    output.insert(END, out)


def decryptFile():
    global out
    f = open(fname, "rb")
    bin = f.read()
    f.close()
    k = keyf.get()
    out = RC4.decrypt(bin, k)
    if (len(fname.split(".")) > 1):
        f = open("{}-decrypted.{}".format(fname.split(".")
                 [0], fname.split(".")[1]), "wb")
        f.write(out)
        f.close()
    else:
        f = open("{}-decrypted".format(fname), "wb")
        f.write(out)
        f.close()
    output.insert(END, out)


encf_bt = Button(file_frame, text="Encrypt", command=encryptFile)
encf_bt.grid(row=6, column=0)
decf_bt = Button(file_frame, text="Decrypt", command=decryptFile)
decf_bt.grid(row=6, column=1)
output = Text(file_frame)
output.grid(row=7, column=0, columnspan=10)


def on_field_changeRC4(index, value, op):
    if (typebox.get() == "Text"):
        print("text")
        raise_frame(text_frame)
    elif (typebox.get() == "File"):
        print("file")
        raise_frame(file_frame)
    else:
        print("error")


# RC4
# label
ttk.Label(tab1, text="Select Type:",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=2)

# Combobox creation
v = StringVar()
v.trace('w', on_field_changeRC4)
typebox = ttk.Combobox(tab1, width=27, state="readonly", textvariable=v)

# Adding combobox drop down list
typebox['values'] = ('Text', 'File')

typebox.grid(column=1, row=2, columnspan=2)
typebox.current(0)


textStego_frame = ttk.Frame(tab2)
textStego_frame.grid(row=4, column=0, sticky='news', columnspan=20)
file_label = Label(
    textStego_frame, text="File").grid(row=2, column=0)
file = Button(textStego_frame, text="Browse", command=load_file, width=10)
file.grid(row=2, column=1, sticky=W)
textStego_label = Label(
    textStego_frame, text="Text").grid(row=4, column=0)
textStego = Entry(textStego_frame)
textStego.grid(row=4, column=1)
var1T = IntVar()
Checkbutton(textStego_frame, text="Encrypt",
            variable=var1T).grid(row=0, sticky=W)
var2T = IntVar()
Checkbutton(textStego_frame, text="Randomize",
            variable=var2T).grid(row=1, sticky=W)
key_label = Label(
    textStego_frame, text="Key").grid(row=5, column=0)
keyST = Entry(textStego_frame)
keyST.grid(row=5, column=1)
seed_label = Label(
    textStego_frame, text="Seed").grid(row=6, column=0)
seedInT = Entry(textStego_frame)
seedInT.grid(row=6, column=1)

fileStego_frame = ttk.Frame(tab2)
fileStego_frame.grid(row=4, column=0, sticky='news', columnspan=20)
file_label = Label(
    fileStego_frame, text="File").grid(row=2, column=0)
file = Button(fileStego_frame, text="Browse", command=load_file, width=10)
file.grid(row=2, column=1, sticky=W)
fileStego_label = Label(
    fileStego_frame, text="File Embedded").grid(row=4, column=0)
fileStego = Button(fileStego_frame, text="Browse",
                   command=load_fileS, width=10)
fileStego.grid(row=4, column=1, sticky=W)
var1F = IntVar()
Checkbutton(fileStego_frame, text="Encrypt",
            variable=var1F).grid(row=0, sticky=W)
var2F = IntVar()
Checkbutton(fileStego_frame, text="Randomize",
            variable=var2F).grid(row=1, sticky=W)
key_label = Label(
    fileStego_frame, text="Key").grid(row=5, column=0)
keySF = Entry(fileStego_frame)
keySF.grid(row=5, column=1)
seed_label = Label(
    fileStego_frame, text="Seed").grid(row=6, column=0)
seedInF = Entry(fileStego_frame)
seedInF.grid(row=6, column=1)


def on_field_changeStego(index, value, op):
    if (typebox1.get() == "Text"):
        print("text")
        raise_frame(textStego_frame)
    elif (typebox1.get() == "File"):
        print("file")
        raise_frame(fileStego_frame)
    else:
        print("error")


# Steganografi
# label
ttk.Label(tab2, text="Select Type:",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=2)

# Combobox creation
s = StringVar()
s.trace('w', on_field_changeStego)
typebox1 = ttk.Combobox(tab2, width=27, state="readonly", textvariable=s)

# Adding combobox drop down list
typebox1['values'] = ('Text', 'File')

# label
ttk.Label(tab2, text="Select File Type:",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=2)

# Combobox creation
a = StringVar()
typebox2 = ttk.Combobox(tab2, width=27, state="readonly", textvariable=a)

# Adding combobox drop down list
typebox2['values'] = ('Image', 'Audio')

# label
ttk.Label(tab3, text="Select File Type:",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=2)

# Combobox creation
c = StringVar()
typebox3 = ttk.Combobox(tab3, width=27, state="readonly", textvariable=c)

# Adding combobox drop down list
typebox3['values'] = ('Image', 'Audio')


def cal():
    outputP.delete('1.0', END)
    if (typebox3.get() == "Image"):
        im = Image.open(fname)
        data_a = b"".join([byte.to_bytes(1, sys.byteorder)
                           for pixel in list(im.getdata()) for byte in pixel])
        im2 = Image.open(fnameS)
        data_b = b"".join([byte.to_bytes(1, sys.byteorder)
                           for pixel in list(im2.getdata()) for byte in pixel])
        print("PSNR:", psnr(data_a, data_b, im.size, 255))
        outputP.insert(END, psnr(data_a, data_b, im.size, 255))
    else:
        print("=====PSNR Audio=====")
        wavpath_a = fname
        wav_a = wave.open(wavpath_a, "rb")
        wav_data_a = wav_a.readframes(wav_a.getnframes())
        size = (wav_a.getsampwidth() * wav_a.getnchannels(), wav_a.getnframes())
        wav_a.close()

        wavpath_b = fnameS
        wav_b = wave.open(wavpath_b, "rb")
        wav_data_b = wav_b.readframes(wav_b.getnframes())
        wav_b.close()
        outputP.insert(END, psnr(wav_data_a, wav_data_b, size, 255))

        print("PSNR:", psnr(wav_data_a, wav_data_b, size, 255))


typebox3.grid(column=1, row=2, columnspan=2)
typebox3.current(0)
file_label = Label(
    tab3, text="File A").grid(row=3, column=0)
file = Button(tab3, text="Browse", command=load_file, width=10)
file.grid(row=3, column=1, sticky=W)
fileStego_label = Label(
    tab3, text="File B").grid(row=4, column=0)
fileStego = Button(tab3, text="Browse",
                   command=load_fileS, width=10)
fileStego.grid(row=4, column=1, sticky=W)
cal_bt = Button(tab2, text="Calculate", command=cal)
cal_bt.grid(row=5, column=0)
outputP = Text(tab3)
outputP.grid(row=6, column=0, columnspan=10)


def insert():
    if (typebox1.get() == "Text"):
        txt = textStego.get()
        seed = 0
        if (var1T.get()):
            k = keyST.get()
            txt = RC4.encrypt(txt.encode("utf-8"), k)
        if (var2T.get()):
            seed = int(seedInT.get())
        if (typebox2.get() == "Image"):
            if (fname.split(".")[-1] == "bmp"):
                img_path = fname
                file_img = open(img_path, 'rb')
                img_byte = file_img.read()
                file_img.close()
                data_header = img_byte[0:54]
                img_data = img_byte[54:]
                text_in = txt
                if (not(var1T.get())):
                    text_bin = text_in.encode("utf-8")
                else:
                    text_bin = text_in
                max_cap = len(img_data) // 8 - 4
                if len(text_bin) < max_cap:
                    print("===== Inserting =====")
                    print("BMP File:", img_path)
                    print("Inserted Text:", text_in)
                    print("Max capacity:", max_cap, "bytes")
                    print("Inserted Text:", len(text_bin), "bytes")
                    insert_out = imgStego.insert(img_data, text_bin, seed)
                    out_path = "{}_out.bmp".format(fname.split(".")[0])
                    img_out = open(out_path, "wb")
                    img_out.write(data_header + insert_out)
                    print("Output IMG:", out_path)
                else:
                    print("Text reached maximum size")
                    print("aborting...")
            else:
                img_path = fname
                img = PIL.Image.open(img_path)
                out_data = b"".join([byte.to_bytes(1, sys.byteorder)
                                    for pixel in list(img.getdata()) for byte in pixel])
                text_in = txt
                if (not(var1T.get())):
                    text_bin = text_in.encode("utf-8")
                else:
                    text_bin = text_in
                max_cap = len(out_data) // 8 - 4
                if len(text_bin) < max_cap:
                    print("===== Inserting =====")
                    print("PNG File:", img_path)
                    print("Inserted Text:", text_in)
                    print("Max capacity:", max_cap, "bytes")
                    print("Inserted Text:", len(text_bin), "bytes")

                    insert_out = imgStego.insert(out_data, text_bin, seed)

                    out_path = "{}_out.png".format(fname.split(".")[0])
                    img_out = PIL.Image.frombytes(
                        img.mode, img.size, insert_out)
                    img_out.save(out_path)
                    print("Output IMG:", out_path)
                else:
                    print("Text reached maximum size")
                    print("aborting...")
        elif (typebox2.get() == "Audio"):
            wavpath = fname
            text_in = txt
            if (not(var1T.get())):
                text_bin = text_in.encode("utf-8")
            else:
                text_bin = text_in
            wav_in = wave.open(wavpath, "rb")
            max_cap = wav_in.getnframes() * wav_in.getnchannels() // 8 - 4

            if len(text_bin) < max_cap:
                insert_out = WavStego.insert(wav_in, text_bin, seed)

                out_path = "{}_out.wav".format(fname.split(".")[0])
                wav_out = wave.open(out_path, "wb")
                wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(insert_out)

                print("Output WAV:", out_path)
            else:
                print("Text reached maximum size")
                print("aborting...")
        else:
            return
    else:
        f = open(fnameS, "rb")
        bin = f.read()
        f.close()
        seed = 0
        if (var1F.get()):
            k = keyST.get()
            bin = RC4.encrypt(bin, k)
        if (var2F.get()):
            seed = int(seedInF.get())

        if (typebox2.get() == "Image"):
            if (fname.split(".")[-1] == "bmp"):
                img_path = fname
                file_img = open(img_path, 'rb')
                img_byte = file_img.read()
                file_img.close()
                data_header = img_byte[0:54]
                img_data = img_byte[54:]

                max_cap = len(img_data) // 8 - 4
                if len(bin) < max_cap:
                    print("===== Inserting =====")
                    print("BMP File:", img_path)
                    print("Max capacity:", max_cap, "bytes")
                    print("Inserted Text:", len(bin), "bytes")
                    insert_out = imgStego.insert(img_data, bin, seed)
                    out_path = "{}_out!{}.bmp".format(
                        fname.split(".")[0], fnameS.split(".")[-1])
                    img_out = open(out_path, "wb")
                    img_out.write(data_header + insert_out)
                    print("Output IMG:", out_path)
                else:
                    print("Text reached maximum size")
                    print("aborting...")
            else:
                img_path = fname
                img = PIL.Image.open(img_path)
                out_data = b"".join([byte.to_bytes(1, sys.byteorder)
                                    for pixel in list(img.getdata()) for byte in pixel])
                max_cap = len(out_data) // 8 - 4
                if len(bin) < max_cap:
                    print("===== Inserting =====")
                    print("PNG File:", img_path)
                    print("Max capacity:", max_cap, "bytes")
                    print("Inserted Text:", len(bin), "bytes")

                    insert_out = imgStego.insert(out_data, bin, seed)

                    out_path = "{}_out!{}.png".format(
                        fname.split(".")[0], fnameS.split(".")[-1])
                    img_out = PIL.Image.frombytes(
                        img.mode, img.size, insert_out)
                    img_out.save(out_path)
                    print("Output IMG:", out_path)
                else:
                    print("Text reached maximum size")
                    print("aborting...")
        elif (typebox2.get() == "Audio"):
            wavpath = fname
            wav_in = wave.open(wavpath, "rb")
            max_cap = wav_in.getnframes() * wav_in.getnchannels() // 8 - 4

            if len(bin) < max_cap:
                insert_out = WavStego.insert(wav_in, bin, seed)
                print("===== Inserting =====")
                print("PNG File:", wavpath)
                print("Max capacity:", max_cap, "bytes")
                print("Inserted Text:", len(bin), "bytes")
                out_path = "{}_out!{}.wav".format(
                    fname.split(".")[0], fnameS.split(".")[-1])
                wav_out = wave.open(out_path, "wb")
                wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(insert_out)

                print("Output WAV:", out_path)
            else:
                print("Text reached maximum size")
                print("aborting...")
        else:
            return


output = Text(tab2)
output.grid(row=7, column=0, columnspan=10)


def extract():
    output.delete('1.0', END)
    if (typebox1.get() == "Text"):
        if (typebox2.get() == "Image"):
            if (fname.split(".")[-1] == "bmp"):
                print("=====EXTRACTING=====")
                print("IMG File:", fname)

                file_img = open(fname, 'rb')
                img_byte = file_img.read()
                file_img.close()
                data_header = img_byte[0:54]
                img_data = img_byte[54:]

                extract_out = imgStego.extract(img_data)
                if (var1T.get()):
                    k = keyST.get()
                    extract_out = RC4.decrypt(extract_out, k)
                print("Extracted Text:", extract_out.decode("utf-8"))
                output.insert(END, extract_out.decode("utf-8"))
            else:
                out_path = fname
                print("=====EXTRACTING=====")
                print("IMG File:", out_path)

                img = PIL.Image.open(out_path)
                out_data = b"".join([byte.to_bytes(1, sys.byteorder)
                                    for pixel in list(img.getdata()) for byte in pixel])

                extract_out = imgStego.extract(out_data)
                if (var1T.get()):
                    k = keyST.get()
                    extract_out = RC4.decrypt(extract_out, k)
                print("Extracted Text:", extract_out.decode("utf-8"))
                output.insert(END, extract_out.decode("utf-8"))
        elif (typebox2.get() == "Audio"):
            print("=====EXTRACTING=====")
            print("WAV File:", fname)

            wav_out = wave.open(fname, "rb")
            extract_out = WavStego.extract(wav_out)

            # print(extract_out)
            if (var1T.get()):
                k = keyST.get()
                extract_out = RC4.decrypt(extract_out, k)
            print("Extracted Text:", extract_out.decode("utf-8"))
            output.insert(END, extract_out.decode("utf-8"))
        else:
            return
    else:
        if (typebox2.get() == "Image"):
            if (fname.split(".")[-1] == "bmp"):
                img_path = fname
                file_img = open(img_path, 'rb')
                img_byte = file_img.read()
                file_img.close()
                data_header = img_byte[0:54]
                img_data = img_byte[54:]

                extract_out = imgStego.extract(img_data)
                if (var1F.get()):
                    k = keyST.get()
                    extract_out = RC4.decrypt(extract_out, k)
                out_path = "extracted-stego.{}".format(
                    fname.split("!")[1].split(".")[0])
                file_out = open(out_path, "wb")
                file_out.write(extract_out)
                file_out.close()

                print("Extracted File:", out_path)
            else:
                out_path = fname
                print("=====EXTRACTING=====")
                print("IMG File:", out_path)

                img = PIL.Image.open(out_path)
                out_data = b"".join([byte.to_bytes(1, sys.byteorder)
                                    for pixel in list(img.getdata()) for byte in pixel])

                extract_out = imgStego.extract(out_data)
                if (var1F.get()):
                    k = keyST.get()
                    extract_out = RC4.decrypt(extract_out, k)
                out_path = "extracted-stego.{}".format(
                    fname.split("!")[1].split(".")[0])
                file_out = open(out_path, "wb")
                file_out.write(extract_out)
                file_out.close()

                print("Extracted File:", out_path)
        elif (typebox2.get() == "Audio"):
            print("=====EXTRACTING=====")
            print("WAV File:", fname)

            wav_out = wave.open(fname, "rb")
            extract_out = WavStego.extract(wav_out)

            # print(extract_out)
            if (var1F.get()):
                k = keyST.get()
                extract_out = RC4.decrypt(extract_out, k)
            out_path = "extracted-stego.{}".format(
                fname.split("!")[1].split(".")[0])
            file_out = open(out_path, "wb")
            file_out.write(extract_out)
            file_out.close()

            print("Extracted File:", out_path)
        else:
            return


typebox1.grid(column=1, row=2, columnspan=2)
typebox1.current(0)
typebox2.grid(column=1, row=3, columnspan=2)
typebox2.current(0)
insert_bt = Button(tab2, text="Insert", command=insert)
insert_bt.grid(row=6, column=0)
extract_bt = Button(tab2, text="Extract", command=extract)
extract_bt.grid(row=6, column=1)

root.mainloop()
