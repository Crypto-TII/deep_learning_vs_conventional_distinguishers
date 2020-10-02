from tea_block import *
import time

def generate_set_of_cipher_output_pairs(cipher_encrypt_block, key, number_of_attacked_rounds, cipher_add64, num_samples, input_difference):

    # generate input pair samples from known cipher

    input = []
    for i in range(num_samples):
        m = random_message()
        input.append([m,cipher_add64(m, input_difference)])

    # generate output pair samples from cipher

    cipher_output_pairs = []
    for i in range(num_samples):
        c1 = cipher_encrypt_block(input[i][0], key, nrounds=number_of_attacked_rounds)
        c2 = cipher_encrypt_block(input[i][1], key, nrounds=number_of_attacked_rounds)
        cipher_output_pairs.append([c1,c2])

    return cipher_output_pairs

def generate_set_of_random_output_pairs(num_samples):
    # generate output pair samples random permutation
    
    random_output_pairs = []
    for i in range(num_samples):
        c1 = random_permutation()
        c2 = random_permutation()
        random_output_pairs.append([c1,c2])

    return random_output_pairs

def bitflip_distinguisher(oracle, num_samples):
    """
    for num_samples messages, flips all bit positions
    returns 1 if the distinguisher believes oracle is a cipher
    returns 0 if the distinguisher believes oracle is a random permutation
    """
    oracle_encrypt_block = oracle["encrypt_block"]
    key = oracle["key"]
    r = oracle["number_of_rounds"]
    
    THRESHOLD = 1

    NUMBER_OF_TESTED_INPUTS = num_samples

    total_changed_bit = 0
    for j in range(NUMBER_OF_TESTED_INPUTS):

        input = join_blocks(random_message())
        for i in range(BLOCK_BIT_SIZE):
            in1 = split_block(input)
            in2 = split_block(change_bit(input, i))
            out1 = join_blocks(oracle_encrypt_block(in1, key, nrounds=r))
            out2 = join_blocks(oracle_encrypt_block(in2, key, nrounds=r))
            output = out1 ^ out2
            total_changed_bit = total_changed_bit + hamming_weight(output)


    average_changed_bits = total_changed_bit / float(BLOCK_BIT_SIZE*NUMBER_OF_TESTED_INPUTS)

    if ((average_changed_bits > (BLOCK_BIT_SIZE//2 - THRESHOLD)) and (average_changed_bits < (BLOCK_BIT_SIZE//2 + THRESHOLD))):
        return 0
    else:
        return 1

def bitflip_distinguisher_variation(oracle, num_samples):
    """
    selects num_samples (random messages, random bit position) pairs
    returns 1 if the distinguisher believes oracle is a cipher
    returns 0 if the distinguisher believes oracle is a random permutation
    """
    oracle_encrypt_block = oracle["encrypt_block"]
    key = oracle["key"]
    r = oracle["number_of_rounds"]
    
    THRESHOLD = 1

    NUMBER_OF_TESTED_INPUTS = 1

    total_changed_bit = 0

    for _ in range(num_samples):
        input = join_blocks(random_message())
        random_bit_position = np.random.randint(0,BLOCK_BIT_SIZE)
        in1 = split_block(input)
        in2 = split_block(change_bit(input, random_bit_position))
        out1 = join_blocks(oracle_encrypt_block(in1, key, nrounds=r))
        out2 = join_blocks(oracle_encrypt_block(in2, key, nrounds=r))
        output = out1 ^ out2
        total_changed_bit = total_changed_bit + hamming_weight(output)

    average_changed_bits = total_changed_bit / float(num_samples)

    if ((average_changed_bits > (BLOCK_BIT_SIZE//2 - THRESHOLD)) and (average_changed_bits < (BLOCK_BIT_SIZE//2 + THRESHOLD))):
        return 0
    else:
        return 1

def differential_distinguisher(oracle, num_samples):
    oracle_encrypt_block = oracle["encrypt_block"]
    key = oracle["key"]
    r = oracle["number_of_rounds"]
    input_difference = oracle["input_difference"]
    output_difference = oracle["output_difference"]
    difference_probability = oracle["difference_probability"]

    counter = 0
    for i in range(num_samples):
        m1 = random_message()
        m2 = add64(m1, input_difference) # additive difference
        c1 = oracle_encrypt_block(m1, key, nrounds=r)
        c2 = oracle_encrypt_block(m2, key, nrounds=r)

        if (sub(c2[0],c1[0]) == output_difference[0] or \
            sub(c2[1],c1[1]) == output_difference[1]):
            counter = counter + 1

    if (counter >= 1):
        # print("The output pair set comes from a known cipher")
        return 1
    else:
        # print("The output pair set comes from a random permutation")
        return 0

def differential_distinguisher_old(output_pairs, number_of_attacked_rounds, round_differences, accumulated_expected_probability):
    num_samples = len(output_pairs)
    counter = 0
    for i in range(num_samples):
        # if (sub64(output_pairs[i][1],output_pairs[i][0]) == round_differences[number_of_attacked_rounds]):
        if (sub(output_pairs[i][1][0],output_pairs[i][0][0]) == round_differences[number_of_attacked_rounds][0] or \
            sub(output_pairs[i][1][1],output_pairs[i][0][1]) == round_differences[number_of_attacked_rounds][1]):
            counter = counter + 1
    if (counter >= 1):
        # print("The output pair set comes from a known cipher")
        return [1, counter]
    else:
        # print("The output pair set comes from a random permutation")
        return [0, counter]



def experiment(distinguisher, number_of_experiments, num_samples, cipher, verb=True):
    start = time.time()

    number_of_experiments_with_cipher = number_of_experiments//2
    number_of_experiments_with_random_permutation = number_of_experiments//2

    oracle = {
    "encrypt_block": cipher["cipher_encrypt_block"],
    "key": cipher["key"],
    "number_of_rounds": cipher["number_of_attacked_rounds"],
    "input_difference": cipher["input_difference"],
    "output_difference": cipher["output_difference"],
    "difference_probability": cipher["difference_probability"]
    }
    counter_real_cipher_recognized = 0
    for i in range(number_of_experiments_with_cipher):
        result = distinguisher(oracle, num_samples)
        if result == 1:
            counter_real_cipher_recognized = counter_real_cipher_recognized + 1

    oracle = {
    "encrypt_block": random_permutation_encrypt_block,
    "key": 0x0,
    "number_of_rounds": 0x0,
    "input_difference": [0x0,0x0],
    "output_difference": [0x0,0x0],
    "difference_probability": 0x0
    }
    counter_random_permutation_recognized = 0
    for i in range(number_of_experiments_with_random_permutation):        
        result = distinguisher(oracle, num_samples)
        if result == 0:
            counter_random_permutation_recognized = counter_random_permutation_recognized + 1

    end = time.time()

    return [[counter_real_cipher_recognized, number_of_experiments_with_cipher], [counter_random_permutation_recognized, number_of_experiments_with_random_permutation]]

def test_differential_distinguisher(number_of_experiments, cipher, num_samples, verb=True):
    cipher_encrypt_block = cipher["cipher_encrypt_block"]
    key = cipher["key"]
    number_of_attacked_rounds = cipher["number_of_attacked_rounds"]
    cipher_add64 = cipher["cipher_add64"]
    round_differences = cipher["round_differences"]
    accumulated_expected_probability = cipher["accumulated_expected_probability"]

    if verb:
        print("\n\nTEST 1:")
        print("-------\n")
        print("\ntesting differential distinguisher accuracy when the input comes from a real cipher...")

    start = time.time()

    number_of_experiments_with_cipher = number_of_experiments//2
    number_of_experiments_with_random_permutation = number_of_experiments//2

    counter_real_cipher_recognized = 0
    average_times_output_difference_was_found = 0

    for i in range(number_of_experiments_with_cipher):
        cipher_output_pairs = generate_set_of_cipher_output_pairs(cipher_encrypt_block, key, number_of_attacked_rounds, cipher_add64, num_samples, round_differences[0])
        
        result = differential_distinguisher_old(cipher_output_pairs, number_of_attacked_rounds, round_differences, accumulated_expected_probability)

        average_times_output_difference_was_found = average_times_output_difference_was_found + result[1]

        if (result[0] == 1):
            counter_real_cipher_recognized = counter_real_cipher_recognized + 1

    end = time.time()

    if verb:
        print("\nThe differential distinguisher succeded in recognizing the real cipher {} times over {}".format(counter_real_cipher_recognized, number_of_experiments_with_cipher))
        print("The output difference was found, on average,              {} times".format(average_times_output_difference_was_found/float(number_of_experiments_with_cipher)))

        print("\nTime: {:05.2f} [sec]\n".format(end-start))


        print("\nTEST 2:")
        print("-------\n")

        print("\ntesting differential distinguisher accuracy when the input comes from a random permutation...")

    start = time.time()

    counter_random_permutation_recognized = 0
    average_times_output_difference_was_found = 0
    for i in range(number_of_experiments_with_random_permutation):
        
        random_output_pairs = generate_set_of_random_output_pairs(num_samples)

        result = differential_distinguisher_old(random_output_pairs, number_of_attacked_rounds, round_differences, accumulated_expected_probability)
        average_times_output_difference_was_found = average_times_output_difference_was_found + result[1]
        if (result[0] == 0):
            counter_random_permutation_recognized = counter_random_permutation_recognized + 1

    end = time.time()

    if verb:
        print("\nThe differential_distinguisher succeded in recognizing the random permutation {} times over {}".format(counter_random_permutation_recognized, number_of_experiments_with_random_permutation))
        print("The output difference was found, on average,                     {} times".format(average_times_output_difference_was_found/float(number_of_experiments_with_random_permutation)))

        print("\nTime: {:05.2f} [seconds]\n".format(end-start))

    return [[counter_real_cipher_recognized, number_of_experiments_with_cipher], [counter_random_permutation_recognized, number_of_experiments_with_random_permutation]]






