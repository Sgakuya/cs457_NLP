# Homework 3 Report

## Basics
External resources used on this assignment:
* 

Classmates you talked to about this assignment:
* 

How many hours did you spend on this assignment?
* 

### Group Member #1
* Your middlebury email: sgakuya@middlebury.edu
* How many hours did you spend on outside of class on CS 457 this week, _excluding this assignment_? 3


## Report
### Accuracy
What is the tag-level accuracy of your system? around 90.55 without extension


### Method
How did you handle unknown words in your system?


### Error Analysis
Identify three errors in the automatically tagged data, and analyse them (i.e., for each error,
write one brief sentence describing the possible reason for the error and how it could be
fixed). To identify errors, you can use the `error_helper.py` script that is provided in the starter code.
* Error 1
  * Tokens: What row ?
  * Actual tags: DET NOUN PUNCT
  * Predicted tags: PRON NOUN PUNCT
  * Analysis:
* Error 2
  * Tokens: He later expanded his pretense by claiming to be " Protector of Mexico " as well .
  * Actual tags: PRON ADV VERB PRON NOUN SCONJ VERB PART AUX PUNCT PROPN ADP PROPN PUNCT ADV ADV PUNCT
  * Predicted tags: PRON ADV VERB PRON NOUN ADP PROPN PART AUX PUNCT NOUN ADP PROPN PUNCT ADV ADV PUNCT
  * Analysis:
* Error 3
  * Tokens: * Tokens: and she was always really shy to show that off to people ,
  * Actual tags: CCONJ PRON AUX ADV ADV ADJ PART VERB PRON ADP ADP NOUN PUNCT 
  * Predicted tags: CCONJ PRON AUX ADV ADV VERB PART VERB PRON ADV ADP NOUN PUNCT
  * Analysis: "shy" is an adj but it is predicted to be an verb, I believe since it is following 2 adverbs. The model might need more context to know it is modifying the "she" in the sentence
