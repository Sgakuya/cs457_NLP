# Homework 1 Report

## Basics
What is your Middlebury email? 
* sgakuya@middlebury.edu

External resources used on this assignment: 
* python docs

Classmates you talked to about this assignment:
* NA

How many hours did you spend on this assignment?
* 3

How many hours did you spend on outside of class on CS 457 this week, _excluding this assignment_?
* 6


## Report

### Regex Description
_Clearly describe how you make use of each of the required regular expression features in your make_message function._

#### Regular expression groups
In one of the cases, I use matchgroups to make a "dad joke" whenever the user makes a statement in the form "I am ..." e.g., "I am tired" to grab the predicate of the sentence and use it to refer to the user as the predicate e.g., "Hi tired"

I also use it similarly in a different case to split a sentence into subject, verb and predicate when the user asks a "wh" question. I then reorganize the sentence to state that what they asked was irrelevant and state a conspiracy theory instead and claim that that's more important


#### Character classes
I used the digit character class to allow users to type simple math equations.

I also used the word boundary in different parts of the code e.g., getting the bounds of the equations, check whether the phrase "[I|i] am" is present in a sentence etc. 

I also use the square brackets to pick up when characters are in lower/upper case


#### Quantifiers
I utilized the Kleene star in various location e.g, to allow any number of spaces between the operands of a mathematical equation, to grab the predicate and verb when the user asks a "wh" question to allow any length, etc


### Analysis
_Describe at least one interaction with your bot that worked well, and at least one interaction with your bot that works poorly (or not as one might expect). You should include a transcript of your conversations in your writeup. This should include explanation not just of what happened, but why it happened, and why that was good or bad._

#### An interaction that went well
##### Transcript
you: what is the meaning of love \
bot: Just ignore what the meaning of love is, let's talk about what's ACTUALLY important - Ever wondered why gas station hot dogs are *always* spinning?


##### What happened and why? What was it good?
Rephrasing the question as a statement worked well in this instance. I made the assumption that a subject(including a prepositional phrase) will follow the verb and could therefore lump everything that comes after it as the subject phrase

#### An interaction that did went poorly
##### Transcript
you: why is cheese spicy \
bot: Stop worrying about why cheese spicy is, have you considered - You never see baby pigeons. Think about that.


##### What happened and why? What was it bad?
The order of the verb and predicate did not coincide with my previous assumptions. When rephrasing English questions as statements, the ordering of the sentence components in the predicate depends on the purpose of the words after. In this case the adjective is not part of the subject phrase although I had lumped them together through my previous assumption


### Another Chatbot
_Interact with one of your classmate's chatbots, and answer the following questions_

#### What was the chatbot called?
PantherBot


#### Did they implement any features that you would have liked to implement in your chatbot if you had extra time?
I liked how it had useful answers to some particular Midd related questions rather than shrugging off the questions like mine does in most instances.


#### Which features of regular expressions might they have used to achieve that functionality (regular expression groups, character classes, quantifiers, anchors, etc.)?
I believe they used RE groups to grab the information being asked for and matched it to the predefined answers to the questions if certain keywords were present e.g, dining hall and dorm in the "What is the best ..." question

