from tea_block import *
import math

# VERIFY DIFFERENTIAL TRAIL PROBABILITIES

number_of_rounds = 3

k = [0xE15C838, 0xDC8DBE76, 0xB3BB0110, 0xFFBB0440]

alpha = [0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000]
beta  = [0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010]

round_differences = [[0x00000000,0x00000000] for i in range(number_of_rounds)]

round_differences = [[0x00000000,0x00000000] for i in range(len(alpha)+1)]
round_differences[0] = [0x00000000, 0x80402010]
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

for i in range(len(round_differences)):
    print("round " + str(i) + ": ", end='')
    print_array(round_differences[i])
    print("")

num_samples = 100
messages = [random_message() for i in range(num_samples)]
# messages_plus_difference = [[0,0] for i in range(num_samples)]


counter_left = [0 for i in range(number_of_rounds)]
counter_right = [0 for i in range(number_of_rounds)]
counter_both = [0 for i in range(number_of_rounds)]

for r in range(0,number_of_rounds):

    i = 0
    for m in messages:
        m1 = [xor(m[0],round_differences[0][0]), xor(m[1],round_differences[0][1])]
        # d = [xor(m1[0],m[0]),xor(m1[1],m[1])]

        # double check input differences

        # if ((xor(m1[0],m[0]) == round_differences[r][0]) and (xor(m1[1],m[1]) == round_differences[r][1])):
        #     counter_left[r] = counter_left[r] + 1

        print("r = " + str(r) + ": message number = " + str(i) + ": ", end='')
        # print(" | (m,m1,d) = "),
        # print_array(m)
        # print(" - "),
        # print_array(m1)
        # print(" - "),
        # print_array(d)

        c  = xtea_encrypt_block(m , k, nrounds=r)
        c1 = xtea_encrypt_block(m1, k, nrounds=r)
        d = [xor(c1[0],c[0]),xor(c1[1],c[1])]


        print(" | (c,c1,d) = ", end='')
        print_array(c)
        print(" - ", end='')
        print_array(c1)
        print(" - ", end='')
        print_array(d)
        print("")

        # if ((xor(c1[0],c[0]) == round_differences[r][0]) and (xor(c1[1],c[1]) == round_differences[r][1])):
        if ((xor(c1[0],c[0]) == round_differences[r][0])):
            counter_left[r] = counter_left[r] + 1
        if ((xor(c1[1],c[1]) == round_differences[r][1])):
            counter_right[r] = counter_right[r] + 1
        if ((xor(c1[0],c[0]) == round_differences[r][0]) and (xor(c1[1],c[1]) == round_differences[r][1])):
            counter_both[r] = counter_both[r] + 1
        
        i = i + 1

print(counter_left)

for r in range(0, number_of_rounds):
    print("r = " + str(r))
    print("  counter_left   = " + str(counter_left[r]))
    print("  counter_right  = " + str(counter_right[r]))
    print("  counter_both   = " + str(counter_both[r]))
    print("  #samples = " + str(num_samples))
    print("  heuristic probability = " + str(float(counter_both[r])/float(num_samples)), end='')
    if counter_both[r] != 0:
        print(" = 2^" + str(math.log(float(counter_both[r])/float(num_samples),2)))
    else:
        print(" = 0")



