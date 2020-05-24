# Acrostic puzzle generator

This is currently a work in progress and under active development.

The goal of this software is to automate the anagramming portion of constructing an [acrostic puzzle](https://en.wikipedia.org/wiki/Acrostic_(puzzle)). In order to that, it takes a quote and runs through a list of possible answers to find a set of words or short phrases that collectively constitute an anagram for that quote, for which the initial letters spell out the name of the quote's originating work and author.

For example, given the following quote from `Control of Nature` by `John McPhee`:

> A relatively major outpouring—somewhere in fifty miles—about once every decade? Mountain time and city time appear to be bifocal. Even with a geology functioning at such remarkably short intervals, the people have ample time to forget it.

One possible solution is the following words:

```
jiggy
onthemove
hardener
nutritive
meatpatty
cheapside
punchline
homealone
eroticism
emmy
cultivate
onliberty
navigate
tucksinto
rareeshow
officiate
lafayette
ovum
frootloops
nimbi
appellate
teamowner
ubbi
roadflare
eggy
```

(The words are only as good as the wordlist that you start with! These aren't great.)

It works in a very brute force manner: after shuffling the entire list of words, it proceeds from front to back selecting words that are made entirely of as-yet-unused letters. Each "loop" constitutes a single run through the entire shuffled dictionary.

By default the script will output the results of a single attempt whether or not it found a solution. To run multiple loops, you can use the `--loop` (or `-l`) flag with an integer argument. Omit the integer to run until you hit a solution.

You can also use the `--quiet` (or `-q`) flag to suppress some of the output. It's still a little noisy, though.
