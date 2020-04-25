from collections import Counter

import random
import sys

QUOTE = "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people’s hats off—then, I account it high time to get to sea as soon as I can."

AUTHOR = 'Herman Melville'
WORK = 'Moby Dick'

FREQ_ALPH = 'qjxzwkvfybhmpgudclotnrsaie'

class Passage():
    def __init__(self, text):
        self.text = text
        self.prepared = ''.join([l for l in text.lower() if l.isalpha()])
        self.count = Counter(self.prepared)

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

    author = ''.join([l for l in AUTHOR.lower() if l.isalpha()])
    work = ''.join([l for l in WORK.lower() if l.isalpha()])

    if not (p.is_substring(author) and p.is_substring(work)):
        sys.exit('Passage does not contain anagrams for {} and {}.'.format(author, work))

    with open('prepared-dict.txt') as f:
        words = [word.strip() for word in f.readlines()]

    words = sorted(words, key=lambda word: [FREQ_ALPH.find(l) for l in word])
    shuffled_words = []

    for x in range(0, len(words), int(len(words)/10)):
        decile = words[x:x+int(len(words)/10)]
        random.shuffle(decile)
        shuffled_words.extend(decile)

    possible_subs = shuffled_words

    subs = []

    print('Finding an acrostic for the passage:', end='\n\n')

    print(p.display, end='\n\n')

    print('from {} by {}.'.format(WORK, AUTHOR), end='\n\n')

    for sub in possible_subs:
        if p.is_substring(sub):
            p.proc_substring(sub)
            subs.append(sub)
        else:
            pass
            # print(sub, 'is not a substring')

    print('You may remove the anagrammed substrings:', end='\n\n')
    print(subs, end='\n\n')

    remaining = ''.join([l for l in p.display if l.isalpha()])

    print('With {} letters remaining:'.format(len(remaining)), end='\n\n')
    print(remaining)

if __name__ == '__main__':
    main()

