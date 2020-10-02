from diffusion import *


# test bit flip

print("\nTest vector bit flip:\n")

input = 0x0000000000000000

print_block(input)
print("")

output = change_bit(input, 0)
print_block(output)
print("")

print_block(change_bit(input, 1))
print("")

print_block(change_bit(input, 63))
print("")

print_block(change_bit(input, 64))
print("")

# test hamming weight

print("\nTest Hamming weight:\n")

v = 0xFFFFFFFFFFFFFFFF
print("weight = " + str(hamming_weight(v)))

v = 0xF0F0F0F0F0F0F0F0
print("weight = " + str(hamming_weight(v)))

v = 0x0000000000100000
print("weight = " + str(hamming_weight(v)))

v = 0x0000000000000000
print("weight = " + str(hamming_weight(v)))


# test split block

print("\nTest split block:\n")

v = 0xFFFFFFFFEEEEEEEE
print("vector.         = ", end='')
print_block(v)
print("")

b = split_block(v)
print("splitted vector = ", end='')
print_array(b)
print("")

c = join_blocks(b)
print("rejoined vector = ", end='')
print_block(c)
print("")



# diffusion test

print("\nBit flip diffusion test:\n")

NUMBER_OF_ROUNDS = 32
encrypt_block_functions = [["random permutation",random_permutation_encrypt_block],["TEA", tea_encrypt_block], ["XTEA", xtea_encrypt_block], ["RAIDEN", raiden_encrypt_block]]
# input = 0x0000000000000000
NUMBER_OF_INPUTS = 10
key = random_key()


for f in encrypt_block_functions:
    print("encryption function: " + f[0])
    encrypt_block_function = f[1]
    average_changed_bits_list = bit_flip_diffusion_test(encrypt_block_function, NUMBER_OF_ROUNDS, key, BLOCK_BIT_SIZE, NUMBER_OF_INPUTS)
    print_result_bit_flip_diffusion_test(average_changed_bits_list, BLOCK_BIT_SIZE)

