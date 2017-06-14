This program kNN.py implement a k-nearest neighbor learner for both classification and regression 
that read files in the ARFF format.
The program can ba callable from the command line: 
kNN <train-set-file> <test-set-file> k

The second program kNN-select.py use leave-one-out cross validation with just the training data 
to select the value of k to use for the test set by evaluating k1 k2 k3 and 
selecting the one that results in the minimal cross-validated error within the training set.
The program can ba callable from the command line: 
kNN-select <train-set-file> <test-set-file> k1 k2 k3

