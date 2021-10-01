import math


def image_psnr(data_a, data_b, size):
    err = 0
    for i in range(size[0] * size[1]):
        err += (data_a[i] - data_b[i]) ** 2

    err = err / (size[0] * size[1])
    mse = 1/255 if math.sqrt(err) == 0 else math.sqrt(err)
    out = 20 * math.log10(255/mse)
    return out
