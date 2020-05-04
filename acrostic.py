from collections import Counter

import json
import random
import sys

# QUOTE = "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people’s hats off—then, I account it high time to get to sea as soon as I can."
#
# AUTHOR = 'Herman Melville'
# WORK = 'Moby Dick'
#


with open('prepared-quotes.json', 'r') as f:
    quotes = json.load(f)

q = quotes[61]

QUOTE = q['quote']
AUTHOR = q['author']
WORK = q['work']

QUOTE = "A relatively major outpouring—somewhere in fifty miles—about once every decade? Mountain time and city time appear to be bifocal. Even with a geology functioning at such remarkably short intervals, the people have ample time to forget it."

AUTHOR = "John McPhee"
WORK = "Control of Nature"


scrabble_score = {"a": 1 , "b": 3 , "c": 3 , "d": 2 ,
         "e": 1 , "f": 4 , "g": 2 , "h": 4 ,
         "i": 1 , "j": 8 , "k": 5 , "l": 1 ,
         "m": 3 , "n": 1 , "o": 1 , "p": 3 ,
         "q": 10, "r": 1 , "s": 1 , "t": 1 ,
         "u": 1 , "v": 4 , "w": 4 , "x": 8 ,
         "y": 4 , "z": 10}


def get_scrabble_score(word):
    total = 0
    for l in word.lower():
        total += scrabble_score.get(l, 0)
    return total

def normalize_text(text):
    return ''.join([l for l in text.lower() if l.isalpha()])

class Passage():
    def __init__(self, text):
        self.text = text
        self.normalized_text = normalize_text(self.text)
        self.count = Counter(self.normalized_text)

        self.display = self.text

    def is_substring(self, sub):
        check = self.count.copy()
        sub_count = Counter(sub)

        check.subtract(sub_count)
        if any(check[letter] < 0 for letter in check):
            return False
        else:
            return True

    def proc_substring(self, sub):
        sub_count = Counter(sub)

        self.count.subtract(sub_count)

        # print(sub, 'is a substring')
        
        for letter in sub_count.elements():
            idx = self.display.lower().index(letter)
            self.display = self.display[:idx] + '?' + self.display[idx + 1:]


def main():
    p = Passage(QUOTE)

    author = normalize_text(AUTHOR)
    work = normalize_text(WORK)

    attribution = author + work
    att_count = Counter(attribution)

    avg_word_length = len(p.normalized_text)/len(attribution)

    if not (p.is_substring(attribution)):
        sys.exit('Passage does not contain anagrams for both {} and {}.'.
                  format(author, work))

    with open('prepared-dict.txt') as f:
        words = [word.strip() for word in f.readlines()]

    words = sorted(words, key=get_scrabble_score, reverse=True)

    length_sorted_words = sorted(words,
                                 key=lambda word: abs(avg_word_length + .75 - len(word)))

    # At this point the words are primarily in length order, with a second sort key on 
    # Scrabble score. The length order goes in both directions away from the desired
    # average word length.

    # The constant there is a magic number... I've had to take it up or down a bit
    # based on experimentation

    shuffled_words = []
    for x in range(0, len(words), int(len(words)/10)):
        quintile = length_sorted_words[x:x+int(len(words)/10)]
        random.shuffle(quintile)
        shuffled_words.extend(quintile)

    # Now the words are split up into segments, each segment is shuffled, and they're
    # reassembled.

    possible_subs = shuffled_words

    subs = []

    if DISPLAY:
        print('Finding an acrostic for the passage:', end='\n\n')
        print(p.display, end='\n\n')
        print('from {} by {}.'.format(WORK, AUTHOR), end='\n\n')
        print('Need {} words each an average of {:.3} letters.'.
               format(len(attribution), avg_word_length), end='\n\n')

    for sub in possible_subs:
        if sub[0] in +att_count and p.is_substring(sub[1:] + ''.join(att_count.elements())):
            p.proc_substring(sub)
            subs.append(sub)
            att_count.subtract(sub[0])

    remaining = normalize_text(p.display)

    if DISPLAY:
        print('Found {} anagrammed substrings with average length of {:.3} letters:'.
               format(len(subs), sum(map(len, subs))/len(subs)))
        print(subs, end='\n\n')
        print('With {} letters remaining:'.format(len(remaining)))
        print(remaining)

    else:
        print('{}/{}'.format(len(subs), len(attribution)), '({})'.format(
              ''.join([l for l in att_count.elements()])),
              len(remaining), remaining)

    if len(remaining) == 0 and len(subs) == len(attribution):
        ordered_subs = []
        for letter in attribution:
            word = next((word for word in subs if word.startwith(letter)))
            ordered_subs.append(word)
            subs.remove(word)
        print(ordered_subs)
        return True
    else:
        return False

if __name__ == '__main__':
    flags = sys.argv[1:]

    RUN = False
    DISPLAY = True

    if '--run' in flags:
        RUN = True

    if '-q' in flags:
        DISPLAY = False

    if RUN:
        attempts = 1
        solved = False
        while not solved:
            print(attempts, end=': ')
            solved = main()
            attempts += 1

    else:
        main()
