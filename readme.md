# Performance comparison between deeplearning-based and conventional cryptographicdistinguishers: software tool

This repository contains the software tools utilized to achieve the results contained in the paper:
_"Performance comparison between deeplearning-based and conventional cryptographicdistinguishers"_

Note that this tool does not search for differential trails.
Indeed, in order to properly work, the differential trails, and their probabilities, need to be given as input, after being computed with another tool.

## Folder: `classical_distinguisher`:

This folders contains the scripts used to generate the results corresponding to the conventional distinguishers, in the paper referred to as:
* _Bitflip distinguisher_
* _Differential distinguisher_

### Main Scripts

The main scripts used for the result of the paper are the following:

* `tea_block.py`
  - Contains Python implementation of 
    + Tiny Encryption Algorithm (TEA)
    + XTEA
    + RAIDEN
    + function to compute the differential trail (round differences) 
      given the input-output difference pair of the F function
    + functions to print the differential trail
    + functions that computes the probability of the trail heuritically
    + function to print the heuristic probability
  - TEA and XTEA encryption function can be tested from the terminal 
    with the commands
    + `python3 test_tea_block.py`
    + `python3 test_xtea_block.py`
  - The trails given from the paper 
    https://eprint.iacr.org/2013/853.pdf
    can be tested from the termina with the command
    + `python3 verify_trails.py`
    + One can select which ciphert to analyze, 
      by commenting/uncommenting the lines
      ```
      CIPHER = "TEA"
      # CIPHER = "XTEA"
      # CIPHER = "RAIDEN"
      ```
    + The number of rounds to be attacked is configurable, 
      for each cipher, in the lines:
      `number_of_rounds = 4`
    + Inside the definition of the ciphers it is also to:
      * set the cipher key
      * the differential trail used 
        (in the form of input/output differences of the F function, 
        as defined in https://eprint.iacr.org/2013/853.pdf)
      * set the probability of each input/output difference
    
* `compare_accuracies.py`
  - Outputs the comparison among the accuracy of the distinguisher when 
    distinguishing a random permutation, a cipher, and the total accuracy 
  - The output generated can also be used to generate 
    the latex tables in the paper
  - One can set the number of experiments and 
    the cipher parameters inside the scirpt
  - One can set the number of tested rounds in the line
    `for number_of_rounds in range(7,9):`
  - One can set the number of samples to be used in the line
    `for i in range(12,21):`


### Other scripts

The folder also contains other scripts (not related to the paper), 
described below:

* `classical_distinguisher.py`
  - Contains the Python code for
    + bitflip distinguisher
    + differential distinguisher
    + experiment to compute the accuracy of the two distinguishers
  - The distinguishers can be run from terminal by typing the command
    + `test_classical_distinguisher.py`
      - One can configure the number of experiments inside the script,
        by modifying the line
        `number_of_experiments = 10`
      - One can select which ciphert to analyze, 
        by commenting/uncommenting the lines
        ```
        CIPHER = "TEA"
        # CIPHER = "XTEA"
        # CIPHER = "RAIDEN"
        ```
      - The number of rounds to be attacked is configurable, 
        for each cipher, in the lines:
        `"number_of_attacked_rounds": 4,`

* `diffusion.py`
  - Contains the `bit_flip_diffusion_test()`
  - The diffusion test can be run from terminal typing the command 
    + `test_diffusion.py`

* `compare_encrypt_time.py`
  - Outputs the time required to perform some of the operations

* `create_latex_3d_graph.py`
  - Used to generate the latex tables in the paper
  - the input must be generated using the script 
    `compare_accuracies.py`

* `verify_trails_tea.py`
  - Verifies that TEA trails computed in 
    https://eprint.iacr.org/2013/853.pdf
    are correct

* `verify_trails_xtea.py`
  - Verifies that XTEA trails computed in 
    https://eprint.iacr.org/2013/853.pdf
    are correct

### Data

Some of the results have been saved for convenience:

* `results_compare_accuracies.txt`
  Contains the output generated by running the command
  `python3 compare_accuracies.py`

* `results_distinguisher.txt`
  Contains the output generated by running the command
  `python3 test_classical_distinguisher.py`


## Folder: `machinelearning_distinguisher`:

This folders contains the scripts used to generate the results corresponding to the neural network based distinguishers, in the paper referred to as:
* _Time Distributed (TD) distinguisher_
* _Convolutional distinguisher_


### Scripts

The main scripts used for the result of the paper are the following:

* `train_and_test_model.py` 
  - Needs to be configured inside the script 
    with the parameters that need to be tested. 
  - The instructions for the configuration of the script 
    can be found in the first lines.
  - It works as follows:
    + Creates the models and saves them in the current working directory. 
    + Generates a .h5 and a .json files using the name convention
      `[date]_[hour]_[cipher]_[rounds]_[number_of_training_samples]`:
      * The json file contains the structure of the network
      * The h5 file contains the serialized weights. 
    + The model is then tested and a summary is printed. 
      To disable the print function, 
      comment out the last lines of the script. 

* `test_model.py` 
  - Tests a pretrained model
  - It can be run from a terminal with the command
    `python3 test_model.py [file_name]` 
    where `[file_name]` is the name of the model to be tested. 
    The name should not contain the extension, 
    since the script will look for both 
    the .json and the .h5 file in the directory. 
  - As default, a number of samples from 2^0 to 2^20 will be tested, 
    but it can be easily changed inside the script.
