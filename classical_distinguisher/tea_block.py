#!/usr/bin/env python
"""
Python implementation of 
- Tiny Encryption Algorithm (TEA)
- XTEA
- RAIDEN
- function to compute the differential trail (round differences) 
  given the input-output difference pair of the F function
- functions to print the differential trail
- functions that computes the probability of the trail heuritically
- function to print the heuristic probability

Block size: 64bits
Key size: 128bits
"""

from ctypes import c_uint32, c_uint64
import numpy as np
from copy import copy 
import math


# Constants
ROUNDS = 64

WORD_BIT_SIZE = 32
WORD_HEX_SIZE = WORD_BIT_SIZE//4
BLOCK_UINT32_SIZE = 2
BLOCK_BYTE_SIZE = BLOCK_UINT32_SIZE*WORD_BIT_SIZE//8
KEY_UINT32_SIZE = 4
KEY_BYTE_SIZE = KEY_UINT32_SIZE*WORD_BIT_SIZE//8

BLOCK_BIT_SIZE = 64



#
#  Helpers for c_uint32 math
#
    
def change_bit(vector, position):
    if position >= BLOCK_BIT_SIZE:
        print("ERROR: position greater than block size.")
        return 0
    return vector ^ (0x1 << position)

def split_block(vector):
    return [c_uint32(vector >> WORD_BIT_SIZE).value, c_uint32(vector & 0xFFFFFFFF).value]

def join_blocks(b):
    return c_uint64(b[0] << WORD_BIT_SIZE ^ b[1]).value

def hamming_weight(vector):
    weight = 0
    for i in range(BLOCK_BIT_SIZE):
        weight = weight + ((vector >> i) & 0x1)
    return weight

def raiden_lshift(a, s):
    """ Left shift s """
    shift = min(s, WORD_BIT_SIZE)
    return c_uint32(a << shift).value

def lshift(a, s):
    """ Left shift s """
    return c_uint32(a << s).value

def rshift(a, s):
    """ Right shift s """
    return c_uint32(a >> s).value

def lshift_add(a, b, s):
    """ Left shift s and add b """
    result = lshift(a,s) + c_uint32(b).value
    return c_uint32(result).value

def rshift_add(a, b, s):
    """ Right shift s and add b """
    result = rshift(a, s) + c_uint32(b).value
    return c_uint32(result).value

def add(a, b):
    """ Add a and b """
    result = c_uint32(a).value + c_uint32(b).value
    return c_uint32(result).value

def add64(a, b):
    """ Add a and b, where a,b contains two 32 bit words """
    result = [add(a[0],b[0]), add(a[1],b[1])]
    return result

def sub(a, b):
    """ Subract a and b """
    result = c_uint32(a).value - c_uint32(b).value
    return c_uint32(result).value

def sub64(a, b):
    """ Subract a and b """
    result = [sub(a[0],b[0]), sub(a[1],b[1])]
    return result

def xor(a, b):
    """ XOR a, b """
    return c_uint32(a).value ^ c_uint32(b).value

def xor3(a, b, c):
    """ XOR a, b, and c """
    middle = c_uint32(a).value ^ c_uint32(b).value
    return c_uint32(middle ^ c_uint32(c).value).value

def bitwise_and(a, b):
    """ AND a, b """
    return c_uint32(a).value & c_uint32(b).value

def print_block(vector):
    print("{0:016x} ".format(vector), end='')
    # print("{0:016x} ".format(v))
    
def print_word(w):
    print("{0:0{1}x} ".format(w, WORD_HEX_SIZE), end='')
    
def print_array(v):
    # print( str(hex(v[0])) + " " + str(hex(v[1])))
    for x in v:
        # print("{}".format(hex(int(x))[2:].rjust(WORD_HEX_SIZE,'0')))
        print("{0:0{1}x} ".format(x, WORD_HEX_SIZE), end='')
        # print("{0:#0{1}x}".format(x,WORD_HEX_SIZE)), # to print with 0x

def print_array2(v):
    print( str(hex(v[0]))[2:WORD_HEX_SIZE+2] + " " + str(hex(v[1]))[2:WORD_HEX_SIZE+2] )


