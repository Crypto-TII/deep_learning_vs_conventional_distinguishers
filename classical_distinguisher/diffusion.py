from tea_block import *

def bit_flip_diffusion_test(encrypt_block_function, number_of_rounds, key, BLOCK_BIT_SIZE, NUMBER_OF_INPUTS):
    average_changed_bits = [0 for i in range(number_of_rounds)]
    for r in range(0,number_of_rounds):
        # print("r = " + str(r))
        total_changed_bit = 0
        for j in range(NUMBER_OF_INPUTS):
            input = join_blocks(random_message())
            for i in range(BLOCK_BIT_SIZE):
            # for i in range(2):
                in1 = split_block(input)
                in2 = split_block(change_bit(input, i))
                out1 = join_blocks(encrypt_block_function(in1, key, nrounds=r))
                out2 = join_blocks(encrypt_block_function(in2, key, nrounds=r))
                output = out1 ^ out2
                total_changed_bit = total_changed_bit + hamming_weight(output)

                # print("i = " + str(i))
                # print("input 1  = ", end='')
                # print_block(input)
                # print("")
                # print("input 2  = ", end='')
                # print_block(change_bit(input, i))
                # print("")

                # print("enc 1    = ", end='')
                # print_array(encrypt_block(in1, key, nrounds=r))
                # print("")
                # print("enc 2.   = ", end='')
                # print_array(encrypt_block(in2, key, nrounds=r))
                # print("")

                # print("output 1 = ", end='')
                # print_block(out1)
                # print("")
                # print("output 2 = ", end='')
                # print_block(out2)
                # print("")
                # print("out xor  = ", end='')
                # print_block(output)
                # print("")

        average_changed_bits[r] = total_changed_bit / float(BLOCK_BIT_SIZE*NUMBER_OF_INPUTS)

    return average_changed_bits

def print_result_bit_flip_diffusion_test(average_changed_bits_list, BLOCK_BIT_SIZE):
    for r in range(len(average_changed_bits_list)):
        print("r = %2d: " % r, end='')
        print("average changed bits = {:06.2f}".format(average_changed_bits_list[r]), end='')
        if ((average_changed_bits_list[r] > (BLOCK_BIT_SIZE//2 - 8)) and (average_changed_bits_list[r] < (BLOCK_BIT_SIZE//2 + 8))):
            print("  *", end='')
        if ((average_changed_bits_list[r] > (BLOCK_BIT_SIZE//2 - 4)) and (average_changed_bits_list[r] < (BLOCK_BIT_SIZE//2 + 4))):
            print("**", end='')
        if ((average_changed_bits_list[r] > (BLOCK_BIT_SIZE//2 - 2)) and (average_changed_bits_list[r] < (BLOCK_BIT_SIZE//2 + 2))):
            print("****", end='')
        if ((average_changed_bits_list[r] > (BLOCK_BIT_SIZE//2 - 1)) and (average_changed_bits_list[r] < (BLOCK_BIT_SIZE//2 + 1))):
            print("*******", end='')
        if ((average_changed_bits_list[r] > (BLOCK_BIT_SIZE//2)) and (average_changed_bits_list[r] < (BLOCK_BIT_SIZE//2 + 1))):
            print("*", end='')
        print("")
