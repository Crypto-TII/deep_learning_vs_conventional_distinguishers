from classical_distinguisher import *
import time

# define ciphers

# XTEA
  
# TODO
# CIPHERS.append(cipher)

CIPHERS = []

# TEA

alpha = [0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x0000000F, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0xFFFFFFF1, 0x00000001, 0x00000000, 0x00000001, 0xFFFFFFF1, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x00000011, 0xFFFFFFFF, 0x00000000]
beta  = [0x0000000F, 0x00000000, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0x00000000, 0xFFFFFFF1, 0x00000002, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0xFFFFFFFE, 0x0000000F, 0x00000000, 0x00000011, 0x00000000, 0xFFFFFFEF, 0x00000000]

# -log_2(p)
expected_probability = [3.62, 0.0, 2.87, 7.90, 3.60, 0.0, 2.78, 8.66, 3.57, 0.0, 2.87, 7.90, 3.59, 0.0, 2.79, 8.83, 3.61, 0.0]

round_differences = compute_round_differences(alpha, beta)
accumulated_expected_probabilities = [sum(expected_probability[0:i]) for i in range(0,len(expected_probability))]
r = 6

cipher = {
"name": "TEA",
"cipher_encrypt_block": tea_encrypt_block,
"number_of_attacked_rounds": r,
"key": [0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3],
"input_difference": round_differences[0],
"output_difference": round_differences[r],
"difference_probability": accumulated_expected_probabilities[r]
}

CIPHERS.append(cipher)

# RAIDEN

# cipher_encrypt_block = raiden_encrypt_block
# number_of_attacked_rounds = 7
# cipher_add64 = add64
# cipher_sub64 = sub64

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

round_differences = compute_round_differences(alpha, beta)
accumulated_expected_probabilities = [sum(expected_probability[0:i]) for i in range(0,len(expected_probability))]
r = 6

# round_differences = compute_round_differences(alpha, beta)

trail_len = len(expected_probability)

key = random_key()

cipher = {
"name":"RAIDEN",
"cipher_encrypt_block":raiden_encrypt_block,
"number_of_attacked_rounds":r,
"key": key,
"input_difference": round_differences[0],
"output_difference": round_differences[r],
"difference_probability": accumulated_expected_probabilities[r]
}

# CIPHERS.append(cipher)



# define number of sample

# max_num_samples = 100000000 # increase/decrease if the testing device can manage more/less
# num_samples = int(math.ceil(2**cipher["accumulated_expected_probability"][cipher["number_of_attacked_rounds"]]))
# num_samples = min(num_samples, max_num_samples)

DISTINGUISHERS = [\
    # ["Bitflip distinguisher", bitflip_distinguisher_variation],\
    ["Differential distinguisher", differential_distinguisher]\
    ]

number_of_experiments = 10

ACCURACY_RESULTS = []
for distinguisher in DISTINGUISHERS:
    print("\nDISTINGUISHER: {}".format(distinguisher[0]))
    for cipher in CIPHERS:
        print("\nCIPHER: {}".format(cipher["name"]))

        #set number of tested rounds
        # for number_of_rounds in range(7,9):
        for number_of_rounds in range(4,6):
            cipher["number_of_attacked_rounds"] = number_of_rounds
            
            print("rounds: {}".format(cipher["number_of_attacked_rounds"]))
            print("\n# samples | ACC REAL | ACC RAND | ACC TOT")
            accuracies = {
                "distinguisher":distinguisher[0],
                "cipher_name":cipher["name"],
                "cipher_rounds":cipher["number_of_attacked_rounds"],
                "number_of_samples":[],
                "total_accuracy": []
                }

            accuracy_reached_one = False

            # set number of samples
            # for i in range(12,21):
            for i in range(6,12):
                if (accuracy_reached_one == True):
                    print("Reached accuracy 1!")
                else:
                    num_samples = 2 ** i

                    # test distinguisher

                    start = time.time()
                    results = experiment(distinguisher[1], number_of_experiments, num_samples, cipher, verb=False)

                    accuracies["number_of_samples"].append(i)
                    accuracy = (results[0][0] + results[1][0])/float(number_of_experiments)
                    accuracies["total_accuracy"].append(accuracy )

                    end = time.time()

                if (accuracy >= 1):
                    accuracy_reached_one = True
                
                # print("\nTime: {:05.2f} [sec]\n".format(end-start))

                print("2^{}: {:05.4f} | {:05.4f} | {:05.4f} = {}/{}".format( \
                    i, results[0][0]/float(results[0][1]), \
                    results[1][0]/float(results[1][1]), \
                    (results[0][0] + results[1][0])/float(number_of_experiments), \
                    results[0][0] + results[1][0], \
                    number_of_experiments \
                    ))
                # print("\nTime: {:05.2f} [sec]\n".format(end-start))

            ACCURACY_RESULTS.append(accuracies)