def random_word():
    return np.random.randint(0,2**WORD_BIT_SIZE)

def random_message():
    return [np.random.randint(0,2**WORD_BIT_SIZE) for i in range(BLOCK_UINT32_SIZE)]

def random_key():
    return [np.random.randint(0,2**WORD_BIT_SIZE) for i in range(KEY_UINT32_SIZE)]

def random_permutation():
    return random_message()

def random_permutation_encrypt_block(input_block=0, input_key=0, nrounds=0):
    return random_message()

def tea_F_function(block, k0, k1, delta_i):
    left_shift = 4
    right_shift = 5
    return xor3(
                lshift_add(block, k0, left_shift),
                add(block, delta_i),
                rshift_add(block, k1, right_shift)
            )

def tea_encrypt_block(input_block, input_key, starting_round=0, nrounds=ROUNDS, verb=False):
    """
    Encrypt a single 64-bit block using a given key
    @param block: list of two c_uint32s
    @param key: list of four c_uint32s
    """
    block = copy(input_block)
    key = copy(input_key)
    assert len(block) == BLOCK_UINT32_SIZE
    assert len(key) == KEY_UINT32_SIZE
    summation = 0x0
    delta = 0x9e3779b9
    for i in range(starting_round, starting_round+nrounds):
        if verb:
            print("round: " + str(i))
            print("input: "),
            print_array(block)
            print("")
            # print("input:  b[0] = " + str(block[0]) + " - b[1] = " + str(block[1]))
        if ((i % 2) == 0 ):
            summation = c_uint32(summation + delta).value
            tmp = tea_F_function(block[1],key[0],key[1],summation)
            block[0] = add( block[0], tmp)
        else:
            tmp = tea_F_function(block[0],key[2],key[3],summation)
            block[1] = add(block[1],tmp)
        if verb:
            print("input: "),
            print_array(block)
            print("")
            # print("output: b[0] = " + str(block[0]) + " - b[1] = " + str(block[1]))
    return block


