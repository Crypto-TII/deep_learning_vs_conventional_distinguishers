from tea_block import *


for i in range(10):
    m = random_message()
    k = random_key()
    print("k            = "),
    print_array(k)
    print("")

    print("m            = "),
    print_array(m)
    print("")
    
    c = tea_encrypt_block(m,k,verb=False)
    print("c = TEA(m,k) = "),
    print_array(c)
    print("")

    m1 = tea_decrypt_block(c,k,verb=False)
    print("TEA^-1(c,k)  = "),
    print_array(m1)
    print("")
    print("TEST TEA^-1(c,k) ?== m: " + str(m1 == m) + "\n")
    


m = [0x0,0x0]
k = [0x0,0x0,0x0,0x0]
print("m        = "),
print_array(m)
print("")
print("k        = "),
print_array(k)
print("")
c = tea_encrypt_block(m,k)
print("TEA(m,k) = "),
print_array(c)
print("")

print("TEST: " + str(c[0] == 0x41ea3a0a and c[1] == 0x94baa940))


m = [0x75697263, 0x6c677270]
k = [0x70666f71, 0x756a6e62, 0x636a6762, 0x7366626d]
print("k        = "),
print_array(k)
print("")
print("m        = "),
print_array(m)
print("")
c = tea_encrypt_block(m,k)
print("TEA(m,k) = "),
print_array(c)
print("")

print("TEST: " + str(c[0] == 0xa8863faf and c[1] == 0x276c565d ))


m = random_message()
k = random_key()
print("k          = "),
print_array(k)
print("")
print("m          = "),
print_array(m)
print("")
for i in range(10):
    c = tea_encrypt_block(m,k,nrounds=i)
    print("TEA(m,k," + str(i) + ") = "),
    print_array(c)
    print("")

# m = random_message()
# k = random_key()
print("k          = "),
print_array(k)
print("")
print("m          = "),
print_array(m)
print("")
c = tea_encrypt_block(m,k,nrounds=ROUNDS,verb=False)
print("TEA(m,k," + str(ROUNDS) + ") = "),
print_array(c)
print("")

