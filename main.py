import wave
import os
from rc4 import RC4
from wav_stego import WavStego
from img_stego import imgStego, is_grey_scale

# file
filepath = "./yoyo.gif"
key = "yoyo"
split_filepath = os.path.splitext(filepath)

file_in = open(filepath, "rb")
plainbin = file_in.read()
file_in.close()

print("===== ENCRYPTING =====")
print("File:", filepath)
print("Key:", key)

cipherbin = RC4.encrypt(plainbin, key)

out_path = "{}-encrypt{}".format(
    split_filepath[len(split_filepath) - 2], split_filepath[-1])
file_out = open(out_path, "wb")
file_out.write(cipherbin)
file_out.close()

print("Output:", out_path)

file_in = open(out_path, "rb")
cipherbin = file_in.read()
file_in.close()

print("===== DECRYPTING =====")
print("File:", out_path)
print("Key:", key)

decipherbin = RC4.decrypt(cipherbin, key)

out_path = "{}-decrypt{}".format(
    split_filepath[len(split_filepath) - 2], split_filepath[-1])
file_out = open(out_path, "wb")
file_out.write(decipherbin)
file_out.close()

print("Output:", out_path)
print()

# text
plaintext = "dcoderc4"
plainbin = plaintext.encode("utf-8")
key = "yoyo"

print("===== ENCRYPTING =====")
print("Text:", plaintext)
print("Key:", key)

cipherbin = RC4.encrypt(plainbin, key)
decipherbin = RC4.decrypt(cipherbin, key)

deciphertext = decipherbin.decode("utf-8")

print("Plaintext:", plaintext)
print("Cipherbin:", cipherbin)
print("Deciphertext:", deciphertext)
print()

# file
wavpath = "./Ensoniq-ZR-76-06-BreakBt-90.wav"
filepath = "./yoyo.gif"
split_filepath = os.path.splitext(filepath)

wav_in = wave.open(wavpath, "rb")
file_in = open(filepath, "rb")
file_bin = file_in.read()
file_in.close()
max_cap = wav_in.getnframes() * wav_in.getnchannels() // 8 - 4

print("===== Inserting =====")
print("WAV File:", wavpath)
print("Inserted File:", filepath)
print("Max capacity:", max_cap, "bytes")
print("Inserted Data:", len(file_bin))

if len(file_bin) < max_cap:
    insert_out = WavStego.insert(wav_in, file_bin)

    out_path = "wav_out.wav"
    wav_out = wave.open(out_path, "wb")
    wav_out.setparams(wav_in.getparams())
    wav_out.writeframes(insert_out)

    print("Output WAV:", out_path)

    print("=====EXTRACTING=====")
    print("WAV File:", out_path)

    wav_out = wave.open(out_path, "rb")
    extract_out = WavStego.extract(wav_out)

    out_path = "{}-stego{}".format(
        split_filepath[len(split_filepath) - 2], split_filepath[-1])
    file_out = open(out_path, "wb")
    file_out.write(extract_out)
    file_out.close()

    print("Extracted File:", out_path)

else:
    print("Data file reached maximum size")
    print("aborting...")
print()

# text
wavpath = "./Ensoniq-ZR-76-06-BreakBt-90.wav"
text_in = "every summertime"
text_bin = text_in.encode("utf-8")

wav_in = wave.open(wavpath, "rb")
max_cap = wav_in.getnframes() * wav_in.getnchannels() // 8 - 4

print("===== Inserting =====")
print("WAV File:", wavpath)
print("Inserted Text:", text_in)
print("Max capacity:", max_cap, "bytes")
print("Inserted Text:", len(text_bin))

if len(text_bin) < max_cap:
    insert_out = WavStego.insert(wav_in, text_bin, 2)

    out_path = "wav_out.wav"
    wav_out = wave.open(out_path, "wb")
    wav_out.setparams(wav_in.getparams())
    wav_out.writeframes(insert_out)

    print("Output WAV:", out_path)

    print("=====EXTRACTING=====")
    print("WAV File:", out_path)

    wav_out = wave.open(out_path, "rb")
    extract_out = WavStego.extract(wav_out)

    # print(extract_out)
    print("Extracted Text:", extract_out.decode("utf-8"))


else:
    print("Text reached maximum size")
    print("aborting...")

# text
img_path = "./gray.bmp"
text_in = "ini gambar"
text_bin = text_in.encode("utf-8")

print("===== Inserting =====")
print("BMP File:", img_path)
print("Inserted Text:", text_in)
print("Inserted Text:", len(text_bin))

insert_out = imgStego.insert(img_path, text_bin, 2)

out_path = "gray_out.bmp"
img_out = open(out_path, "wb")
img_out.write(insert_out)
print("Output IMG:", out_path)

print("=====EXTRACTING=====")
print("IMG File:", out_path)

extract_out = imgStego.extract(out_path)

# print(extract_out)
print("Extracted Text:", extract_out.decode("utf-8"))
print()

# file
img_path = "./gray.bmp"
filepath = "./kucing.png"
split_filepath = os.path.splitext(filepath)

file_in = open(filepath, "rb")
file_bin = file_in.read()
file_in.close()

print("===== Inserting =====")
print("IMG File:", img_path)
print("Inserted File:", filepath)
print("Inserted Data:", len(file_bin))

insert_out = imgStego.insert(img_path, file_bin)

out_path = "gray_out.bmp"
img_out = open(out_path, "wb")
img_out.write(insert_out)

print("Output IMG:", out_path)

print("=====EXTRACTING=====")
print("IMG File:", out_path)

extract_out = imgStego.extract(out_path)

out_path = "{}-stego{}".format(
    split_filepath[len(split_filepath) - 2], split_filepath[-1])
file_out = open(out_path, "wb")
file_out.write(extract_out)
file_out.close()

print("Extracted File:", out_path)
print()
