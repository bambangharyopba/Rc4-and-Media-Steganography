import sys


class RC4:
    def encrypt(plainbin, key):
        N = 256
        S = [i for i in range(N)]

        def getBit(byte, pos):
            return byte & (1 << pos)

        j = 0
        for i in range(N):
            j = (j + S[i] + ord(key[i % len(key)])) % 256
            S[i], S[j] = S[j], S[i]

        i = 0
        j = 0
        cipherbin = bytes()
        for p in plainbin:
            i = (i + 1) % N
            j = (j + S[i]) % N

            # LSFR
            S[i] = (S[i] >> 1) | 128 if getBit(
                S[i], 0) ^ getBit(S[i], 4) else S[i] >> 1
            S[j] = (S[j] >> 1) | 128 if getBit(
                S[j], 0) ^ getBit(S[j], 4) else S[j] >> 1

            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % N
            u = S[t]
            c = u ^ p
            cipherbin += c.to_bytes(1, sys.byteorder)

        return cipherbin

    def decrypt(cipherbin, key):
        N = 256
        S = [i for i in range(N)]

        def getBit(byte, pos):
            return byte & (1 << pos)

        j = 0
        for i in range(N):
            j = (j + S[i] + ord(key[i % len(key)])) % N
            S[i], S[j] = S[j], S[i]

        i = 0
        j = 0
        plainbin = bytes()
        for c in cipherbin:
            i = (i + 1) % N
            j = (j + S[i]) % N

            # LSFR
            S[i] = (S[i] >> 1) | 128 if getBit(
                S[i], 0) ^ getBit(S[i], 4) else S[i] >> 1
            S[j] = (S[j] >> 1) | 128 if getBit(
                S[j], 0) ^ getBit(S[j], 4) else S[j] >> 1

            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % N
            u = S[t]
            p = u ^ c
            plainbin += p.to_bytes(1, sys.byteorder)

        return plainbin
