from tea_block import *
import time

# INPUT:
# - k: key
# - alpha -> beta: input/output difference of the F function at each round
# - expected_probability: probability that the difference alpha propagates to beta through the function F, for each round


CIPHER = "TEA"
# CIPHER = "XTEA"
# CIPHER = "RAIDEN"

if CIPHER == "XTEA":

    encrypt_block = xtea_encrypt_block
    cipher_add = xor
    cipher_sub = xor

    number_of_rounds = 4

    key = [0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3]

    alpha = [0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000]
    beta  = [0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010, 0x80402010, 0x00000000, 0x80402010]

    # -log_2(p)
    expected_probability = [4.61, 3.01, 5.48, 3.30, 3.01, 5.35, 5.36, 2.99, 5.45, 5.42, 2.99, 5.38, 5.40, 2.99]


if CIPHER == "TEA":

    encrypt_block = tea_encrypt_block
    cipher_add = add
    cipher_sub = sub

    number_of_rounds = 3

    key = [0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3]
    
    alpha = [0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x0000000F, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0xFFFFFFF1, 0x00000001, 0x00000000, 0x00000001, 0xFFFFFFF1, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x00000011, 0xFFFFFFFF, 0x00000000]
    beta  = [0x0000000F, 0x00000000, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0x00000000, 0xFFFFFFF1, 0x00000002, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0xFFFFFFFE, 0x0000000F, 0x00000000, 0x00000011, 0x00000000, 0xFFFFFFEF, 0x00000000]
    
    # -log_2(p)
    expected_probability = [3.62, 0.0, 2.87, 7.90, 3.60, 0.0, 2.78, 8.66, 3.57, 0.0, 2.87, 7.90, 3.59, 0.0, 2.79, 8.83, 3.61, 0.0]
    

if CIPHER == "RAIDEN":

    encrypt_block = raiden_encrypt_block
    cipher_add = add
    cipher_sub = sub

    number_of_rounds = 6

    key = random_key() #[0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3]
    
    trail_length = 32+1
    alpha = [0 for i in range(trail_length)]
    beta  = [0 for i in range(trail_length)]
    expected_probability = [0.0 for i in range(trail_length)]

    for i in range(0, trail_length, 3):
        alpha[i  ] = 0x00000000
        alpha[i+1] = 0x7FFFFF00
        alpha[i+2] = 0x7FFFFF00
        beta[i  ]  = 0x00000000
        beta[i+1]  = 0x7FFFFF00
        beta[i+2]  = 0x80000100
        # -log_2(p)
        expected_probability[i  ] = 0.0
        expected_probability[i+1] = 2.0
        expected_probability[i+2] = 2.0

    # alpha = [0x00000000, 0x7FFFFF00, 0x7FFFFF00, 0x00000000, 0x7FFFFF00, 0x7FFFFF00, 0x00000000, 0x7FFFFF00, 0x7FFFFF00, 0x00000000, 0x7FFFFF00, 0x7FFFFF00, 0x00000000, 0x7FFFFF00, 0x7FFFFF00]
    # beta  = [0x00000000, 0x7FFFFF00, 0x80000100, 0x00000000, 0x7FFFFF00, 0x80000100, 0x00000000, 0x7FFFFF00, 0x80000100, 0x00000000, 0x7FFFFF00, 0x80000100, 0x00000000, 0x7FFFFF00, 0x80000100]
    
    # # -log_2(p)
    # expected_probability = [0.0, 2.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 2.0]
    



# print("\nComputing round differences...\n")
round_differences = compute_round_differences(alpha, beta)
print_round_differences(round_differences, alpha, beta)


# print("\nComputing heuristic and expected probability...\n")
start = time.time()

output = compute_heuristic_and_expected_probability(encrypt_block, key, number_of_rounds, round_differences, expected_probability, verb=False)
heuristic_probabilities            = output[0]
accumulated_expected_probability = output[1]
counters                         = output[2]
num_samples                      = output[3]

end = time.time()

# print_round_differences_latex_table(round_differences, alpha, beta, accumulated_expected_probability)

print(counters[0])
print(counters[1])
print(counters[2])
print(heuristic_probabilities[0])
print(heuristic_probabilities[1])
print(heuristic_probabilities[2])

# print("\nPrinting heuristic and expected probability...\n")
print_heuristic_vs_expected_probability(heuristic_probabilities, accumulated_expected_probability, counters, num_samples, number_of_rounds)

print("\nTime: {:05.2f} [sec]\n".format(end-start))


