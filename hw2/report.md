# Homework 2 Report

## Basics
What is your Middlebury email?
* sgakuya@middlebury.edu

External resources used on this assignment:
* None

Classmates you talked to about this assignment:
* NA

How many hours did you spend on this assignment?
* 3

How many hours did you spend on outside of class on CS 457 this week, _excluding this assignment_?
* 4


## Report
### Evaluating evaluation metrics
#### What is one advantage of using accuracy over a confusion matrix to evaluate your model?
It is easier to compute


#### What is one advantage of using a confusion matrix over accuracy to evaluate your model?
Has more information about what was accurately predicted in the individual categories. 


#### Interpreting your confusion matrix
_Choose a language from the data set. Given any knowledge that you have about properties about that language (e.g., writing system, language families), explain any unique properties of its row in the confusion matrix, including (a) performance compared to other languages, (b) languages that it is more likely to be predicted as than others, and (c) anything else you think is relevant._




### Effects of priors
Update your code so that your prior is uniform, e.g., the probability for each of the 8 languages is $log\left(\frac{1}{8}\right)$. Then, answer the following questions.
#### How do your results change? Why?
Slight increase in accuracy. I believe it is equally likely that a document is in any language therefore the determining factor is just the likelihood


#### Describe a situation in which you might _want_ to use a uniform prior.
Similar to above, likely if you want to make it equally likely to a document with any language

