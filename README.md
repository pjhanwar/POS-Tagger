# Hidden Markov Model Part-of-Speech Tagger

## Overview
A Hidden Markov Model part-of-speech tagger for English, Hindi and Chinese language. The training data is tokenized and tagged; the test data is also tokenized, and the tagger add the tags to the test data. Add one smoothing is done for unseen words.

## Training and Development data:

Two files (one English, one Chinese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
Two files (one English, one Chinese) with untagged development data, with words separated by spaces and each sentence on a new line.
Two files (one English, one Chinese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.

## Programs
Consists of two programs: hmmlearn.py learns a hidden Markov model from the training data, and hmmdecode.py uses the model to tag new data. 

The learning program is invoked in the following way:
> python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. 

The tagging program is invoked in the following way:
> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program reads the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

## Accuracy 
The accuracy of your tagger is determined by comparing the output of the tagger to a reference tagged text. 

## Resuts on Test Data

English : 88% accurate <br>
Chinese : 86% accurate <br>
Hindi   : 92% accurate <br>
