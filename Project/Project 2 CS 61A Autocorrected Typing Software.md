# Project 2: CS 61A Autocorrected Typing Software

> Programmers dream of
> Abstraction, recursion, and
> Typing really fast.

## Introduction

In this project, you will write a program that measures typing speed. Additionally, you will implement typing autocorrect, which is a feature that attempts to correct the spelling of a word after a user types it. This project is inspired by [typeracer](https://play.typeracer.com/).

**Read each description thoroughly before starting to code.**

## Final Product

Our staff solution to the project can be interacted with at [cats.cs61a.org](https://cats.cs61a.org). If you'd like, feel free to try it out now. When you finish the project, you'll have implemented a significant part of this match yourself!

## Download starter files

You can download all of the project code as a [zip archive](https://cs61a.org/proj/cats/cats.zip). This project includes several files, but your changes will be made only to `cats.py`. Here are the files included in the archive:

- `cats.py`: The typing test logic.
- `utils.py`: Utility functions for interacting with files and strings.
- `ucb.py`: Utility functions for CS 61A projects.
- `data/sample_paragraphs.txt`: A file containing text samples to be typed.  These are  [scraped](https://github.com/kavigupta/wikivideos/blob/626de521e04ca643751ed85d549faca6ea528b1d/get_corpus.py)  Wikipedia articles about various topics.
- `data/common_words.txt`: A file containing common  [English words in order of frequency](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears.txt).
- `data/words.txt`: A file containing many more  [English words in order of frequency](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears.txt).
- `cats_gui.py`: A web server for the web-based graphical user interface (GUI).
- `gui_files`: A directory of files needed for the graphical user interface  (GUI).
- `multiplayer`: A directory of files needed to support multiplayer mode.
- `favicons`: A directory of icons.
- `images`: A directory of images.
- `ok`, `proj02.ok`, `tests`: Testing files.

## Logistics

> The project is worth 20 points. 17 points are assigned for correctness, 2 points for composition, and 1 point for submitting Phase 1 by the checkpoint deadline.

You will turn in the following files:

- `cats.py`

For the functions that we ask you to complete, there may be some initial code that we provide. If you would rather not use that code, feel free to delete it and start from scratch. You may also add new function definitions as you see fit.

However, please do **not** modify any other functions.  Doing so may result in your code failing our autograder tests. Also, please do not change any function signatures (names, argument order, or number of arguments).

Throughout this project, you should be testing the correctness of your code. **It is good practice to test often, so that it is easy to isolate any problems. However, you should not be testing *too* often, to allow yourself time to think through problems.**

If you do not want us to record a backup of your work or information about your progress, you can run

```
python3 ok --local
```

With this option, no information will be sent to our course servers. If you want to test your code interactively, you can run

```
 python3 ok -q [question number] -i 
```

with the appropriate question number (e.g. `01`) inserted. This will run the tests for that question until the first one you failed, then give you a chance to test the functions you wrote interactively.

You can also use the debugging print feature in OK by writing

```
 print("DEBUG:", x) 
```

which will produce an output in your terminal without causing OK tests to fail with extra output.

# Phase 1: Typing

### Problem 1 (1 pt)

Throughout the project, we will be making changes to functions in `cats.py`.

Implement `choose`. This function selects which paragraph the user will type. It takes three parameters:

- a list of `paragraphs` (strings)
- a `select` function, which returns `True` for paragraphs that can be selected
- a non-negative index `k`

The `choose` function returns the `k`th paragraph for which `select` returns `True`. If no such paragraph exists (because `k` is too large), then `choose` returns the empty string.

Before writing any code, unlock the tests to verify your understanding of the question.

```
Problem 1 > Suite 1 > Case 1
(cases remaining: 102)

>>> from cats import choose
>>> ps = ['short', 'really long', 'tiny']
>>> s = lambda p: len(p) <= 5
>>> choose(ps, s, 0) # remember to put quotes ('') around strings!
? 'short'
-- OK! --

>>> choose(ps, s, 1)
? 'tiny'
-- OK! --

>>> choose(ps, s, 2)
? ''
-- OK! --
```

### Problem 2 (1 pt)

Implement `about`, which takes a list of `topic` words. It returns a function which takes a paragraph and returns a boolean indicating whether that paragraph contains any of the words in `topic`.

Once we've implemented `about`, we'll be able to pass the returned function to `choose` as the `select` argument, which will be useful as we continue to implement our typing test.

To be able to make this comparison accurately, you will need to ignore case (that is, assume that uppercase and lowercase letters don't change what word it is) and punctuation in the paragraph. Additionally, only check for exact matches of the words in topic in the paragraph, not substrings. For example, "dogs" is not a match for the word "dog".

> **Hint**: You may use the string utility functions in `utils.py`. You can reference the docstrings of the utility functions to see how they are being used.

Before writing any code, unlock the tests to verify your understanding of the question.

```
Problem 2 > Suite 1 > Case 1
(cases remaining: 104)

>>> from cats import about
>>> from cats import choose
>>> dogs = about(['dogs', 'hounds'])
>>> dogs('A paragraph about cats.')
? False
-- OK! --

>>> dogs('A paragraph about dogs.')
? True
-- OK! --

>>> dogs('Release the Hounds!')
? True
-- OK! --

>>> dogs('"DOGS" stands for Department Of Geophysical Science.')
? True
-- OK! --

>>> dogs('Do gs and ho unds don\'t count')
? False
-- OK! --

>>> dogs("AdogsParagraph")
? True
-- Not quite. Try again! --

? False
-- OK! --
```

### Problem 3 (2 pts)

Implement `accuracy`, which takes a `typed` paragraph and a `reference` paragraph. It returns the percentage of words in `typed` that exactly match the corresponding words in `reference`. Case and punctuation must match as well. "Corresponding" here means that two words must occur at the same indices in `typed` and `reference`—the first words of both must match, the second words of both must match, and so on.

A *word* in this context is any sequence of characters separated from other words by whitespace, so treat "dog;" as a single word.

If `typed` is longer than `reference`, then the extra words in `typed` that have no corresponding word in `reference` are all incorrect.

If both `typed` and `reference` are empty, then the accuracy is 100.0. If `typed` is empty but `reference` is not empty, then the accuracy is zero. If `typed` is not empty but `reference` is empty, then the accuracy is zero.

Before writing any code, unlock the tests to verify your understanding of the question.

```
---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 1
(cases remaining: 103)

>>> from cats import accuracy
>>> accuracy("12345", "12345") # This should return 100.0 (not the integer 100!)
? 100.0
-- OK! --

>>> accuracy("a b c", "a b c")
? 100.0
-- OK! --

>>> accuracy("a  b  c  d", "b  a  c  d")
? 50.0
-- OK! --

>>> accuracy("a b", "c d e")
? 0.0
-- OK! --

>>> accuracy("Cat", "cat") # the function is case-sensitive
? 0.0
-- OK! --

>>> accuracy("a b c d", "a d")
? 25.0
-- OK! --

>>> accuracy("abc", " ")
? 0.0
-- OK! --

>>> accuracy("a b \tc" , "a b c") # Tabs don't count as words
? 100.0
-- OK! --

>>> accuracy("abc", "")
? 0.0
-- OK! --

>>> accuracy("", "abc")
? 0.0
-- OK! --

>>> accuracy("a b c d", "b c d")
? 0.0
-- OK! --

>>> accuracy("cats.", "cats") # punctuation counts
? 0.0
-- OK! --

>>> accuracy("", "") # Returns 100.0
? 100.0
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 03
```

👩🏽‍💻👨🏿‍💻 [Pair programming?](https://cs61a.org/articles/pair-programming) Remember to alternate between driver and navigator roles. The driver controls the keyboard; the navigator watches, asks questions, and suggests ideas.

### Problem 4 (1 pt)

Implement `wpm`, which computes the *words per minute*, a measure of typing speed, given a string `typed` and the amount of `elapsed` time in **seconds.** Despite its name, *words per minute* is not based on the number of words typed, but instead the number of groups of 5 characters, so that a typing test is not biased by the length of words. <u>The formula for *words per minute* is the ratio of the number of characters (including spaces) typed divided by 5 (a typical word length) to the elapsed time in **minutes.**</u>

For example, the string `"I am glad!"` contains three words and ten characters (not including the quotation marks). The words per minute calculation uses 2 as the number of words typed (because 10 / 5 = 2). If someone typed this string in 30 seconds (half a minute), their speed would be 4 words per minute.

Before writing any code, unlock the tests to verify your understanding of the question.

```
>>> from cats import wpm
>>> wpm("12345", 3) # Note: wpm returns a float (with a decimal point)
? 1.3
-- Not quite. Try again! --

? 0.3
-- Not quite. Try again! --

? 0.33
-- Not quite. Try again! --

? 20
-- Not quite. Try again! --

? 20.0
-- OK! --

>>> wpm("a b c", 20)
? 3.0
-- OK! --

>>> wpm("", 10)
? 0
-- Not quite. Try again! --

? 0.0
-- OK! --
```

**Time to test your typing speed!** You can use the command line to test your typing speed on paragraphs about a particular topic. For example, the command below will load paragraphs about cats or kittens. See the `run_typing_test` function for the implementation if you're curious (but it is defined for you).

```
python3 cats.py -t cats kittens
```

You can try out the web-based graphical user interface (GUI) using the following command. (You may have to use `Ctrl+C` or `Cmd+C` on your terminal to quit the GUI after you close the tab in your browser).

```
python3 cats_gui.py
```

👩🏽‍💻👨🏿‍💻 [Pair programming?](https://cs61a.org/articles/pair-programming) This would be a good time to switch roles. Switching roles makes sure that you both benefit from the learning experience of being in each role.

# Phase 2: Autocorrect

In the web-based GUI, there is an autocorrect button, but right now it doesn't do anything. Let's implement automatic correction of typos. Whenever the user presses the space bar, if the last word they typed doesn't match a word in the dictionary but is close to one, then that similar word will be substituted for what they typed.

### Problem 5 (2 pts)

Implement `autocorrect`, which takes a `typed_word`, a list of all `valid_words`, a `diff_function`, and a `limit`.

If the `typed_word` is contained inside the `valid_words` list, `autocorrect` returns that word.

*Otherwise*, `autocorrect` returns the word from `valid_words` that has the lowest difference from the provided `typed_word` based on the `diff_function`. However, if the lowest difference between `typed_word` and any of the `valid_words` is greater than `limit`, then `typed_word` is returned instead.

> **Important**: If `typed_word` is not contained inside `valid_words`, and multiple strings have the same lowest difference from `typed_word` according to the `diff_function`, `autocorrect` should return the string that appears first in `valid_words`.

A diff function takes in three arguments. The first two arguments are the two strings to be compared (the `typed_word` and a word from `valid_words`), and the third argument is the `limit`. The output of the diff function, which is a number, represents the amount of difference between the two strings.

Here is an example of a diff function that computes the minimum of `1 + limit` and the difference in length between the two input strings:

```
>>> def length_diff(w1, w2, limit):
...     return min(limit + 1, abs(len(w2) - len(w1)))
>>> length_diff('mellow', 'cello', 10)
1
>>> length_diff('hippo', 'hippopotamus', 5)
6
```

Assume that `typed_word` and all elements of `valid_words` are lowercase and have no punctuation.

> **Hint**: Try using `max` or `min` with the optional `key` argument.

Before writing any code, unlock the tests to verify your understanding of the question.

```
Problem 5 > Suite 1 > Case 1
(cases remaining: 104)

>>> from cats import autocorrect, lines_from_file
>>> abs_diff = lambda w1, w2, limit: abs(len(w2) - len(w1))
>>> autocorrect("cul", ["culture", "cult", "cultivate"], abs_diff, 10)
? 1
-- Not quite. Try again! --

? 'cult'
-- OK! --

>>> autocorrect("cul", ["culture", "cult", "cultivate"], abs_diff, 0)
? 'cul
-- Not quite. Try again! --

? 'cul'
-- OK! --

>>> autocorrect("wor", ["worry", "car", "part"], abs_diff, 10)
? 'worry'
-- Not quite. Try again! --

? 'car'
-- OK! --

>>> first_diff = lambda w1, w2, limit: 1 if w1[0] != w2[0] else 0
>>> autocorrect("wrod", ["word", "rod"], first_diff, 1)
? 'word'
-- OK! --

>>> autocorrect("inside", ["idea", "inside"], first_diff, 0.5)
? 'idea'
-- Not quite. Try again! --

? 'idea'
-- Not quite. Try again! --

? 'inside'
-- OK! --

>>> autocorrect("inside", ["idea", "insider"], first_diff, 0.5)
? 'idea'
-- OK! --

>>> autocorrect("outside", ["idea", "insider"], first_diff, 0.5)
? 'outside'
-- OK! --
```

### Problem 6 (2 pts)

Implement `feline_flips`, which is a diff function that takes two strings. It returns the minimum number of characters that must be changed in the `start` word in order to transform it into the `goal` word. If the strings are not of equal length, the difference in lengths is added to the total.

> **Important**: You may not use `while`, `for`, or list comprehensions in your implementation. Use recursion.

Here are some examples:

```
>>> big_limit = 10
>>> feline_flips("nice", "rice", big_limit)    # Substitute: n -> r
1
>>> feline_flips("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
2
>>> feline_flips("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
3
>>> feline_flips("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
5
>>> feline_flips("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
5
```

> **Important:** If the number of characters that must change is greater than `limit`, then `feline_flips` should return any number larger than `limit` and should minimize the amount of computation needed to do so.
>
> These two calls to `feline_flips` should take about the same amount of time to evaluate:
>
> ```
> >>> limit = 4
> >>> feline_flips("roses", "arose", limit) > limit
> True
> >>> feline_flips("rosesabcdefghijklm", "arosenopqrstuvwxyz", limit) > limit
> True
> ```

Before writing any code, unlock the tests to verify your understanding of the question.

```
Problem 6 > Suite 1 > Case 1
(cases remaining: 105)

>>> from cats import feline_flips, autocorrect
>>> import tests.construct_check as test
>>> big_limit = 10
>>> feline_flips("car", "cad", big_limit)
? 1
-- OK! --

>>> feline_flips("this", "that", big_limit)
? 2
-- OK! --

>>> feline_flips("one", "two", big_limit)
? 3
-- OK! --

>>> feline_flips("from", "form", big_limit)
? 2
-- OK! --

>>> feline_flips("awe", "awesome", big_limit)
? 4
-- OK! --

>>> feline_flips("someawe", "awesome", big_limit)
? 6
-- OK! --

>>> feline_flips("awful", "awesome", big_limit)
? 4
-- Not quite. Try again! --

? 5
-- OK! --

>>> feline_flips("awful", "awesome", 3) > 3
? True
-- OK! --

>>> feline_flips("awful", "awesome", 4) > 4
? true
-- Not quite. Try again! --

? True
-- OK! --

>>> feline_flips("awful", "awesome", 5) > 5
? False
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 06
```

Try turning on autocorrect in the GUI. Does it help you type faster? Are the corrections accurate? You should notice that inserting a letter or leaving one out near the beginning of a word is not handled well by this diff function. Let's fix that!

### Problem 7 (2 pts)

Implement `minimum_mewtations`, which is a diff function that returns the minimum number of edit operations needed to transform the `start` word into the `goal` word.

There are three kinds of edit operations, with some examples:

1. Add a letter to `start`.
   - Adding `"k"` to `"itten"` gives us `"kitten"`.
2. Remove a letter from `start`.
   - Removing `"s"` from `"scat"` givs us `"cat"`.
3. Substitute a letter in `start` for another.
   - Substituting `"z"` with `"j"` in `"zaguar"` gives us `"jaguar"`.

Each edit operation contributes 1 to the difference between two words.

```
>>> big_limit = 10
>>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
2
>>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
2
>>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
3
```

We have provided a template of an implementation in `cats.py`.

> **Hint:** This is a recursive function with three recursive calls. One of these recursive calls will be similar to the recursive call in `feline_flips`.

You may modify the template however you want or delete it entirely.

> **Important:** If the number of edits required is greater than `limit`, then `minimum_mewtations` should return any number larger than `limit` and should minimize the amount of computation needed to do so.
>
> These two calls to `minimum_mewtations` should take about the same amount of time to evaluate:
>
> ```
> >>> limit = 2
> >>> minimum_mewtations("ckiteus", "kittens", limit) > limit
> True
> >>> minimum_mewtations("ckiteusabcdefghijklm", "kittensnopqrstuvwxyz", limit) > limit
> True
> ```

Before writing any code, unlock the tests to verify your understanding of the question.

```
---------------------------------------------------------------------
Problem 7 > Suite 1 > Case 2
(cases remaining: 103)

>>> from cats import minimum_mewtations, autocorrect
>>> big_limit = 10
>>> minimum_mewtations("cats", "scat", big_limit)
? 2
-- OK! --

>>> minimum_mewtations("purng", "purring", big_limit)
? 2
-- OK! --

>>> minimum_mewtations("ckiteus", "kittens", big_limit)
? 2
-- Not quite. Try again! --

? 3
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 07
```

Try typing again. Are the corrections more accurate?

```
python3 cats_gui.py
```

👩🏽‍💻👨🏿‍💻 [Pair programming?](https://cs61a.org/articles/pair-programming) Celebrate, take a break, and switch roles!

### (Optional) Extension: final diff (0pt)

You may optionally design your own diff function called `final_diff`. Here are some ideas for making even more accurate corrections:

- Take into account which additions and deletions are more likely than others.  For example, it's much more likely that you'll accidentally leave out a  letter if it appears twice in a row.
- Treat two adjacent letters that have swapped positions as one change,  not two.
- Try to incorporate common misspellings.

You can also set the limit you'd like your diff function to use by changing the value of the variable `FINAL_DIFF_LIMIT` in `cats.py`.

You can check your `final_diff`'s success rate by running:

```
 python3 score.py
```

If you don't know where to start, try copy-pasting your code for `feline_flips` and `minimum_mewtations` into `final_diff` and scoring them. Looking at the typos they accidentally fixed might give you some ideas!

# Phase 3: Multiplayer

Typing is more fun with friends! You'll now implement multiplayer functionality, so that when you run `cats_gui.py` on your computer, it connects to the course server at [cats.cs61a.org](https://cats.cs61a.org) and looks for someone else to race against.

To race against a friend, 5 different programs will be running:

- Your GUI, which is a program that handles all the text coloring and display  in your web browser.
- Your `cats_gui.py`, which is a web server that communicates with your GUI using  the code you wrote in `cats.py`.
- Your opponent's `cats_gui.py`.
- Your opponent's GUI.
- The CS 61A multiplayer server, which matches players together and passes  messages around.

When you type, your GUI uploads what you have typed to your `cats_gui.py` server, which computes how much progress you have made and returns a progress update. It also uploads a progress update to the multiplayer server, so that your opponent's GUI can display it.

Meanwhile, your GUI display is always trying to keep current by asking for progress updates from `cats_gui.py`, which in turn requests that info from the multiplayer server.

Each player has an `id` number that is used by the server to track typing progress.

### Problem 8 (2 pts)

Implement `report_progress`, which is called every time the user finishes typing a word. It takes a list of the words `sofar`, a list of the words in the `prompt`, the user's `user_id`, and a `upload` function that is used to upload a progress report to the multiplayer server. There will never be more words in `sofar` than in `prompt`.

Your progress is a ratio of the words in the `prompt` that you have typed correctly, up to the first incorrect word, divided by the number of `prompt` words. For example, this example has a progress of `0.25`:

```
report_progress(["Hello", "ths", "is"], ["Hello", "this", "is", "wrong"], ...)
```

Your `report_progress` function should do two things: upload a message to the multiplayer server and return the progress of the player with `user_id`.

You can upload a message to the multiplayer server by calling the `upload` function on a two-element dictionary containing the keys `'id'` and `'progress'`. You should then return the player's progress, which is the ratio of words you computed.

> **Hint:** See the dictionary below for an example of a potential input into the `upload` function. This dictionary represents a player with `user_id` 1 and `progress` 0.6.
>
> ```
> {'id': 1, 'progress': 0.6}
> ```

Before writing any code, unlock the tests to verify your understanding of the question.

```
---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 1
(cases remaining: 102)

>>> from cats import report_progress
>>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
>>> typed = ['I', 'have', 'begun']
>>> prompt = ['I', 'have', 'begun', 'to', 'type']
>>> print_progress({'id': 1, 'progress': 0.6})
? ID: 1 Progress: 0.6
-- OK! --

>>> report_progress(typed, prompt, 1, print_progress) # print_progress is called on the report
(line 1)? ID: 1 Progress: 0.6
(line 2)? 0.6
-- OK! --

>>> report_progress(['I', 'begun'], prompt, 2, print_progress)
(line 1)? ID: 2 Progress: 0.2
(line 2)? 0.2
-- OK! --

>>> report_progress(['I', 'hve', 'begun', 'to', 'type'], prompt, 3, print_progress)
(line 1)? ID: 3 Progress: 0.8
-- Not quite. Try again! --

(line 1)? ID: 3 Progress: 0.2
(line 2)? 0.2
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 08
```

### Problem 9 (2 pts)

Implement `time_per_word`, which takes in a list `words` and `times_per_player`, a list of lists for each player with timestamps indicating when each player finished typing every individual word in `words`. It returns a `match` with the given information.

A `match` is a data abstraction that has a list of `words` and `times`. The `times` are stored as a list of lists of how long it took each player to type every word in `words`. Specifically, `times[i][j]` indicates how long it took player `i` to type `words[j]`.

For example, say `words = ['Hello', 'world']` and `times = [[5, 1], [4, 2]]`, then `[5, 1]` corresponds to the list of times for player 0, and `[4, 2]` corresponds to the list of times for player 1. Thus, player 0 took `5` units of time to write the word `'Hello'`.

> **Important**: Be sure to use the `match` constructor when returning a `match`. The tests will check that you are using the data abstraction rather than assuming a particular data format.
>
> Read the definitions for the `match` constructor and selectors in `cats.py` to learn more about how the data abstraction is implemented.

Timestamps are cumulative and always increasing, while the values in `times` are **differences between consecutive timestamps for each player**.

Here's an example: If `times_per_player = [[1, 3, 5], [2, 5, 6]]`, the corresponding `times` attribute of the `match` would be `[[2,2], [3, 1]]`. This is because the differences in timestamps are `(3-1)`, `(5-3)` for the first player and `(5-2)`, `(6-5)` for the second player. The first value of each list within `times_per_player` represents the initial starting time for each player.

Before writing any code, unlock the tests to verify your understanding of the question.

```
---------------------------------------------------------------------
Problem 9 > Suite 1 > Case 1
(cases remaining: 102)

>>> from cats import *
>>> p = [[1, 4, 6, 7], [0, 4, 6, 9]]
>>> words = ['This', 'is', 'fun']
>>> match = time_per_word(words, p)
>>> get_words(match)
? ['This', 'is', 'fun']
-- OK! --

>>> get_times(match)
? [[3, 2, 1], [4, 2, 3]]
-- OK! --

>>> p = [[0, 2, 3], [2, 4, 7]]
>>> match = time_per_word(['hello', 'world'], p)
>>> word_at(match, word_index=1)
? 'world'
-- OK! --

>>> get_times(match)
? [[2, 1], [2, 3]]
-- OK! --

>>> time(match, player_num=0, word_index=1)
? 1
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 09
```

👩🏽‍💻👨🏿‍💻 [Pair programming?](https://cs61a.org/articles/pair-programming) We suggest switching roles now, if you haven't recently. Almost done!

### Problem 10 (2 pts)

Implement `fastest_words`, which returns which words each player typed fastest. This function is called once both players have finished typing. It takes in a `match`.

Specifically, the `fastest_words` function returns a list of lists of words, one list for each player, and within each list the words they typed the fastest (against all the other players). In the case of a tie, consider the earliest player in the list (the smallest player index) to be the one who typed it the fastest.

For example consider the following match with the words 'Just', 'have', and 'fun'. Player 0 typed 'fun' the fastest (3 seconds), Player 1 typed 'Just' the fastest (4 seconds), and they tied on the word 'have' (both took 1 second) so we consider to Player 0 to be the fastest, because they are the earliest player in the list.

```
>>> player_0 = [5, 1, 3]
>>> player_1 = [4, 1, 6]
>>> fastest_words(match(['Just', 'have', 'fun'], [player_0, player_1]))
[['have', 'fun'], ['Just']]
```

The `match` argument is a `match` data abstraction, like the one returned in Problem 9. You can access words in the `match` with the selector `word_at`, which takes in a `match` and the `word_index` (an integer). With `word_at` you can access the time it took any player to type any word using `time`.

> **Important**: Be sure to use the `match` constructor when returning a `match`. The tests will check that you are using the data abstraction rather than assuming a particular data format.
>
> Make sure your implementation does not mutate the given player input lists. For the example above, calling `fastest_words` on `[player_0, player_1]` should **not** mutate `player_0` or `player_1`.

Before writing any code, unlock the tests to verify your understanding of the question.

```
---------------------------------------------------------------------
Problem 10 > Suite 1 > Case 1
(cases remaining: 103)

>>> from cats import match, fastest_words
>>> p0 = [2, 2, 3]
>>> p1 = [6, 1, 2]
>>> fastest_words(match(['What', 'great', 'luck'], [p0, p1]))
? [['What'], ['great', 'luck']]
-- OK! --

>>> p0 = [2, 2, 3]
>>> p1 = [6, 1, 3]
>>> fastest_words(match(['What', 'great', 'luck'], [p0, p1]))  # with a tie, choose the first player
? [['What', 'luck'], ['great']]
-- OK! --

>>> p2 = [4, 3, 1]
>>> fastest_words(match(['What', 'great', 'luck'], [p0, p1, p2]))
? [['What'], ['luck'], ['great']]
-- Not quite. Try again! --

? [['What'], ['great'], ['luck']]
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 10
```

Congratulations! Now you can play against other students in the course. Set `enable_multiplayer` to `True` near the bottom of `cats.py` and type swiftly!

```
python3 cats_gui.py
```

At this point, run the entire autograder to see if there are any tests that don't pass.

```
python3 ok
```

Check to make sure that you did all the problems by running:

```
python3 ok --score
```

​      