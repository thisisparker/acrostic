import argparse
import json
import random
import sys

from collections import Counter

QUOTE = "A relatively major outpouring—somewhere in fifty miles—about once every decade? Mountain time and city time appear to be bifocal. Even with a geology functioning at such remarkably short intervals, the people have ample time to forget it."

AUTHOR = "John McPhee"
WORK = "Control of Nature"

def get_scrabble_score(word):
    total = 0
    scrabble_score = {"a": 1 , "b": 3 , "c": 3 , "d": 2 ,
                      "e": 1 , "f": 4 , "g": 2 , "h": 4 ,
                      "i": 1 , "j": 8 , "k": 5 , "l": 1 ,
                      "m": 3 , "n": 1 , "o": 1 , "p": 3 ,
                      "q": 10, "r": 1 , "s": 1 , "t": 1 ,
                      "u": 1 , "v": 4 , "w": 4 , "x": 8 ,
                      "y": 4 , "z": 10}

    for l in word.lower():
        total += scrabble_score.get(l, 0)
    return total

def normalize_text(text):
    return ''.join([l for l in text.lower() if l.isalpha()])

class Passage():
    def __init__(self, text, work, author):
        self.text = text
        self.normalized_text = normalize_text(self.text)
        self.count = Counter(self.normalized_text)

        self.work = work
        self.author = author

        self.attribution = normalize_text(self.work + self.author)
        self.att_count = Counter(self.attribution)

        self.display = self.text

        self.avg_word_length = len(self.normalized_text)/len(self.attribution)

    def reset(self):
        self.display = self.text
        self.count = Counter(self.normalized_text)
        self.att_count = Counter(self.attribution)

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

def deterministic_sort(words, p):
    words = sorted(words, key=get_scrabble_score, reverse=True)
    words = sorted(words, key=lambda word: abs(p.avg_word_length + .75 - len(word)))

    # at this point the words are primarily in length order, with a second sort key on 
    # scrabble score. the length order goes in both directions away from the desired
    # average word length.

    # the constant there is a magic number... i've had to take it up or down a bit
    # based on experimentation

    return words

def run_dictionary(words, p):
    shuffled_words = []
    for x in range(0, len(words), int(len(words)/10)):
        quintile = words[x:x+int(len(words)/10)]
        random.shuffle(quintile)
        shuffled_words.extend(quintile)

    # Now the words are split up into segments, each segment is shuffled, and they're
    # reassembled.

    possible_subs = shuffled_words

    subs = []

    for sub in possible_subs:
        if sub[0] in +p.att_count and p.is_substring(sub[1:] +  
                ''.join(p.att_count.elements())):
            p.proc_substring(sub)
            subs.append(sub)
            p.att_count.subtract(sub[0])

    remaining = normalize_text(p.display)

    return subs, remaining

def main(loopcount=1, quiet=False):
    p = Passage(QUOTE, WORK, AUTHOR)

    if not (p.is_substring(p.attribution)):
        sys.exit('Passage does not contain anagrams for both {} and {}.'.
                  format(author, work))

    with open('prepared-dict.txt') as f:
        words = [word.strip() for word in f.readlines()]

    words = deterministic_sort(words, p)

    # At this point the words are in a single "standard" order, with the shuffling
    # happening during each dictionary run.


    print('Finding an acrostic for the passage:', end='\n\n')
    print(p.display, end='\n\n')
    print('from {} by {}.'.format(p.work, p.author), end='\n\n')
    print('need {} words each an average of {:.3} letters.'.
           format(len(p.attribution), p.avg_word_length), end='\n\n')

    attempts = 1
    solved = False

    while not solved and (not loopcount or attempts <= loopcount):
        print(f'{attempts:>4}', end=': ')
        subs, remaining  = run_dictionary(words, p)

        if len(remaining) == 0 and len(subs) == len(p.attribution):
            solved = True
 
        unordered_subs = subs[:]
        ordered_subs = []
        for letter in p.attribution:
            word = next((word for word in unordered_subs if word.startswith(letter)), '')
            ordered_subs.append(word)
            if word:
                unordered_subs.remove(word)

        if quiet:
            print('{}/{}'.format(len(subs), len(p.attribution)), '({})'.format(
                  ''.join([l for l in p.att_count.elements()])),
                  len(remaining), remaining)
        else:
            print('Found {} anagrammed substrings with average length of {:.3} letters:'.
                   format(len(subs), sum(map(len, subs))/len(subs)))
            print(ordered_subs, end='\n\n')
            print('With {} letters remaining:'.format(len(remaining)))
            print(remaining)

        p.reset()
        attempts += 1

    if solved and quiet:
        print('yay!', ordered_subs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--loop',
                        nargs='?',      # takes one or zero arguments
                        const=0,        # uses const if flag is present but with no argument
                        default=1,      # uses default if flag is not present at all
                        type=int)
    parser.add_argument('-q', '--quiet', action='store_true')

    args = parser.parse_args()

    main(loopcount=args.loop, quiet=args.quiet)
