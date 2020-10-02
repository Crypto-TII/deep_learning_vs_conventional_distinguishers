from network_utils import model_from_file, distinguisher
import sys

#### START CONFIG
CIPHER = "TEA" #TEA or RAIDEN
N_ROUNDS = int(sys.argv[1].split("_")[-2])
N_TRAINING_INPUT_PAIRS = [1000000]
#INPUT_DIFFS =  [0x7fffff0000000000] #RAIDEN
INPUT_DIFFS = [0xfffffff1ffffffff] #TEA
KEY = 0x11CAD84E96168E6B704A8B1C57BBE5D3 #TEA
#KEY = -1 #RAIDEN
#### END CONFIG

d = {}
model = model_from_file(sys.argv[1])
print("With {} rounds".format(N_ROUNDS))
#thres = [x/10 for x in range(10)]
thres = [0.5]
for t in thres:
    print(t)
    for tries in range(20):
        THRESHOLD = t*2**tries
        total_accuracy, accuracy_from_cipher, accuracy_from_random = distinguisher(0, model, 1000, THRESHOLD, 2**tries, CIPHER, INPUT_DIFFS[0], N_ROUNDS, KEY, 0)
        d[tries] = (N_ROUNDS,total_accuracy)
        print((tries, total_accuracy))
    print(d)
