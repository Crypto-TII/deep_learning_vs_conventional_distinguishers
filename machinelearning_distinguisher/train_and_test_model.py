import datetime
from network_utils import *

total_results = []

#### START CONFIG
NET = "TD" #TD or CNN
CIPHER = "TEA" #TEA or RAIDEN
ROUNDS_LIST = [1,2] #TEA up to 64, RAIDEN up to 32
N_TRAINING_INPUT_PAIRS = [1000000]
N_TRIES_CLASSIFICATION = 4
#INPUT_DIFFS =  [0x7fffff0000000000] #RAIDEN
INPUT_DIFFS = [0xfffffff1ffffffff] #TEA
KEY = 0x11CAD84E96168E6B704A8B1C57BBE5D3 #TEA
#KEY = -1 #RAIDEN
EPOCHS = 10
EPOCHS_CYCLE = 5
BATCH = 500
MINLR = 0.0003
MAXLR = 0.015
THRESHOLD = 0.5*N_TRIES_CLASSIFICATION
LAYERS = [64,64,32]
VERBOSE = 1
#### END CONFIG


scheduler = cyclic_lr(EPOCHS_CYCLE,MAXLR,MINLR)
for DELTA in INPUT_DIFFS:
    for N_TRAINING_SAMPLES in N_TRAINING_INPUT_PAIRS:
        results = {}
        for N_ROUNDS in ROUNDS_LIST:
            model = train_network_words(NET, LAYERS, scheduler, N_TRAINING_SAMPLES, CIPHER, DELTA, N_ROUNDS, KEY, EPOCHS, BATCH, VERBOSE)
            model_to_file(model, CIPHER, N_ROUNDS, N_TRAINING_SAMPLES)
            total_accuracy, accuracy_from_cipher, accuracy_from_random = distinguisher(0, model, 10000, THRESHOLD, N_TRIES_CLASSIFICATION, CIPHER, DELTA, N_ROUNDS, KEY, 0)
            results[N_ROUNDS] = (total_accuracy, accuracy_from_cipher, accuracy_from_random)
        total_results.append((N_TRAINING_SAMPLES,DELTA,results))

print(total_results)

for v in total_results:
    print("SAMPLES: {}".format(v[0]))
    print("INPUT DIFFERENCE: {}".format(hex(v[1])))
    print(v[2])
    print()
