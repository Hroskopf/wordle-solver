import random
import os
from math import log

class WordLogic:
    
    def __init__(self):
        self.words = []
        with open("data/words.txt", 'r') as file:
            for line in file:
                self.words.append(line.upper()[:-1])
        self.candidates = []
        self.reset()
    
    def reset(self):
        self.candidates = list(self.words)

    # def mask_to_int(self, tup:tuple) -> int:
    #     val = 0
    #     for i in tup:
    #         val = val*3 + i
    #     return val
    
    # def int_to_mask(self, val:int) -> tuple:
    #     mask = [0]*5
    #     for i in reversed(range(len(mask))):
    #         mask[i] = val%3
    #         val //= 3
    #     return tuple(mask)
                
    # def is_suitable(self, word:str, other_word:str, mask:tuple) -> bool:
    #     return self.get_mask(word, other_word) == mask
    
    def is_valid_mask(self, word:str, mask:tuple) -> bool:
        st = set()
        for i in range(len(mask)):
            if mask[i] == 1 and word[i] in st:
                return False
            if mask[i] == 0:
                st.add(word[i])
        return True

    # def average_number_of_new_candidates(self, word:str) -> float:
    #     cnt = 0
    #     # for other_word in self.candidates:
    #     for other_word in self.candidates[::max(1, len(self.candidates)//100)]:######
    #         cnt += self.mask_value(word, self.get_mask(word, other_word))
    #     return cnt
    
    
    def decrease_candidates(self, word:str, mask:tuple) -> None:
        
        # for i in range(len(mask)):
        #     if mask[i] != 0:
        #         self.known_letters.add(word[i])
        
        new_candidates = []
        for candidate in self.candidates:
            if self.get_mask(word, candidate) == mask:
                new_candidates.append(candidate)
        self.candidates = new_candidates
        # if len(self.candidates) <= 10:
        #     for i in self.candidates:
        #         print(i)
        #     print("-------------------")
        
    
    # def next_word(self) -> str:  
    #     #return random.choice(self.words)    

    #     maximal_average = -1
    #     s = ""
    #     for i in self.candidates[::max(1, len(self.candidates)//100)]:######
    #     # for i in self.words:
    #         x = self.average_number_of_new_candidates(i)
    #         if maximal_average < x:
    #             maximal_average = x
    #             s = i
    #     return s
    
    def best_suggestions(self, num = 10) -> list:
        
        if len(self.candidates) <= 1:
            return self.candidates
        
        words_sample = set(random.sample(self.words, min(500, len(self.words))) + random.sample(self.candidates, min(500, len(self.candidates))))
        answers_sample = random.sample(self.candidates, min(200, len(self.candidates)))
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
        ans = []
        # return arr[::-1][:num]
        for x in arr[::-1][:num]:
            ans.append(x[1])
        return ans
            
    
    # def get_mask(self, word_index:int, other_word_index:int) -> tuple:
    #     """
    #     returns the result if the mystery word is other_word and the suggestion is word
    #     """
    #     return self.int_to_mask(self.masks[word_index][other_word_index])
    
    def get_mask(self, word:str, other_word:str) -> tuple:        
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
    
    def value(self, word:str, other_word:tuple) -> int:
        mask = self.get_mask(word, other_word)
        val = 0
        for i in range(len(mask)):
            val += mask[i]*mask[i]
        return val
    
    def words_left(self):
        return len(self.candidates)
    

def test_program(test_cnt = 50):
    W = WordLogic()
    suma = 0     
    max_value = 0 
    for i in range(test_cnt):
        if i%10 == 0:
            print(i, end = "..")
        W.reset()
        word = random.choice(W.words)
        cnt = 0
        mask = (0,0,0,0,0)
        while mask != (2,2,2,2,2):
            cnt += 1
            s = W.best_suggestions()[0]
            mask = W.get_mask(s, word)
            W.decrease_candidates(s, mask)
        max_value = max(max_value, cnt)
        suma += cnt
        print()
    os.system('clear')
    print(f"The average number of queries on {test_cnt} random tests is {suma/test_cnt}. The maximum number of queries is {max_value}.")
        

if __name__ == "__main__":
    
    test_program()
    
    # w = WordLogic() 
    # while True:
    #     print("---",w.best_suggestions(), len(w.candidates))
    #     if len(w.candidates) < 10:
    #         print(w.candidates)
    #     s = input()
    #     t = input()
    #     mask = [0,0,0,0,0]
    #     for i in range(5):
    #         if t[i] == "O":
    #             mask[i] = 1
    #         if t[i] == 'G':
    #             mask[i] = 2
    #     w.decrease_candidates(s, tuple(mask))
