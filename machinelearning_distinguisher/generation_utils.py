import numpy as np

def get_int64():
    return (np.random.randint(0,2**63) << 1) + np.random.randint(0, 2)

def add_mod(v1, v2, mod = 2**32):
    return (v1+v2)%mod

def encrypt_tea(plain, key, rounds):
    v1, v0 = plain & 0xFFFFFFFF, plain >> 32
    k3, k2, k1, k0 = key & 0xFFFFFFFF, (key >> 32) & 0xFFFFFFFF, (key >> 64) & 0xFFFFFFFF, (key >> 96) & 0xFFFFFFFF
    delta = 0x9E3779B9
    sum = 0
    for i in range(rounds):
        if i%2 == 0:
            sum = add_mod(sum, delta)
            v0 = add_mod(v0,(add_mod((v1<<4),k0)) ^ add_mod(v1, sum) ^ add_mod((v1>>5), k1))
        else:
            v1 = add_mod(v1, add_mod((v0<<4), k2) ^ add_mod(v0, sum) ^ add_mod((v0>>5), k3))
    return add_mod((v0 << 32), v1, 2**64)

def encrypt_raiden(plain, key, rounds):
    v1, v0 = plain & 0xFFFFFFFF, plain >> 32
    k = [key & 0xFFFFFFFF, (key >> 32) & 0xFFFFFFFF, (key >> 64) & 0xFFFFFFFF, (key >> 96) & 0xFFFFFFFF][::-1]
    sk = 0
    for i in range(rounds):
        if i%2 == 0:
            k[i%4]= add_mod(add_mod(k[0], k[1]), (add_mod(k[2], k[3])^(k[0]*pow(2,k[2],2**32))))
            sk = k[i%4]
            v0 = add_mod(v0, (add_mod(sk, v1) << 9) ^ (add_mod(sk,-v1) ^ (add_mod(sk,v1) >> 14)))
        else:
            v1 = add_mod(v1, (add_mod(sk, v0) << 9) ^ (add_mod(sk,-v0) ^ (add_mod(sk,v0) >> 14)))
    return add_mod((v0 << 32), v1, 2**64)

def generate_sample(sample_size, delta, cipher, fixed_key, rounds):
    y = np.random.randint(0, 2, sample_size)
    data = []
    if cipher == "TEA":
        encrypt = encrypt_tea
    else:
        encrypt = encrypt_raiden
    for i in range(sample_size):
        if y[i] == 0:
            data.append([get_int64(), get_int64()])
        else:
            if fixed_key == -1:
                key = get_int64() << 64 | get_int64()
            else:
                key = fixed_key
            p1 = get_int64()
            if cipher == "XTEA":
                p2 = (p1^delta) % 2**64
            else:
                p2 = add_mod(p1, delta, 2**64)
            data.append([encrypt(p1, key, rounds), encrypt(p2, key, rounds)])
    return np.array(to_binary(data)), np.array(to_onehot(y))

def generate_sample_same_output(sample_size, delta, cipher, fixed_key, rounds, output):
    data = []
    if output == 0:
        for i in range(sample_size):
            data.append([get_int64(), get_int64()])
    else:
        if cipher == "TEA":
            encrypt = encrypt_tea
        else:
            encrypt = encrypt_raiden

        for i in range(sample_size):
            if fixed_key == -1:
                key = get_int64() << 64 | get_int64()
            else:
                key = fixed_key
            p1 = get_int64()
            p2 = add_mod(p1, delta, 2**64)
            data.append([encrypt(p1, key, rounds), encrypt(p2, key, rounds)])
    return np.array(to_binary(data)), output

def generate_diff_sample(sample_size, delta, cipher, fixed_key, rounds):
    y = np.random.randint(0, 2, sample_size)
    data = []
    if cipher == "TEA":
        encrypt = encrypt_tea
    else:
        encrypt = encrypt_raiden
    for i in range(sample_size):
        if y[i] == 0:
            data.append([get_int64(), 0])
        else:
            if fixed_key == -1:
                key = get_int64() << 64 | get_int64()
            else:
                key = fixed_key
            p1 = get_int64()
            p2 = add_mod(p1, delta, 2**64)
            diff = (encrypt(p1, key, rounds) - encrypt(p2, key, rounds)) % 2**64
            data.append([diff, 0])
    return np.array(to_binary(data, words_number = 1)), np.array(to_onehot(y))

def generate_diff_sample_same_output(sample_size, delta, cipher, fixed_key, rounds, output):
    data = []
    if output == 0:
        for i in range(sample_size):
            data.append([get_int64(), 0])
    else:
        if cipher == "TEA":
            encrypt = encrypt_tea
        else:
            encrypt = encrypt_raiden

        for i in range(sample_size):
            if fixed_key == -1:
                key = get_int64() << 64 | get_int64()
            else:
                key = fixed_key
            p1 = get_int64()
            p2 = add_mod(p1, delta, 2**64)
            diff = (encrypt(p1, key, rounds) - encrypt(p2, key, rounds)) % 2**64
            data.append([diff, 0])
    return np.array(to_binary(data, words_number = 1)), output

def to_binary(data, l = 64, words_number = 2):
    v = []
    for c in data:
        b = bin(c[0]+2**l*c[1])[2:].rjust(words_number*l,'0')
        vv = [int(x)*2-1 for x in b]
        v.append(vv)
    return v

def to_onehot(data):
    v = []
    for c in data:
        b = [0, 0]
        b[c] = 1
        v.append(b)
    return v
