The file train_and_test_model.py creates the models and saves them in the current working directory. 
It needs to be configured inside the script with the parameters you want to test. 
At the end you get two files named (date)_(hour)_(cipher)_(rounds)_(number of training samples), one .h5 and one .json. 
The json file contains the structure of the network, while the h5 file contains the serialized weights. 
The model is then tested and a summary is printed. 
If you want to disable this function, just comment out the last lines of the script. 
The instructions for the configuration of the script can be found in the first lines.

The file test_model.py tests a pretrained model, you have to call it as 
python3 test_model.py file_name 
where file_name is the name of the model you want to test. 
The name should not contain the extension, since the script will look for both the .json and the .h5 file in the directory. 
As default, a number of samples from 2^0 to 2^20 will be tested, but it can be easily changed inside the script.