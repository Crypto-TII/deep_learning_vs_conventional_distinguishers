from classical_distinguisher import *
import time

# define cipher

CIPHER = "TEA"
# CIPHER = "XTEA"
# CIPHER = "RAIDEN"

if (CIPHER == "XTEA"):
    # TODO
    print(CIPHER)

if (CIPHER == "TEA"):

    alpha = [0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x0000000F, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0xFFFFFFF1, 0x00000001, 0x00000000, 0x00000001, 0xFFFFFFF1, 0xFFFFFFFF, 0x00000000, 0xFFFFFFFF, 0x00000011, 0xFFFFFFFF, 0x00000000]
    beta  = [0x0000000F, 0x00000000, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0x00000000, 0xFFFFFFF1, 0x00000002, 0x0000000F, 0x00000000, 0xFFFFFFF1, 0xFFFFFFFE, 0x0000000F, 0x00000000, 0x00000011, 0x00000000, 0xFFFFFFEF, 0x00000000]
    
    # -log_2(p)
    expected_probability = [3.62, 0.0, 2.87, 7.90, 3.60, 0.0, 2.78, 8.66, 3.57, 0.0, 2.87, 7.90, 3.59, 0.0, 2.79, 8.83, 3.61, 0.0]

    cipher = {
    "name":"TEA",
    "cipher_encrypt_block":tea_encrypt_block,
    "number_of_attacked_rounds":4,
    "cipher_add64": add64,
    "cipher_sub64": sub64,
    "round_differences": compute_round_differences(alpha, beta),
    "accumulated_expected_probability":[sum(expected_probability[0:i]) for i in range(0,len(expected_probability))],
    "key": [0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3]
    }

if (CIPHER == "RAIDEN"):

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

    # round_differences = compute_round_differences(alpha, beta)

    trail_len = len(expected_probability)

    key = random_key()

    cipher = {
    "name":"RAIDEN",
    "cipher_encrypt_block":raiden_encrypt_block,
    "number_of_attacked_rounds":6,
    "cipher_add64": add64,
    "cipher_sub64": sub64,
    "round_differences": compute_round_differences(alpha, beta),
    "accumulated_expected_probability":[sum(expected_probability[0:i]) for i in range(0,trail_len)],
    "key": random_key()
    }

# define number of sample

max_num_samples = 100000000 # increase/decrease if the testing device can manage more/less
num_samples = int(math.ceil(2**cipher["accumulated_expected_probability"][cipher["number_of_attacked_rounds"]]))
num_samples = min(num_samples, max_num_samples)

print("\nCipher                            = " + CIPHER + "\n")
print("key                               = {}".format(cipher["key"]))
print("number of attacked rounds         = {}".format(cipher["number_of_attacked_rounds"]))
exp = cipher["accumulated_expected_probability"][cipher["number_of_attacked_rounds"]]
print("distinguisher success probability = 1/2^{} = {}".format(exp, 1 / float(2 ** exp)))
# print("accumulated expected probability = {}".format(accumulated_expected_probability))
print("input difference                  = {}".format(cipher["round_differences"][0]))
print("round difference                  = {}".format(cipher["round_differences"][cipher["number_of_attacked_rounds"]]))
exp = cipher["accumulated_expected_probability"][cipher["number_of_attacked_rounds"]]
print("number of samples                 = 2^{} = {}".format(exp, num_samples))


number_of_experiments = 10


# time estimation

start = time.time()

m1 = random_message()
m2 = cipher["cipher_add64"](m1,cipher["round_differences"][0])
c1 = cipher["cipher_encrypt_block"](m1, cipher["key"], nrounds=cipher["number_of_attacked_rounds"])
c2 = cipher["cipher_encrypt_block"](m2, cipher["key"], nrounds=cipher["number_of_attacked_rounds"])

end = time.time()

print("\nEstimated time to generate {} cipher output pairs: {:05.2f} [seconds]".format(num_samples, num_samples*(end-start)))
print("\nEstimated time to run      {} experiments:         {:05.2f} [seconds]".format(number_of_experiments, number_of_experiments*num_samples*(end-start)))




# test differential distinguisher

start = time.time()
results = test_differential_distinguisher(number_of_experiments, cipher, num_samples, verb=False)
end = time.time()

print("\nSUMMARY:")
print("--------\n")

print("ACCURACY when distinguishing real cipher:        {}/{}".format(results[0][0], results[0][1]))
print("ACCURACY when distinguishing random permutation: {}/{}".format(results[1][0], results[1][1]))
print("TOTAL ACCURACY:                                  {}/{}".format(results[0][0] + results[1][0], number_of_experiments))

print("\nTime: {:05.2f} [sec]\n".format(end-start))

