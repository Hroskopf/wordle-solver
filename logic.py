import random
import os
from math import log

class WordLogic:
    
    """
    Class with all functions needed for solving Wordle game in (almost) optimal way.
    
    Attributes:
    -----------
    words : list of strings
        Array of all strings, that Wordle game accepts as (5-letter) words.
    candidates : list of string
        Words that could be the unknown word in the current game.
    """

    
    def __init__(self):
        self.words = []
        with open("data/words.txt", 'r') as file:
            for line in file:
                self.words.append(line.upper()[:-1])
        self.reset()
    
    def reset(self):
        """
        Resets the list of candidates.
        """
        self.candidates = list(self.words)
        
    def words_left(self):
        """
        Returns:
        -------
        int
            The number of possible unknown word in the current game.

        """
        return len(self.candidates)
        
    def get_mask(self, word:str, other_word:str):
        
        """
        Returns the result, for given entered and unknown words.

        Parameters:
        -----------
        word : string 
            The entered word
        other_word : string 
            The unknown word

        Returns:
        --------
        tuple
            The mask, we would get as a result for such a query.
        """
        
        other_word_letters_cnt = {c:0 for c in other_word + word}
        mask = [0, 0, 0, 0, 0]
        for i in range(len(mask)):
            if word[i] == other_word[i]:
                mask[i] = 2
            else:
                other_word_letters_cnt[other_word[i]] += 1
        
        for i in range(len(mask)):
            if mask[i] != 2:
                if other_word_letters_cnt[word[i]] > 0:
                    other_word_letters_cnt[word[i]] -= 1
                    mask[i] = 1
        return tuple(mask)

    def update_candidates(self, word:str, mask:tuple):
        
        """
        Function, that updates a candidates array, after we enter a word and get a result.

        Parameters:
        -----------
        word : string
            The word, we enter into game.
        mask: tuple
            The result we get
        """

        new_candidates = []
        for candidate in self.candidates:
            if self.get_mask(word, candidate) == mask:
                new_candidates.append(candidate)
        self.candidates = new_candidates
    
    def best_suggestions(self, num = 10) -> list:
        
        """
        Finds the suggestions for the next word to enter.

        Parameters:
        -----------
        num : int 
            The number of suggestions you want to get

        Returns:
        --------
        list of pairs (float, str)
            The best suggestions for the next move with entropies. 
            If returns one word, that is the answer. If no words returned, answer does not exists.
        """
        
        if len(self.candidates) == 0:
            return []
        if len(self.candidates) == 1:
            return [(0, self.candidates[0])]
        
        # words_sample = set(random.sample(self.words, min(500, len(self.words))) + random.sample(self.candidates, min(500, len(self.candidates))))
        words_sample = random.sample(self.words, min(600, len(self.words)))
        answers_sample = random.sample(self.candidates, min(400, len(self.candidates)))
        arr = []
        for word in words_sample:
            cnt = dict()
            for other_word in answers_sample:
                mask = self.get_mask(word, other_word)
                if not mask in cnt:
                    cnt[mask] = 0
                cnt[mask] += 1
            entropy = 0
            for mask in cnt:
                p = cnt[mask] / len(answers_sample)
                entropy += p * log(1 / p)
            arr.append((entropy, word))
        arr.sort()
        return arr[::-1][:num]

    

def test(test_cnt = 25):
    
    """
        Simulates the game proccess for given number of random unknown words and counts average number of queries.

        Parameters:
        -----------
        test_cnt : int 
            The number of tests. 
    """
    
    W = WordLogic()
    suma = 0     
    max_value = 0 
    for i in range(test_cnt):
        print(i + 1, end = "..")
        W.reset()
        word = random.choice(W.words)
        cnt = 0
        mask = (0,0,0,0,0)
        while mask != (2,2,2,2,2):
            cnt += 1
            s = W.best_suggestions()[0][1]
            mask = W.get_mask(s, word)
            W.update_candidates(s, mask)
        max_value = max(max_value, cnt)
        suma += cnt
    os.system('clear')
    print(f"The average number of queries on {test_cnt} random tests is {suma/test_cnt}. The maximum number of queries is {max_value}.")
        
def play():
    """
        Simulates the game proccess on a console.
        On each turn, writes down a list of best suggestions and number candidates left.
        After that you enter a word you enter and a mask you get.
        Mask must be 5-letter string, consist of letters "B" (for letters that is not in word), "O" (for letters that in a wrong place in word) and "G" (for letters on it`s place).
    """
    w = WordLogic() 
    while True:
        print(w.best_suggestions(), w.words_left())
        s = input()
        t = input()
        mask = [0,0,0,0,0]
        for i in range(5):
            if t[i] == "O":
                mask[i] = 1
            if t[i] == 'G':
                mask[i] = 2
        w.update_candidates(s, tuple(mask))

    

if __name__ == "__main__":
    
    test()
    