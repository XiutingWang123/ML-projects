nnet.py implement a program that learns a neural network using stochastic gradient descent.
it is callable from command line:
nnet l h e <train-set-file> <test-set-file>
where l specifies the learning rate, 
h the number of hidden units and 
e the number of training epochs. 
After training for e epochs on the training set, this program use the learned neural net 
to predict a classification for every instance in the test set.
