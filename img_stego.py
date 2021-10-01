from PIL import Image
import sys
import random


def is_grey_scale(img_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            if r != g != b:
                return False
    return True


print()


class imgStego:
    def insert(img_data, data, seed=0):

        if seed < 0 or seed > 255:
            return

        def getBit(data, byte_pointer, bit_pointer):
            return (data[byte_pointer] >> bit_pointer) & 1
        data_byte_pointer = 0
        data_bit_pointer = 0

        queue = []
        if seed != 0:
            random.seed(seed)
            queue = random.sample([i for i in range(8)], 8)

        data_modified = seed.to_bytes(
            1, sys.byteorder) + data + b"EOD"  # end of data
        output_data = bytes()
        insert_seed = False
        for i, byte in enumerate(img_data):
            if not insert_seed:
                data_bit = getBit(
                    data_modified, data_byte_pointer, 7 - data_bit_pointer)
                output_data += ((byte & (~1)) |
                                data_bit).to_bytes(1, sys.byteorder)
                data_bit_pointer += 1
                if data_bit_pointer >= 8:
                    data_bit_pointer = 0
                    data_byte_pointer += 1
                    insert_seed = True

            elif data_byte_pointer < len(data_modified):
                data_bit = getBit(
                    data_modified, data_byte_pointer, 7 - data_bit_pointer if seed == 0 else queue[data_bit_pointer])
                output_data += ((byte & (~1)) |
                                data_bit).to_bytes(1, sys.byteorder)
                data_bit_pointer += 1
                if data_bit_pointer >= 8:
                    data_bit_pointer = 0
                    data_byte_pointer += 1
                    if seed != 0:
                        queue = random.sample([i for i in range(8)], 8)
            else:
                data_pointer = i
                break

        return output_data + img_data[data_pointer:]

    def extract(img_data):

        def getBit(data, byte_pointer, bit_pointer):
            return (data[byte_pointer] >> bit_pointer) & 1

        data = bytes()
        data_byte = 0
        data_bit_pointer = 0
        eod = [False, False, False]
        get_seed = False
        for byte in img_data:
            data_bit = getBit([byte], 0, 0)
            data_byte = data_byte | data_bit
            data_byte = data_byte << 1
            data_bit_pointer += 1

            if data_bit_pointer >= 8:
                data_byte = data_byte >> 1
                data_bit_pointer = 0

                if not get_seed:
                    seed = data_byte
                    data_byte = 0
                    random.seed(seed)
                    get_seed = True

                # EOD CHECKER
                else:
                    if seed != 0:
                        queue = random.sample([i for i in range(8)], 8)
                        new_data_byte = 0
                        for i, q in enumerate(queue):
                            bit = getBit([data_byte], 0, 7 - i)
                            new_data_byte = new_data_byte | (bit << q)
                        data_byte = new_data_byte

                    if data_byte == ord("E"):
                        eod[0] = True
                    elif eod[0] and not eod[1] and data_byte == ord("O"):
                        eod[1] = True
                    elif eod[0] and eod[1] and data_byte == ord("D"):
                        eod[2] = True
                    else:
                        eod[0] = False
                        eod[1] = False

                    data_byte = data_byte.to_bytes(1, sys.byteorder)
                    data += data_byte
                    data_byte = 0

            if eod[0] and eod[1] and eod[2]:
                break

        return data[:len(data) - 3]
