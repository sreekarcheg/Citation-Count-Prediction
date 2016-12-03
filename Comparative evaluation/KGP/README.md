## Description
**run.sh**: Parses the dataset and stores in pickled files(for later programs to use). Further, trains an LDA model and writes the model to a pickled file, as well.  

**authorFeats.py**: Generates the author feats and writes to pickled file  

**paperFeats.py**: Generates paper features and writes to pickled file  

**rule-based.py**: Categorises train set into the six categories as detailed in the paper

**learning-model.py**: Learns an SVC over the train set to categorise paper into any one of 6 categories  

**train-model.py**: Trains 5 SVR's(1year-5years) over each of the six categories and print train and test accuracy reports

## To print and view results   
```
$ ./run.sh  
$ python getTopic.py  
$ python authorFeats.py  
$ python paperFeats.py  
$ python rule-based.py  
$ python learning_model.py  
$ python train_model.py 
```