colors = []

# for i in range(len(DISTINGUISHERS)):
#     for j in range(len(CIPHERS)):
#         for h in range(4,9):
#             color = str(hex((0xFF7F00 + 20*i) % 0x1000000))[2:8]
#             color_name = "color" + str(i) + "_" + str(j) + "_" + str(h)
#             colors.append(color_name)
#             print("\\definecolor{" + color_name + "}{HTML}{" + color + "}")

for i in range(32):
    color = str(hex((0xFF7F00 + 20*i) % 0x1000000))[2:8]
    color_name = "color" + str(i)
    colors.append(color_name)
    print("\\definecolor{" + color_name + "}{HTML}{" + color + "}")


print("\nLATEX 2D coordinates ( <log2(#samples)> , <Accuracy> )")

def select_color(cipher_name,distinguisher_name, r):
    if (cipher_name == "TEA"):
        c = str(0)
    if (cipher_name == "RAIDEN"):
        c = str(1)
    if (cipher_name == "XTEA"):
        c = str(2)
    if (distinguisher_name == "Bitflip distinguisher"):
        d = str(0)
    if (distinguisher_name == "Differential distinguisher"):
        d = str(1)
    return "color" + d + "_" + c + "_" + str(r)

color_counter = 0
for accuracies in ACCURACY_RESULTS:
    print("\n%")
    # print("\\addplot+[mark=x,color=" + select_color(accuracies["cipher_name"],accuracies["distinguisher"],accuracies["cipher_rounds"])+ "]")
    print("\\addplot+[mark=x]")
    print("coordinates {")
    for i in range(len(accuracies["total_accuracy"])):
        print("({:2}, {:03.2f}) ".format(accuracies["number_of_samples"][i],accuracies["total_accuracy"][i]), end='')
        if ((i) % 4) == 3:
            print("")
    print("};")
    print("\\addlegendentry{" + accuracies["distinguisher"] + " " + str(accuracies["cipher_name"]) + " " + str(accuracies["cipher_rounds"]) + "-rounds}")

    color_counter = (color_counter + 1) % len(colors)


print("\nLATEX 3D coordinates ( <log2(#samples)> , <Round>, <Accuracy> )")

color_counter = 0
for accuracies in ACCURACY_RESULTS:
    print("\n%")
    print("\\addplot3+[mark=x,color=" + colors[color_counter]+ "]")
    print("coordinates{")
    for i in range(len(accuracies["total_accuracy"])):
        print("({:2}, {:2}, {:03.2f}) ".format(accuracies["number_of_samples"][i],accuracies["cipher_rounds"],accuracies["total_accuracy"][i]), end='')
        if ((i) % 4) == 3:
            print("")
    print("};")
    print("\\addlegendentry{" + accuracies["distinguisher"] + " " + str(accuracies["cipher_name"]) + " " + str(accuracies["cipher_rounds"]) + "-rounds}")

    color_counter = (color_counter + 1) % len(colors)


