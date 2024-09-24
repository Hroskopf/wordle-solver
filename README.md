# Wordle Solver
## Users' documentation

Program, that will solve your daily [Wordle](https://www.nytimes.com/games/wordle/index.html) for you. 

To run the program, you need to run a GUI.py file.

When opened, you will see a 6 x 5 grid on a left and a list of suggested words on the right and two buttons.

You can enter words to the grid from the keyboard. Each words is entered to the current row. You can also erase the last entered letter using Backspace. When entered the word you need to choose colours for each letter, according to result you will get from Wordle. As in standart Wordle green colour is for letter which is on the right place in word, orange --- letter is in word, but in other place, grey --- letter is not in a word. After you choose a word and colours, you need to submit a word. You can do it by pressing a submit button on screen or Enter key on the keyboard.

When the word is submitted, you will move to next row and the list of suggested words will be updated. You will see the new number of candidates to be the unknown word. On suggestion list you are seeing the 10 best choices  of next word according to the program. After each word there is a number --- entropy of the word. The bigger the entropy is, the better choice of this word. The list is sorted in decreasing order of the entropies. 

When program surely knows the unknown word, it will tell you. It is also may happen that the entered data is inconsistent. In this case program also notify you. 

If you get the right word or enter some wrong data, you can reset the field by clicking the reset button or F5 button on the keyboard.

The program is expected to be used as follows: you select a word from the list, enter it into Wordle game, get the result (the color of each letter), enter the selected word and the result into Solver and see how the number of possible unknown words has changed and the new suggestion list. So you iterate until you guess the word, which we promise will happen in no more than 6 attempts. You can also enter words not from list, but this may increase the number of requests.

## Programmers' documentation

You will find next files:

- data/words.txt --- list of all 5-letter words that are accepted by a Wordle game. We will search for words among this list.

- logic.py --- file with the implementation of the main logic for searching for the necessary words. The file implements the WordLogic class, the main function of which --- best suggestions --- returns a list of the best next words.

- GUI.py --- implementation of a graphical interface for user interaction.

---------------	

### Logic

We will call those words that may be the unknown word in the current round as candidates. Also let us call a mask --- some result (colors) we get from a Wordle game. In the implementation such masks are tuples, where 0 is "gray" letter, 1 --- "orange" and 2 --- "green" one.

The key work was to be able to choose words that would reduce the list of candidates as much as possible, regardless of the mask we get. The implementation of this is in the best_suggestions function.

How can we do it? We need some help from math. More precisely, we will need the term [entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) from information theory. Then we want to calculate for some fixed word how good it is as the next entered word. For this, let's calculate the entropy. In this case, entropy will mean the expected value of the "amount" of information that we will receive (in bits). For this for each mask we need to calculate probability to get it as a result of entering the word. And calculate the entropy as a sum of all p(mask) * log (1/p(mask)). After that we can just take the words with the biggest value of entropy.

For that we would need a O(number of words * number of candidates) time (for each entered word - unknown word pairs). There are about 12,000 words in total, so it takes quite a long time to go through all the pairs for python. Therefore, it is implemented in some way probabilistically. A (nearly) random subset of words that are candidates for the input word and a subset of unknown words are selected.And as the test showed, this implementation, although not ideal, gives a good result. On average, it is possible to fit in 6 requests.

In addition to the class, the file implements functions for testing the program on random tests and a function for simulating the program from the console.

---------------	

### GUI

The program implements a simple GUI for Wordle Solver. Written using the Pygame library. 

Implemented Button and Label classes. The Grid class is needed to enter words and display them on the screen. An auxiliary Row class is written for the Grid class, which is one row of cells on the screen.

Character input and output is controlled in the main program loop.

All this interacts with a representative of the WordLogic class to select the necessary words. And the proposed words are displayed on the screen using Labels.
