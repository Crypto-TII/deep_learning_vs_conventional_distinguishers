import time
from tea_block import *

w1 =random_word()
w2 =random_word()

start = time.time()
c = add(w1,w2)
end = time.time()
print("Time add():    ", end='')
print(end - start)

start = time.time()
c = xor(w1,w2)
end = time.time()
print("Time xor():    ", end='')
print(end - start)

start = time.time()
c = w1 << w2
end = time.time()
print("Time <<:    ", end='')
print(end - start)


b = random_word()
k0 = random_word()
k1 = random_word()
d = random_word()

start = time.time()
c = tea_F_function(b, k0, k1, d)
end = time.time()
print("Time tea_F_function():    ", end='')
print(end - start)


b = random_word()
k = random_word()
d = random_word()

start = time.time()
c = xtea_F_function(b, k, d)
end = time.time()
print("Time xtea_F_function():   ", end='')
print(end - start)


b = random_word()
k = random_word()

start = time.time()
c = raiden_F_function(b, k)
end = time.time()
print("Time raiden_F_function(): ", end='')
print(end - start)


k = random_key()

start = time.time()
round_k = raiden_key_schedule_one_round(k)
end = time.time()
print("Time raiden key schedule() [one rounds key]: ", end='')
print(end - start)

start = time.time()
round_keys = raiden_key_schedule(k)
end = time.time()
print("Time raiden_key_schedule(): ", end='')
print(end - start)


m = random_message()
k = random_key()

start = time.time()
c = tea_encrypt_block(m, k, verb=False)
end = time.time()
print("Time tea_encrypt_block():    ", end='')
print(end - start)

start = time.time()
c = xtea_encrypt_block(m, k, verb=False)
end = time.time()
print("Time xtea_encrypt_block():   ", end='')
print(end - start)

start = time.time()
c = raiden_encrypt_block(m, k, verb=False)
end = time.time()
print("Time raiden_encrypt_block(): ", end='')
print(end - start)