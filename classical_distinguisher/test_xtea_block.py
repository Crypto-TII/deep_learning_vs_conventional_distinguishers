from tea_block import *


for i in range(10):
    m = random_message()
    k = random_key()
    print("k             = ", end='')
    print_array(k)
    print("")

    print("m             = ", end='')
    print_array(m)
    print("")
    
    c = xtea_encrypt_block(m, k, verb=False)
    print("c = XTEA(m,k) = ", end='')
    print_array(c)
    print("")

    m1 = xtea_decrypt_block(c, k, verb=False)
    print("XTEA^-1(c,k)  = ", end='')
    print_array(m1)
    print("")
    print("XTEST TEA^-1(c,k) ?== m: " + str(m1 == m) + "\n")
    

print("TEST VECTORS test:\n")
# from https://github.com/froydnj/ironclad/blob/master/testing/test-vectors/xtea.testvec

k = [0x80000000, 0x00000000, 0x00000000, 0x00000000]
m = [0x00000000, 0x00000000]
expected_c = [0x057e8c05, 0x50151937]
print("k             = ", end='')
print_array(k)
print("")

print("m             = ", end='')
print_array(m)
print("")

c = xtea_encrypt_block(m, k, verb=False)
print("c = XTEA(m,k) = ", end='')
print_array(c)
print("")
print("XTEA(m,k) ?== expected_c: " + str(c == expected_c) + "\n")

k = [0x2BD6459F, 0x82C5B300, 0x952C4910, 0x4881FF48]
m = [0xEA024714, 0xAD5C4D84]
expected_c = [0x67b41e0a, 0xa05f593a]
print("k             = ", end='')
print_array(k)
print("")

print("m             = ", end='')
print_array(m)
print("")

c = xtea_encrypt_block(m, k, verb=False)
print("c = XTEA(m,k) = ", end='')
print_array(c)
print("")
print("XTEA(m,k) ?== expected_c: " + str(c == expected_c) + "\n")

