# from calculate_constant import calculate_const
import pickle

def rot_right(x, n):
    return (x >> n) | (x << (32 - n))
    # return (x >> n)

def shift_right(x, n):
    """Realiza uma operação de deslocamento bit a bit para a direita (shift right) em um número binário."""
    return (x & 0xffffffff) >> n

def sha256(message):
    # K = calculate_const(64, 3) # Carrega as Constantes K
    # H = calculate_const(8, 2) # Carrega as Constantes H

    k1 = open('constants.pkl', 'rb')
    h1 = open('hashes.pkl', 'rb')

    K = pickle.load(k1)
    H = pickle.load(h1)

    k1.close()
    h1.close()

    h0 = H[0]
    h1 = H[1]
    h2 = H[2]
    h3 = H[3]
    h4 = H[4]
    h5 = H[5]
    h6 = H[6]
    h7 = H[7]
    
    message = bytearray(message, 'utf-8')
    ml = len(message) * 8
    message.append(0x80)
    while (len(message) * 8) % 512 != 448:
        message.append(0x00)
    message += ml.to_bytes(8, byteorder='big')


    total_words = []

    for i in range(0, len(message), 64):
        words = [int.from_bytes(message[i+j:i+j+4], byteorder='big') for j in range(0, 64, 4)]
        for j in range(16, 64):
            s0 = rot_right(words[j-15], 7) ^ rot_right(words[j-15], 18) ^ shift_right(words[j-15], 3)
            s1 = rot_right(words[j-2], 17) ^ rot_right(words[j-2], 19) ^ shift_right(words[j-2], 10)
            words.append((words[j-16] + s0 + words[j-7] + s1) & 0xffffffff)
            total_words.append(words) 

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        total_blocks = []

        for j in range(64):
            s0 = rot_right(a, 2) ^ rot_right(a, 13) ^ rot_right(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = s0 + maj
            s1 = rot_right(e, 6) ^ rot_right(e, 11) ^ rot_right(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = h + s1 + ch + K[j] + words[j]

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff
            total_blocks.append([a, b, c, d, e, f, g, h])

        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff

    hash = '{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3, h4, h5, h6, h7)

    return hash

if __name__ == '__main__':
    message = input("Enter a message to get the SHA-256 hash: ")
    message_hash = sha256(message)
    print("Hash:", message_hash)