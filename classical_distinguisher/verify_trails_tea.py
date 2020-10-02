from tea_block import *
import math

# VERIFY DIFFERENTIAL TRAIL PROBABILITIES

def compute_round_differences(alpha, beta):
    round_differences = [[0x00000000,0x00000000] for i in range(len(alpha)+1)]
    # round_differences[0] = [0xFFFFFFF1, 0xFFFFFFFF]
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

def print_round_differences(round_differences):
    print("\nInput/Output differences:")
    print("\n             LEFT    RIGHT")
    for i in range(len(round_differences)):
        print("round %2d: " % (i), end='')
        print_array(round_differences[i])
        print("")



def compute_heuristic_and_expected_probability(number_of_rounds, round_differences, expected_probability, verb=True):
    trail_len = len(expected_probability)
    accumulated_expected_probability = [sum(expected_probability[0:i]) for i in range(0,trail_len)]
    heuristic_probability    = [0 for i in range(0,trail_len)]

    # define number of sample
    max_num_samples = 100000000 # increase/decrease if the testing device can manage more/less
    num_samples = int(math.ceil(2**accumulated_expected_probability[number_of_rounds]))

    num_samples = min(num_samples, max_num_samples)
    if verb:
        print("For " + str(number_of_rounds) + " rounds, " + str(num_samples) + " are needed")
        print("Taking " + str(num_samples) + " samples")

    # create input message set
    messages = [random_message() for i in range(num_samples)]


    #set counters
    counter_left  = [0 for i in range(trail_len)]
    counter_right = [0 for i in range(trail_len)]
    counter_both  = [0 for i in range(trail_len)]

    # start counting for each round and for each message
    for r in range(0,number_of_rounds):
        for m in messages:
            m1 = [add(m[0],round_differences[0][0]), add(m[1],round_differences[0][1])]

            c  = tea_encrypt_block(m , k, nrounds=r)
            c1 = tea_encrypt_block(m1, k, nrounds=r)
            d = [sub(c1[0],c[0]),sub(c1[1],c[1])]

            if verb:
                print("r = " + str(r) + ": message number = " + str(i) + ": ", end='')
                print(" | (c,c1,d) = ", end='')
                print_array(c)
                print(" - ", end='')
                print_array(c1)
                print(" - ", end='')
                print_array(d)
                print("")

            if ((sub(c1[0],c[0]) == round_differences[r][0])):
                counter_left[r] = counter_left[r] + 1
            if ((sub(c1[1],c[1]) == round_differences[r][1])):
                counter_right[r] = counter_right[r] + 1
            if ((sub(c1[0],c[0]) == round_differences[r][0]) and (sub(c1[1],c[1]) == round_differences[r][1])):
                counter_both[r] = counter_both[r] + 1
        
        heuristic_probability[r] = float(counter_both[r])/float(num_samples)

    return [heuristic_probability, accumulated_expected_probability, \
            [counter_both, counter_left, counter_right], num_samples]

def print_heuristic_vs_expected_probability(heuristic_probability, accumulated_expected_probability, counters, num_samples):
    print("\n#samples = " + str(num_samples))
    print("\n          Heur.Pr  - Exp.Pr. - Counters")
    for r in range(0, len(heuristic_probability)):
        print("r = %2d - " % (r), end='')

        # heuristic probability
        if heuristic_probability[r] != 0:
            print("2^{:06.2f}".format(round(math.log(heuristic_probability[r],2),2)), end='')
        else:
            print("NA      ", end='')
  
        print(" - ", end='')

        # accumulated expected probability
        if (r == 0):
            print("2^ 0    ", end='')
        else:
            print("2^-{:05.2f}".format(round(accumulated_expected_probability[r],2)), end='')

        print(" - [" + str(counters[0][r]) + ", " + str(counters[1][r]) + ", " + str(counters[1][r]) + "]")


# INPUT:
# - k: key
# - alpha -> beta: input/output difference of the F function at each round
# - expected_probability: probability that the difference alpha propagates to beta through the function F, for each round

k = [0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3]

alpha = [0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x0000000F, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0xFFFFFFF1, 0x00000001, 0x00000000, 0x00000001, 0xFFFFFFF1, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x00000011, 0xFFFFFFFF, 0x00000000]
beta  = [0x0000000F, 0x00000000, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0x00000000, 0xFFFFFFF1, 0x00000002, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0xFFFFFFFE, 0x0000000F, 0x00000000, 0x00000011, 0x00000000, 0xFFFFFFEF, 0x00000000]

expected_probability = [3.62, 0.0, 2.87, 7.90, 3.60, 0.0, 2.78, 8.66, 3.57, 0.0, 2.87, 7.90, 3.59, 0.0, 2.79, 8.83, 3.61, 0.0]

number_of_rounds = 3




round_differences = compute_round_differences(alpha, beta)
print_round_differences(round_differences)

output = compute_heuristic_and_expected_probability(number_of_rounds, round_differences, expected_probability, verb=False)
heuristic_probability            = output[0]
accumulated_expected_probability = output[1]
counters                         = output[2]
num_samples                      = output[3]
print_heuristic_vs_expected_probability(heuristic_probability, accumulated_expected_probability, counters, num_samples)