def tea_decrypt_block(input_block, input_key, nrounds=ROUNDS, verb=False):
    """
    Decrypt a single 64-bit block using a given key
    @param block: list of two c_uint32s
    @param key: list of four c_uint32s
    """
    block = copy(input_block)
    key = copy(input_key)
    assert len(block) == BLOCK_UINT32_SIZE
    assert len(key) == KEY_UINT32_SIZE
    summation = (0x9e3779b9*((ROUNDS+1)//2)) % 2**WORD_BIT_SIZE # for 64 rounds: 0xc6ef3720
    delta = 0x9e3779b9
    for i in range(nrounds-1,-1,-1):

        if verb:
            print("round: " + str(i))
            print("input: "),
            print_array(block)
            print("")

        if ((i % 2) == 1 ):
            tmp = tea_F_function(block[0],key[2],key[3],summation)
            block[1] = sub( block[1], tmp)
        else:
            tmp = tea_F_function(block[1],key[0],key[1],summation)
            block[0] = sub( block[0], tmp)
            summation = c_uint32(summation - delta).value
        if verb:
            print("input: "),
            print_array(block)
            print("")
    return block

def xtea_F_function(block, key, delta_i):
    # (((b1 << 4) ^ (b1 >> 5)) + b1) ^ (delta_i + key);
    left_shift = 4
    right_shift = 5
    tmp = xor(lshift(block, left_shift),rshift(block, right_shift))
    tmp = add(tmp, block)
    return xor(tmp, add(delta_i, key))
    
def xtea_encrypt_block(input_block, input_key, starting_round=0, nrounds=ROUNDS, verb=False):
    """
    Encrypt a single 64-bit block using a given key
    @param block: list of two c_uint32s
    @param key: list of four c_uint32s
    """
    block = copy(input_block)
    key = copy(input_key)
    assert len(block) == BLOCK_UINT32_SIZE
    assert len(key) == KEY_UINT32_SIZE
    summation = 0x0
    delta = 0x9e3779b9
    for i in range(starting_round, starting_round+nrounds):

        if verb:
            print("round: " + str(i))
            print("input: "),
            print_array(block)
            print("")
            # print("input:  b[0] = " + str(block[0]) + " - b[1] = " + str(block[1]))
        
        if ((i % 2) == 0 ):
            round_key = key[bitwise_and(summation, 3)] # key[delta_i & 3]
            tmp = xtea_F_function(block[1], round_key, summation)
            block[0] = add( block[0], tmp)
            summation = c_uint32(summation + delta).value
        else:
            round_key = key[bitwise_and(rshift(summation, 11), 3)] # key[(sum>>11) & 3]
            tmp = xtea_F_function(block[0], round_key, summation)
            block[1] = add(block[1], tmp)

        if verb:
            print("input: "),
            print_array(block)
            print("")
            # print("output: b[0] = " + str(block[0]) + " - b[1] = " + str(block[1]))

    return block

def xtea_decrypt_block(input_block, input_key, nrounds=ROUNDS, verb=False):
    """
    Decrypt a single 64-bit block using a given key
    @param block: list of two c_uint32s
    @param key: list of four c_uint32s
    """
    block = copy(input_block)
    key = copy(input_key)
    assert len(block) == BLOCK_UINT32_SIZE
    assert len(key) == KEY_UINT32_SIZE
    summation = (0x9e3779b9*((ROUNDS+1)//2)) % 2**WORD_BIT_SIZE # for 64 rounds: 0xc6ef3720
    delta = 0x9e3779b9
    for i in range(nrounds-1,-1,-1):

        if verb:
            print("round: " + str(i))
            print("input: "),
            print_array(block)
            print("")

        if ((i % 2) == 1 ):
            round_key = key[bitwise_and(rshift(summation, 11), 3)] # key[(sum>>11) & 3]
            tmp = xtea_F_function(block[0], round_key, summation)
            block[1] = sub( block[1], tmp)
        else:
            summation = c_uint32(summation - delta).value
            round_key = key[bitwise_and(summation, 3)] # key[delta_i & 3]
            tmp = xtea_F_function(block[1], round_key, summation)
            block[0] = sub( block[0], tmp)
            
        if verb:
            print("input: "),
            print_array(block)
            print("")

    return block

def raiden_F_function(block, key):
    # ((k + x) << 9) ^ (k − x) ^ ((k + x) >> 14)

    # tmp1 = rshift(add(key,block),9)
    # tmp2 = sub(key, block)
    # tmp3 = lshift(add(key, block), 14)
    # return xor3(tmp1, tmp2, tmp3)

    tmp1 = lshift(add(key,block),9)
    tmp2 = sub(key, block)
    tmp3 = rshift(add(key, block), 14)
    return xor3(tmp1, tmp2, tmp3)

def raiden_key_schedule_one_round(key):
    tmp1 = add(key[0], key[1])
    tmp2 = add(key[2], key[3])
    tmp3 = raiden_lshift(key[0], key[2])
    # tmp3 = key[0] << key[2]
    tmp4 = xor( tmp2, tmp3)

    return add(tmp1, tmp4)

def raiden_key_schedule(key, nrounds=ROUNDS):
    round_keys = [0 for i in range(nrounds)]
    for i in range(nrounds):
        round_keys[i] = raiden_key_schedule_one_round

def raiden_encrypt_block(input_block, input_key, starting_round=0, nrounds=ROUNDS, verb=False):
    """
    Encrypt a single 64-bit block using a given key
    @param block: list of two c_uint32s
    @param key: list of four c_uint32s
    """
    block = copy(input_block)
    key = copy(input_key)
    assert len(block) == BLOCK_UINT32_SIZE
    assert len(key) == KEY_UINT32_SIZE
    for i in range(starting_round, starting_round+nrounds):

        if verb:
            print("round: " + str(i))
            print("input: "),
            print_array(block)
            print("")
            # print("input:  b[0] = " + str(block[0]) + " - b[1] = " + str(block[1]))

        if ((i % 2) == 0 ):
            # sk.       = k[i%4]=((k[0]+k[1])+((k[2]+k[3])^(k[0]<<k[2])));
            key[i%4] = raiden_key_schedule_one_round(key)
            # key[i%4] = add(( add(key[0], key[1])), xor( add(key[2], key[3]), ( key[0] << key[2] ) ) )
            round_key = key[i%4]
            tmp = raiden_F_function(block[1], round_key)
            block[0] = add( block[0], tmp)
        else:
            tmp = raiden_F_function(block[0], round_key)
            block[1] = add(block[1], tmp)

        if verb:
            print("input: "),
            print_array(block)
            print("")
            # print("output: b[0] = " + str(block[0]) + " - b[1] = " + str(block[1]))

    return block


# VERIFY DIFFERENTIAL TRAIL PROBABILITIES

def compute_round_differences(alpha, beta):
    round_differences = [[0x00000000,0x00000000] for i in range(len(alpha)+1)]
    round_differences[0] = [sub(alpha[1],beta[0]), alpha[0]]

    for i in range(len(alpha)):
        # print("i = " + str(i))
        if (((i+1) % 2) == 1):
            # print("LEFT  = round_differences[i][0], beta[i] = " + str(hex(round_differences[i][0])) + ", " + str(hex(beta[i])))
            # print("RIGHT = round_differences[i][1].         = " + str(hex(round_differences[i][1])) )
            left = add(round_differences[i][0], beta[i])
            right = round_differences[i][1]
        else:
            # print("RIGHT = round_differences[i][1], beta[i] = " + str(hex(round_differences[i][1])) + ", " + str(hex(beta[i])))
            # print("LEFT  = round_differences[i][0].         = " + str(hex(round_differences[i][0])) )
            right = add(round_differences[i][1], beta[i])
            left = round_differences[i][0]
        round_differences[i+1] = [left, right]

    return round_differences

def print_round_differences(round_differences, alpha, beta):
    print("\nInput/Output differences:")
    print("\n             LEFT    RIGHT       alpha   ->    beta")
    print("round  0: ", end='')
    print_array(round_differences[0])
    print(" | ", end='')
    print("")
    for i in range(1,len(round_differences)):
        print("round %2d: " % (i), end='')
        print_array(round_differences[i])
        print(" | ", end='')
        print("{0:0{1}x} ".format(alpha[i-1], WORD_HEX_SIZE), end='')
        print(" -> ", end='')
        print("{0:0{1}x} ".format(beta[i-1], WORD_HEX_SIZE), end='')
        print("")

def print_round_differences_latex_table(round_differences, alpha, beta, accumulated_expected_probability):
    print("\nInput/Output differences:")
    print("\n             LEFT    RIGHT       alpha   ->    beta")
    print(" 0 & \\texttt{ 0x", end='')
    print_word(round_differences[0][0])
    print("} & \\texttt{ 0x", end='')
    print_word(round_differences[0][1])
    # print_array(round_differences[0])
    print("} & - & - & - \\\\")
    for i in range(1,len(round_differences)):
        print("%2d & \\texttt{ 0x" % (i), end='')
        # print_array(round_differences[i])
        print_word(round_differences[i][0])
        print("} & \\texttt{ 0x", end='')
        print_word(round_differences[i][1])
        print("} & ", end='')
        print("\\texttt{{ 0x{0:0{1}x} }} ".format(alpha[i-1], WORD_HEX_SIZE), end='')
        print(" & ", end='')
        print("\\texttt{{ 0x{0:0{1}x} }}".format(beta[i-1], WORD_HEX_SIZE), end='')
        print(" & $2^{{- {:5.2f} }}$".format(round(accumulated_expected_probability[i],2)), end='')
        print(" \\\\")

def compute_heuristic_and_expected_probability(encrypt_block_algorithm, key, number_of_rounds, round_differences, expected_probability, verb=True):
    trail_len = len(expected_probability)
    accumulated_expected_probability = [sum(expected_probability[0:i]) for i in range(0,trail_len+1)]
    heuristic_probability_both       = [0 for i in range(0,trail_len)]
    heuristic_probability_left       = [0 for i in range(0,trail_len)]
    heuristic_probability_right      = [0 for i in range(0,trail_len)]

    # define number of sample

    max_num_samples = 100000000 # increase/decrease if the testing device can manage more/less
    num_samples = int(math.ceil(2**accumulated_expected_probability[number_of_rounds]))
    num_samples = min(num_samples, max_num_samples)

    # if verb:
    print("\nTesting {} rounds\n".format(number_of_rounds))
    print("For " + str(number_of_rounds) + " rounds, " + str(num_samples) + " are needed")
    print("Taking " + str(num_samples) + " samples")

    # create input message set

    messages = [random_message() for i in range(num_samples)]

    #set counters

    counter_left  = [0 for i in range(trail_len)]
    counter_right = [0 for i in range(trail_len)]
    counter_both  = [0 for i in range(trail_len)]

    # start counting for each round and for each message

    for r in range(0, number_of_rounds+1):
        for m in messages:
            m1 = add64(m,round_differences[0])

            c  = encrypt_block_algorithm(m , key, nrounds=r)
            c1 = encrypt_block_algorithm(m1, key, nrounds=r)
            d = sub64(c1, c)

            if verb:
                print("r = " + str(r+1) + ": message number = " + str(i) + ": ", end='')
                print(" | (c,c1,d) = ", end='')
                print_array(c)
                print(" - ", end='')
                print_array(c1)
                print(" - ", end='')
                print_array(d)
                print("")

            if (sub64(c1,c)      == round_differences[r]): # if ((sub(c1[0],c[0]) == round_differences[r][0]) and (sub(c1[1],c[1]) == round_differences[r][1])):
                counter_both[r]  = counter_both[r]  + 1

            if ((sub(c1[0],c[0]) == round_differences[r][0])):
                counter_left[r]  = counter_left[r]  + 1

            if ((sub(c1[1],c[1]) == round_differences[r][1])):
                counter_right[r] = counter_right[r] + 1

        
        heuristic_probability_both[r]  = float(counter_both[r]) /float(num_samples)
        heuristic_probability_left[r]  = float(counter_left[r]) /float(num_samples)
        heuristic_probability_right[r] = float(counter_right[r])/float(num_samples)

    return [[heuristic_probability_both, heuristic_probability_left, heuristic_probability_right], \
            accumulated_expected_probability, \
            [counter_both, counter_left, counter_right], \
            num_samples]

def print_heuristic_vs_expected_probability(heuristic_probabilities, accumulated_expected_probability, counters, num_samples, number_of_rounds):
    print("\n#samples = " + str(num_samples))
    print("\n           Heu.Pr -  Heu.Pr. -  Heu.Pr. - Exp.Pr. - Counters")
    print("           [both]    [left]     [right]                     \n")
    for r in range(0, len(heuristic_probabilities[0])):
        print("r = %2d - " % (r), end='')

        # heuristic probability

        # both
        if heuristic_probabilities[0][r] != 0:
            print("2^{:06.2f}".format(round(math.log(heuristic_probabilities[0][r],2),2)), end='')
        else:
            print("NA      ", end='')
  
        print(" - ", end='')

        # left
        if heuristic_probabilities[1][r] != 0:
            print("2^{:06.2f}".format(round(math.log(heuristic_probabilities[1][r],2),2)), end='')
        else:
            print("NA      ", end='')
  
        print(" - ", end='')

        # right
        if heuristic_probabilities[2][r] != 0:
            print("2^{:06.2f}".format(round(math.log(heuristic_probabilities[2][r],2),2)), end='')
        else:
            print("NA      ", end='')
  
        print(" - ", end='')

        # accumulated expected probability

        if (r == 0):
            print("2^ 0    ", end='')
        else:
            print("2^-{:05.2f}".format(round(accumulated_expected_probability[r],2)), end='')

        print(" - [" + str(counters[0][r]) + ", " + str(counters[1][r]) + ", " + str(counters[2][r]) + "]")

        if (r == number_of_rounds or r == 0):
            print("------------------------------------------------------------------------")

