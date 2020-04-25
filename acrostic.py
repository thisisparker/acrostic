from collections import Counter

import random

quote = "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people’s hats off—then, I account it high time to get to sea as soon as I can."

possible_subs = ['hermanmelville', 'mobydick']

with open('prepared-dict.txt') as f:
    words = [word.strip() for word in f.readlines()]

random.shuffle(words)

possible_subs.extend(words)

subs = []

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
    p = Passage(quote)

    print('Beginning with the passage:')

    print(p.display)

    for sub in possible_subs:
        if p.is_substring(sub):
            p.proc_substring(sub)
            subs.append(sub)
        else:
            pass
            # print(sub, 'is not a substring')

    print('You may remove the anagrammed substrings:')
    print(subs)

    remaining = ''.join([l for l in p.display if l.isalpha()])

    print('With {} letters remaining:'.format(len(remaining)))
    print(remaining)

if __name__ == '__main__':
    main()

