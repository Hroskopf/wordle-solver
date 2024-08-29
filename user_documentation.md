# Wordle Solver

Program, that will solve your daily [Wordle](https://www.nytimes.com/games/wordle/index.html) for you. When opened, you will see a 6 x 5 grid on a left and a list of suggested words on the right.

- A grid created to enter words and the color of each letter (which you will get from the Wordle game). Words are entered to the current line from the keyboard. The colors of the letters can be changed by clicking on the corresponding cell with the mouse.

- The list are 10 of words that would help you find a unknown word in a smallest amount of queries. The best suggestions are located on the top of list. If the programm knows exactly the unknown word, there will only be one word in the list. On the other hand, if the list is empty, it means that the data you entered is inconsistent.

- The reset button would clear a grid and update a list of suggestions.

The program is expected to be used as follows: you select a word from the list, enter it into Wordle, get the result (the color of each letter), enter the selected word and the result into Solver and see how the number of possible unknown words has changed and the new suggestion list. So you iterate until you guess the word, which will happen in no more than 6 attempts.