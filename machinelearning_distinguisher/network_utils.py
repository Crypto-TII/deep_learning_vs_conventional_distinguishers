import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
from keras.callbacks import LearningRateScheduler
from keras.models import Sequential, model_from_json, Model
from keras.layers import Dense, Conv1D, Flatten, Reshape, Permute, TimeDistributed, Input, Add, BatchNormalization, Activation, LeakyReLU
from keras.optimizers import Adam
from generation_utils import *
from keras import backend as k
from keras.regularizers import l2
import tensorflow as tf
import numpy as np
import datetime

def cyclic_lr(num_epochs, high_lr, low_lr):
  res = lambda i: low_lr + (high_lr - low_lr)*((num_epochs-i) % (num_epochs))/(num_epochs)
  return(res)

def create_cnn(input_shape, dims, loss='mse', optimizer='adam', metrics=['accuracy']):
    assert len(dims) > 0
    m = Sequential()
    m.add(Reshape((input_shape//32,32), input_shape=(input_shape,)))
    m.add(Permute((2,1)))
    m.add(Conv1D(32, kernel_size=1))
    m.add(BatchNormalization())
    m.add(LeakyReLU())
    m.add(Conv1D(32, kernel_size=1))
    m.add(BatchNormalization())
    m.add(LeakyReLU())
    m.add(Flatten())
    for j in range(len(dims)):
        m.add(Dense(dims[j]))
    m.add(BatchNormalization())
    m.add(LeakyReLU())
    m.add(Dense(2,activation='softmax'))
    m.compile(loss = loss, optimizer = optimizer, metrics = metrics)
    return m

def create_td(input_shape, dims, loss='mse', optimizer='adam', metrics=['accuracy']):
    assert len(dims) > 0
    m = Sequential()
    m.add(Reshape((input_shape//32,32), input_shape=(input_shape,)))
    m.add(Permute((2,1)))
    m.add(TimeDistributed(Dense(32)))
    m.add(BatchNormalization())
    m.add(LeakyReLU())
    m.add(TimeDistributed(Dense(32)))
    m.add(BatchNormalization())
    m.add(LeakyReLU())
    m.add(Flatten())
    for j in range(1, len(dims)):
        m.add(Dense(dims[j]))
        m.add(BatchNormalization())
        m.add(LeakyReLU())
    m.add(Dense(2,activation='softmax'))
    m.compile(loss = loss, optimizer = optimizer, metrics = metrics)
    return m

def train_network_words(network_type, layers, scheduler, samples, cipher, input_diff, rounds, key = -1, epochs = 20, batch = 500,  verb = 0):
    x,y = generate_sample(samples, input_diff, cipher, key, rounds)
    val_x, val_y = generate_sample(10000, input_diff, cipher, key, rounds)
    if network_type == "CNN":
        model = create_cnn(128, layers)
    elif network_type == "TD":
        model = create_td(128, layers)
    model.fit(x, y, epochs=epochs, batch_size=batch, validation_data=(val_x, val_y), shuffle=1, callbacks=[LearningRateScheduler(scheduler)], verbose=verb)
    if verb:
        loss, accuracy = model.evaluate(val_x, val_y)
        print('Loss {}, Accuracy {}'.format(loss, accuracy))
    return model

def train_network_diff(network_type, layers, scheduler, samples, cipher, input_diff, rounds, key = -1, epochs = 20, batch = 500,  verb = 0):
    x,y = generate_diff_sample(samples, input_diff, cipher, key, rounds)
    val_x, val_y = generate_diff_sample(10000, input_diff, cipher, key, rounds)
    if network_type == "CNN":
        model = create_cnn(64, layers)
    elif network_type == "TD":
        model = create_td(64, layers)
    model.fit(x, y, epochs=epochs, batch_size=batch, validation_data=(val_x, val_y), shuffle=1, callbacks=[LearningRateScheduler(scheduler)], verbose=verb)
    if verb:
        loss, accuracy = model.evaluate(val_x, val_y)
        print('Loss {}, Accuracy {}'.format(loss, accuracy))
    return model

def distinguisher(type, model, tries, thres, set_size, cipher, input_diff, rounds, key, verb = 0):
    num_tp = 0
    den_tp = 0
    num_tn = 0
    den_tn = 0
    res = 0
    for i in range(tries):
        if type == 0:
            pred_x, pred_y = generate_sample_same_output(set_size, input_diff, cipher, key, rounds, np.random.randint(0,2))
        elif type == 1:
            pred_x, pred_y = generate_diff_sample_same_output(set_size, input_diff, cipher, key, rounds, np.random.randint(0,2))

        if pred_y == 1:
            den_tp = den_tp + 1
        else:
            den_tn = den_tn + 1
        predictions = model.predict_classes(pred_x)
        if list(predictions).count(0) > thres:
            pred_output = 0
        else:
            pred_output = 1
        if verb:
            print("zeros:{}, ones: {}, predicted: {}, true: {}".format(list(predictions).count(0), list(predictions).count(1),pred_output, pred_y), end=" ")

        if pred_output == pred_y:
            if verb:
                print()
            res = res + 1
            if pred_y == 1:
                num_tp = num_tp + 1
            else:
                num_tn = num_tn + 1
        else:
            if verb:
                print("FAIL")
    return res/tries, num_tp/den_tp, num_tn/den_tn

def model_to_file(model, cipher, rounds, samples):
    t = datetime.datetime.now()
    fname = str(t.date())+"_"+str(t.hour)+"-"+str(t.minute)+"-"+str(t.second)+"_"+cipher+"_"+str(rounds)+"_"+str(samples)
    j = model.to_json()
    with open(fname+".json", "w") as json_file:
        json_file.write(j)
    model.save_weights(fname+".h5")

def model_from_file(fname):
    json_file = open(fname+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(fname+".h5")
    return loaded_model
