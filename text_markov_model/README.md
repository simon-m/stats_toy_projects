# stats_toy_projects

Miscellaneous toy projects related to statstical modeling / learning.

## Text markov model tmm.py
A small naive implementation of a markov model for text data.

For a model of order *n*, a given *prefix* consists in *n* words
(separated by blanks). A distribution of *suffixes* is assigned to
each prefix with probabilities fitted on the training data. So far
frequencies are used (MLE).

Given a prefix, it is then possible to output the most likely suffix
or a random suffix whose probability follows that of the traning data.
Considering the suffix as part of a new prefix allows the generation
of sentences.
 


