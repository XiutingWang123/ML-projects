This program implement an ID3-like decision-tree learned for classification that read files in the ARFF format.

This program can handle numeric and nominal attributes.

It can be called from the command line:
dt-learn <train-set-file> <test-set-file> m

where m is a threshold that if there are less than m training instances reaching the node, making a node into a leaf.
