import math


def psnr(data_a, data_b, size, maxval):
    err = 0
    for i in range(size[0] * size[1]):
        err += (data_a[i] - data_b[i]) ** 2

    err = err / (size[0] * size[1])
    mse = 1/maxval if math.sqrt(err) == 0 else math.sqrt(err)
    out = 20 * math.log10(maxval/mse)
    return out
