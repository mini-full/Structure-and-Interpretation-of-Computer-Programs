# Project 1: The Game of Hog

> I know! I'll use my
> Higher-order functions to
> Order higher rolls.

## Introduction

In this project, you will develop a simulator and multiple strategies for the dice game Hog. You will need to use *control statements* and *higher-order functions* together, as described in Sections 1.2 through 1.6 of [Composing Programs](http://composingprograms.com), the online textbook.

>  **Read each description thoroughly before starting to code.**

### Rules

In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points. On each turn, the current player chooses some number of dice to roll, up to 10. That player's score for the turn is the sum of the dice outcomes. However, a player who rolls too many dice risks:

- **Sow Sad**. If any of the dice outcomes is a 1, the current player's score  for the turn is `1`.
  - *Example 1:* The current player rolls 7 dice, 5 of which are 1's. They  score `1` point for the turn.
  - *Example 2:* The current player rolls 4 dice, all of which are 3's. Since  Sow Sad did not occur, they score `12` points for the turn.

In a normal game of Hog, those are all the rules. To spice up the game, we'll include some special rules:

- **Picky Piggy**. A player who chooses to roll zero dice scores the `n`th  digit of the decimal expansion of 1/7 (0.14285714...), where `n` is the  opponent's score. As a special case, if `n` is 0, the player scores 7 points.

  - *Example 1:* The current player rolls zero dice and the opponent has a score of 3.  The 3rd digit of the decimal expansion of 1/7 is 2: `0.14[2]85714285714285`,  The current player will receive `2` points.

  - *Example 2:* The current player rolls zero dice and the opponent has a score of 14.  The 14th digit of the decimal expansion of 1/7 is 4: `0.1428571428571[4]285`,  so the current player will receive `4` points.

  - *Example 3:* The current player rolls zero dice and the opponent has a score of 0.  The current player will receive `7` points.

**Hog Pile**. After points for the turn are added to the  current player's score, if the players' scores are the same, the current player's score doubles.

## Final product

You can try out the online Hog GUI with the staff solution to the project at [hog.cs61a.org](https://hog.cs61a.org). When you finish the project, you'll have implemented a significant part of this game yourself.

## Download starter files

To get started, download all of the project code as a [zip archive](https://cs61a.org/proj/hog/hog.zip). Below is a list of all the files you will see in the archive once unzipped. For the project, you'll only be making changes to `hog.py`.

- `hog.py`: A starter implementation of Hog
- `dice.py`: Functions for rolling dice
- `hog_gui.py`: A graphical user interface (GUI) for Hog (updated)
- `ucb.py`: Utility functions for CS 61A
- `ok`: CS 61A autograder
- `tests`: A directory of tests used by `ok`
- `gui_files`: A directory of various things used by the web GUI
- `calc.py`: A file you can use to approximately test your final strategy  (in progress)

You may notice some files other than the ones listed above too—those are needed for making the autograder and portions of the GUI work. Please do not modify any files other than `hog.py`.

## Logistics

You will turn in the following files:

- `hog.py`

You do not need to modify or turn in any other files to complete the project. To submit the project, run the following command:

```
python3 ok --submit
```

You will be able to view your submissions on the [Ok dashboard](http://ok.cs61a.org).

For the functions that we ask you to complete, there may be some initial code that we provide. If you would rather not use that code, feel free to delete it and start from scratch. You may also add new function definitions as you see fit.

However, please do **not** modify any other functions.  Doing so may result in your code failing our autograder tests. Also, please do not change any function signatures (names, argument order, or number of arguments).

Throughout this project, you should be testing the correctness of your code. It is good practice to test often, so that it is easy to isolate any problems. However, you should not be testing *too* often, to allow yourself time to think through problems.

We have provided an **autograder** called `ok` to help you with testing your code and tracking your progress. The first time you run the autograder, you will be asked to **log in with your Ok account using your web browser**. Please do so. Each time you run `ok`, it will back up your work and progress on our servers.

The primary purpose of `ok` is to test your implementations.

We recommend that you submit **after you finish each problem**. Only your last submission will be graded. It is also useful for us to have more backups of your code in case you run into a submission issue. **If you forget to submit, your last backup will be automatically converted to a submission.** 

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

## Graphical User Interface

A **graphical user interface** (GUI, for short) is provided for you. At the moment, it doesn't work because you haven't implemented the game logic. Once you complete the `play` function, you will be able to play a fully interactive version of Hog!

Once you've done that, you can run the GUI from your terminal:

```
python3 hog_gui.py
```

## Phase 1: Simulator

In the first phase, you will develop a simulator for the game of Hog.

### Problem 0 (0 pt)

The `dice.py` file represents dice using non-pure zero-argument functions. These functions are non-pure because they may have different return values each time they are called. The documentation of `dice.py` describes the two different types of dice used in the project:

- A **fair** dice produces each possible outcome with equal probability.  Two fair dice are already defined, `four_sided` and `six_sided`,  and are generated by the `make_fair_dice` function.
- A **test** dice is deterministic: it always cycles through a fixed sequence  of values that are passed as arguments.  Test dice are generated by  the `make_test_dice` function.

Before writing any code, read over the `dice.py` file and check your understanding by unlocking the following tests.

```
---------------------------------------------------------------------
Question 0 > Suite 1 > Case 1
(cases remaining: 2)

>>> from hog import *
>>> test_dice = make_test_dice(4, 1, 2)
>>> test_dice()
? 4
-- OK! --

>>> test_dice() # Second call
? 1
-- OK! --

>>> test_dice() # Third call
? 2
-- OK! --

>>> test_dice() # Fourth call
? 4
-- OK! --

---------------------------------------------------------------------
Question 0 > Suite 2 > Case 1
(cases remaining: 1)

Q: Which of the following is the correct way to "roll" a fair, six-sided die?
Choose the number of the correct choice:
0) six_sided()
1) make_fair_dice(6)
2) make_test_dice(6)
3) six_sided
? 1
-- Not quite. Try again! --

? 0
-- OK! --
```

You can exit the unlocker by typing `exit()`.

In general, for each of the unlocking tests, you might find it helpful to read through the provided skeleton for that problem before attempting the unlocking test.

### Problem 1 (2 pt)

Implement the `roll_dice` function in `hog.py`. It takes two arguments: a positive integer called `num_rolls` giving the number of dice to roll and a `dice` function. It returns the number of points scored by rolling the dice that number of times in a turn: either the sum of the outcomes or 1 *(Sow Sad)*.

- **Sow Sad**. If any of the dice outcomes is a 1, the current player's score for the turn is `1`.
  - *Example 1:* The current player rolls 7 dice, 5 of which are 1's. They  score `1` point for the turn.
  - *Example 2:* The current player rolls 4 dice, all of which are 3's. Since  Sow Sad did not occur, they score `12` points for the turn.

To obtain a single outcome of a dice roll, call `dice()`. You should call `dice()` exactly `num_rolls` times in the body of `roll_dice`. **Remember to call `dice()` exactly `num_rolls` times even if Sow Sad happens in the middle of rolling.** In this way, you correctly simulate rolling all the dice together.

**Understand the problem**:

Before writing any code, unlock the tests to verify your understanding of the question. **Note: you will not be able to test your code using `ok` until you unlock the test cases for the corresponding question**.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 1 > Suite 1 > Case 1
(cases remaining: 59)

>>> from hog import *
>>> roll_dice(2, make_test_dice(4, 6, 1))
? 4
-- Not quite. Try again! --

? 10
-- OK! --

---------------------------------------------------------------------
Question 1 > Suite 1 > Case 2
(cases remaining: 58)

>>> from hog import *
>>> roll_dice(3, make_test_dice(4, 6, 1))
? 1
-- OK! --

---------------------------------------------------------------------
Question 1 > Suite 1 > Case 3
(cases remaining: 57)

>>> from hog import *
>>> roll_dice(4, make_test_dice(2, 2, 3))
? 9
-- OK! --

---------------------------------------------------------------------
Question 1 > Suite 1 > Case 4
(cases remaining: 56)

>>> from hog import *
>>> a = roll_dice(4, make_test_dice(1, 2, 3))
>>> a # check that the value is being returned, not printed
? 1
-- OK! --

---------------------------------------------------------------------
Question 1 > Suite 1 > Case 5
(cases remaining: 55)

>>> from hog import *
>>> counted_dice = make_test_dice(4, 1, 2, 6)
>>> roll_dice(3, counted_dice)
? 1
-- OK! --

>>> # Make sure you call dice exactly num_rolls times!
>>> # If you call it fewer or more than that, it won't be at the right spot in the cycle for the next roll
>>> # Note that a return statement within a loop ends the loop
>>> roll_dice(1, counted_dice)
? 6
-- OK! --

---------------------------------------------------------------------
Question 1 > Suite 1 > Case 6
(cases remaining: 54)

>>> from hog import *
>>> roll_dice(9, make_test_dice(6))
? 54
-- OK! --

>>> roll_dice(7, make_test_dice(2, 2, 2, 2, 2, 2, 1))
? 1
-- OK! --
```

**Write code and check your work**:

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 01
```

#### Debugging Tips

If the tests don't pass, it's time to debug. You can observe the behavior of your function using Python directly. First, start the Python interpreter and load the `hog.py` file.

```
python3 -i hog.py
```

Then, you can call your `roll_dice` function on any number of dice you want. The `roll_dice` function has a [default argument value](http://composingprograms.com/pages/14-designing-functions.html#default-argument-values) for `dice` that is a random six-sided dice function. Therefore, the following call to `roll_dice` simulates rolling four fair six-sided dice.

```
>>> roll_dice(4)
```

You will find that the previous expression may have a different result each time you call it, since it is simulating random dice rolls. You can also use test dice that fix the outcomes of the dice in advance. For example, rolling twice when you know that the dice will come up 3 and 4 should give a total outcome of 7.

```
>>> fixed_dice = make_test_dice(3, 4)
>>> roll_dice(2, fixed_dice)
7
```

> On most systems, you can evaluate the same expression again by pressing the up arrow, then pressing enter or return. To evaluate earlier commands, press the up arrow repeatedly.
>
> If you find a problem, you need to change your `hog.py` file, save it, quit Python, start Python again, and then start evaluating expressions. Pressing the up arrow should give you access to your previous expressions, even after restarting Python.

Continue debugging your code and running the `ok` tests until they all pass. You should follow this same procedure of **<u>understanding the problem, implementing a solution, testing, and debugging</u>** for all the problems in this project.

> One more debugging tip: to start the interactive interpreter automatically upon failing an `ok` test, use `-i`. For example, `python3 ok -q 01 -i` will run the tests for question 1, then start an interactive interpreter with `hog.py` loaded if a test fails.

### Problem 2 (3 pt)

Implement `picky_piggy`, which takes the opponent's current `score` and returns the number of points scored by rolling 0 dice.

- **Picky Piggy**. A player who chooses to roll zero dice scores the `n`th  digit of the decimal expansion of 1/7 (0.14285714...), where `n` is the  opponent's score. As a special case, if `n` is 0, the player scores 7 points.
  - *Example 1:* The current player rolls zero dice and the opponent has a score of 3.  The 3rd digit of the decimal expansion of 1/7 is 2: `0.14[2]85714285714285`,  The current player will receive `2` points.
  - *Example 2:* The current player rolls zero dice and the opponent has a score of 14.  The 14th digit of the decimal expansion of 1/7 is 4: `0.1428571428571[4]285`,  so the current player will receive `4` points.
  - *Example 3:* The current player rolls zero dice and the opponent has a score of 0.  The current player will receive `7` points.

The goal of this question is for you to practice retrieving the digits of a number, so it may be helpful to keep in mind the techniques used in previous assignments for digit iteration.

However, your code should not use `str`, lists, or contain square brackets `[` `]` in your implementation. Aside from this constraint, you can otherwise implement this function how you would like to.

> **Note:** Remember to remove the `"*** YOUR CODE HERE ***"` string from the function once you've implemented it so that you're not getting an unintentional `str` check error.
>
> If the syntax check isn't passing on the docstring, try upgrading your Python version to 3.8 or 3.9. It seems that the docstring being included in the check is specific to Python version 3.7, so updating your Python version should resolve the issue.
>
> **Hint:** The decimal expansion of 1/7 is a 6-digit repeating decimal with the digits 142857. Therefore, the 2nd digit is the same as the 8th digit, the 14th, 20th, 26th, 32nd, etc.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 2 > Suite 1 > Case 1
(cases remaining: 36)

>>> from hog import *
>>> import tests.construct_check as test
>>> picky_piggy(0)
? 1
-- Not quite. Try again! --

? 7
-- OK! --

---------------------------------------------------------------------
Question 2 > Suite 1 > Case 2
(cases remaining: 35)

>>> from hog import *
>>> import tests.construct_check as test
>>> picky_piggy(1)
? 1
-- OK! --

---------------------------------------------------------------------
Question 2 > Suite 1 > Case 3
(cases remaining: 34)

>>> from hog import *
>>> import tests.construct_check as test
>>> picky_piggy(2)
? 4
-- OK! --

---------------------------------------------------------------------
Question 2 > Suite 1 > Case 4
(cases remaining: 33)

>>> from hog import *
>>> import tests.construct_check as test
>>> picky_piggy(5)
? 5
-- OK! --

---------------------------------------------------------------------
Question 2 > Suite 1 > Case 5
(cases remaining: 32)

>>> from hog import *
>>> import tests.construct_check as test
>>> a = picky_piggy(24)
>>> a # check that the value is being returned, not printed
? 7
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 02
```

You can also test `picky_piggy` interactively by entering `python3 -i hog.py` in the terminal and then calling `picky_piggy` with various inputs.

### Problem 3 (2 pt)

Implement the `take_turn` function, which returns the number of points scored for a turn by rolling the given `dice` `num_rolls` times.

Your implementation of `take_turn` should call both `roll_dice` and `picky_piggy` when possible.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 3 > Suite 1 > Case 1
(cases remaining: 10)

>>> from hog import *
>>> take_turn(2, 0, make_test_dice(4, 5, 1))
? 9
-- OK! --

---------------------------------------------------------------------
Question 3 > Suite 1 > Case 2
(cases remaining: 9)

>>> from hog import *
>>> take_turn(3, 0, make_test_dice(4, 6, 1))
? 1
-- OK! --

---------------------------------------------------------------------
Question 3 > Suite 1 > Case 3
(cases remaining: 8)

>>> from hog import *
>>> take_turn(0, 2)
? 7
-- Not quite. Try again! --

? 4
-- OK! --

---------------------------------------------------------------------
Question 3 > Suite 1 > Case 4
(cases remaining: 7)

>>> from hog import *
>>> take_turn(0, 0)
? 7
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 03
```

[Pair programming?](https://cs61a.org/articles/pair-programming) Remember to alternate between driver and navigator roles. The driver controls the keyboard; the navigator watches, asks questions, and suggests ideas.

### Problem 4 (1 pt)

Implement `hog_pile`, which takes the current player and opponent scores and returns the points that the current player will receive due to Hog Pile. If Hog Pile is not applicable, the current player could also recieve 0 additional points.

- **Hog Pile**. After points for the turn are added to  the current player's score, if the players' scores are the same, the  current player's score doubles.
  - *Example:*
    - Both players start out at 0. (0, 0)
    - Player 0 rolls 2 dice and gets `5` points. (5, 0)
    - Player 1 rolls 1 dice and gets `5` points. Player 1's score doubles. (5, 10)
    - Player 0 rolls 2 dice and gets `6` points. (11, 10)
    - Player 1 rolls 8 dice and gets `1` points. Player 1's score doubles. (11, 22)

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 1
(cases remaining: 107)

>>> from hog import *
>>> hog_pile(25, 43)
? 0
-- OK! --

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 2
(cases remaining: 106)

>>> from hog import *
>>> hog_pile(32, 33)
? 0
-- OK! --

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 3
(cases remaining: 105)

>>> from hog import *
>>> hog_pile(7, 7)
? 14
-- Not quite. Try again! --

? 7
-- OK! --

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 4
(cases remaining: 104)

>>> from hog import *
>>> hog_pile(26, 26)
? 26
-- OK! --

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 5
(cases remaining: 103)

>>> from hog import *
>>> hog_pile(23, 23)
? 23
-- OK! --

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 6
(cases remaining: 102)

>>> from hog import *
>>> hog_pile(193, 42)
? 0
-- OK! --

---------------------------------------------------------------------
Question 4 > Suite 1 > Case 7
(cases remaining: 101)

>>> from hog import *
>>> a = hog_pile(187, 187)
>>> a # check that the value is being returned, not printed
? 187
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 04
```

### Problem 5 (4 pt)

Implement the `play` function, which simulates a full game of Hog. Players take turns rolling dice until one of the players reaches the `goal` score. A turn is defined as one roll of the dice.

To determine how many dice are rolled each turn, each player uses their respective strategy (Player 0 uses `strategy0` and Player 1 uses `strategy1`). A *strategy* is a function that, given a player's score and their opponent's score, returns the number of dice that the current player will roll in the turn. Don't worry about implementing strategies yet; you'll do that in Phase 3.

> **Important:** Your implementation should only need to use a single loop; you don't need multiple loops. This might not affect passing the test cases if your logic is correct overall, but this could affect your [composition](https://cs61a.org/articles/composition/) grade for the project. Here's the section of the syllabus on composition for [projects](https://cs61a.org/articles/about#projects).
>
> Additionally, each strategy function should be called only once per turn. This means you only want to call `strategy0` when it is Player 0's turn and only call `strategy1` when it is Player 1's turn. Otherwise, the GUI and some `ok` tests may get confused.

If a player achieves the goal score by the end of their turn, i.e. after all applicable rules have been applied, the game ends. `play` will then return the final total scores of both players, with Player 0's score first and Player 1's score second.

> **Hints**:
>
> - You should call the functions you have implemented already.
> - Call `take_turn` with four arguments (don't forget to pass in the `goal`).  Only call `take_turn` once per turn.
> - Call `hog_pile` to determine if the current player will gain additional  points due to Hog Pile, and if so, how many points.
> - You can get the number of the next player (either 0 or 1) by calling the  provided function `next_player`.
> - You can ignore the `say` argument to the `play` function for now. You will  use it in Phase 2 of the project.
> - For the unlocking tests, `hog.always_roll` refers to the `always_roll`  function defined in `hog.py`.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 5 > Suite 1 > Case 1
(cases remaining: 110)

Q: The variables score0 and score1 are the scores for Player 0
and Player 1, respectively. Under what conditions should the
game continue?
Choose the number of the correct choice:
0) While score1 is less than goal
1) While at least one of score0 or score1 is less than goal
2) While score0 and score1 are both less than goal
3) While score0 is less than goal
? 2
-- OK! --

---------------------------------------------------------------------
Question 5 > Suite 1 > Case 2
(cases remaining: 109)

Q: What is a strategy in the context of this game?
Choose the number of the correct choice:
0) A player's desired turn outcome
1) A function that returns the number of dice a player will roll
2) The number of dice a player will roll
? 1
-- OK! --

---------------------------------------------------------------------
Question 5 > Suite 1 > Case 3
(cases remaining: 108)

Q: If strategy1 is Player 1's strategy function, score0 is
Player 0's current score, and score1 is Player 1's current
score, then which of the following demonstrates correct
usage of strategy1?
Choose the number of the correct choice:
0) strategy1(score1)
1) strategy1(score0, score1)
2) strategy1(score0)
3) strategy1(score1, score0)
? 1
-- Not quite. Try again! --

Choose the number of the correct choice:
0) strategy1(score1)
1) strategy1(score0, score1)
2) strategy1(score0)
3) strategy1(score1, score0)
? 3
-- OK! --

---------------------------------------------------------------------
Question 5 > Suite 2 > Case 1
(cases remaining: 107)

>>> import hog
>>> always_three = hog.make_test_dice(3)
>>> always = hog.always_roll
>>> #
>>> # Play function stops at goal
>>> s0, s1 = hog.play(always(5), always(3), score0=91, score1=10, dice=always_three)
>>> s0
? 241
-- Not quite. Try again! --

? 106
-- OK! --

>>> s1
? 10
-- OK! --

---------------------------------------------------------------------
Question 5 > Suite 2 > Case 2
(cases remaining: 106)

>>> import hog
>>> always_three = hog.make_test_dice(3)
>>> always = hog.always_roll
>>> #
>>> # Goal score is not hardwired
>>> s0, s1 = hog.play(always(5), always(5), goal=10, dice=always_three)
>>> s0
? 15
-- OK! --

>>> s1
? 0
-- OK! --

---------------------------------------------------------------------
Question 5 > Suite 2 > Case 3
(cases remaining: 105)

-- Already unlocked --

---------------------------------------------------------------------
Question 5 > Suite 3 > Case 1
(cases remaining: 104)

>>> import hog
>>> always_three = hog.make_test_dice(3)
>>> always_seven = hog.make_test_dice(7)
>>> #
>>> # Use strategies
>>> # We recommend working this out turn-by-turn on a piece of paper (use Python for difficult calculations).
>>> strat0 = lambda score, opponent: opponent % 10
>>> strat1 = lambda score, opponent: max((score // 10) - 4, 0)
>>> s0, s1 = hog.play(strat0, strat1, score0=71, score1=80, dice=always_seven)
>>> s0
? 99
-- Not quite. Try again! --

? 75
-- OK! --

>>> s1
? 108
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 05
```

Once you are finished, you will be able to play a graphical version of the game. We have provided a file called `hog_gui.py` that you can run from the terminal:

```
python3 hog_gui.py
```

> Note: The GUI has been updated. See the announcement at the top of the page for instructions.

The GUI relies on your implementation, so if you have any bugs in your code, they will be reflected in the GUI. This means you can also use the GUI as a debugging tool; however, it's better to run the tests first.

Make sure to submit your work so far before the checkpoint deadline:

```
python3 ok --submit
```

Check to make sure that you did all the problems in Phase 1:

```
python3 ok --score
```

**Congratulations! You have finished Phase 1 of this project!**

[Pair programming?](https://cs61a.org/articles/pair-programming) This would be a good time to switch roles. Switching roles makes sure that you both benefit from the learning experience of being in each role.

## Phase 2: Commentary

In the second phase, you will implement commentary functions that print remarks about the game after each turn, such as: `"22 point(s)! That's a record gain for Player 1!"`

A commentary function takes two arguments, Player 0's current score and Player 1's current score. It can print out commentary based on either or both current scores and any other information in its parent environment. Since commentary can differ from turn to turn depending on the current point situation in the game, a commentary function always returns another commentary function to be called on the next turn. The only side effect of a commentary function should be to print.

### Commentary examples

The function `say_scores` in `hog.py` is an example of a commentary function that simply announces both players' scores. Note that `say_scores` returns itself, meaning that the same commentary function will be called each turn.

```
def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores
```

The function `announce_lead_changes` is an example of a higher-order function that returns a commentary function that tracks lead changes. A different commentary function will be called each turn.

```
def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say
```

You should also understand the function `both`, which takes two commentary functions (`f` and `g`) and returns a *new* commentary function. This returned commentary function returns *another* commentary function which calls the functions returned by calling `f` and `g`, in that order.

```
def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say
```

### Problem 6 (1 pt)

Update your `play` function so that a commentary function is called at the end of each turn. The return value of calling a commentary function gives you the commentary function to call on the next turn.

For example, `say(score0, score1)` should be called at the end of the first turn. Its return value (another commentary function) should be called at the end of the second turn. Each consecutive turn, call the function that was returned by the call to the previous turn's commentary function.

> **Hint:** For the unlocking tests for this problem, remember that when calling `print` with multiple arguments, Python will put a space between each of the arguments. For example:
>
> ```
> >>> print(9, 12)
> 9 12
> ```

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 6 > Suite 1 > Case 1
(cases remaining: 7)

Q: What does a commentary function return?
Choose the number of the correct choice:
0) An integer representing the score.
1) None.
2) Another commentary function.
? 2
-- OK! --

---------------------------------------------------------------------
Question 6 > Suite 2 > Case 1
(cases remaining: 6)

>>> from hog import play, always_roll
>>> from dice import make_test_dice
>>> #
>>> def echo(s0, s1):
...     print(s0, s1)
...     return echo
>>> s0, s1 = play(always_roll(1), always_roll(1), dice=make_test_dice(3), goal=5, say=echo)
(line 1)? 3 0
(line 2)? 3 6
-- OK! --

---------------------------------------------------------------------
Question 6 > Suite 2 > Case 2
(cases remaining: 5)

>>> from hog import play, always_roll
>>> from dice import make_test_dice
>>> def count(n):
...     def say(s0, s1):
...         print(n, s0)
...         return count(n + 1)
...     return say
>>> s0, s1 = play(always_roll(1), always_roll(1), dice=make_test_dice(5), goal=15, say=count(1))
(line 1)? 1 5
(line 2)? 2 5
(line 3)? 3 20
-- OK! --

---------------------------------------------------------------------
Question 6 > Suite 2 > Case 3
(cases remaining: 4)

>>> from hog import play, always_roll
>>> from dice import make_test_dice
>>> #
>>> def echo(s0, s1):
...     print(s0, s1)
...     return echo
>>> strat0 = lambda score, opponent: 1 - opponent // 10
>>> strat1 = always_roll(3)
>>> s0, s1 = play(strat0, strat1, dice=make_test_dice(4, 2, 6), goal=15, say=echo)
(line 1)? 4 0
(line 2)? 4 6
-- Not quite. Try again! --

(line 1)? 4 0
(line 2)? 4 12
(line 3)? 11 12
(line 4)? 11 24
-- OK! --

---------------------------------------------------------------------
Question 6 > Suite 2 > Case 4
(cases remaining: 3)

>>> from hog import play, always_roll
>>> from dice import make_test_dice
>>> #
>>> # Ensure that say is properly updated within the body of play
>>> def total(s0, s1):
...     print(s0 + s1)
...     return echo
>>> def echo(s0, s1):
...     print(s0, s1)
...     return total
>>> s0, s1 = play(always_roll(1), always_roll(1), dice=make_test_dice(2, 5), goal=10, say=echo)
(line 1)? 2 0
(line 2)? 7
(line 3)? 4 5
(line 4)? 14
-- OK! --

---------------------------------------------------------------------
Question 6 > Suite 3 > Case 1
(cases remaining: 2)

>>> from hog import play, always_roll, both, announce_lead_changes, say_scores
>>> from dice import make_test_dice
>>> #
>>> def echo_0(s0, s1):
...     print('*', s0)
...     return echo_0
>>> def echo_1(s0, s1):
...     print('**', s1)
...     return echo_1
>>> s0, s1 = play(always_roll(1), always_roll(1), dice=make_test_dice(2), goal=5, say=both(echo_0, echo_1))
(line 1)? * 2
(line 2)? ** 0
(line 3)? * 2
(line 4)? ** 4
(line 5)? * 8
(line 6)? ** 4
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 06
```

### Problem 7 (3 pt)

Implement the `announce_highest` function, which is a higher-order function that returns a commentary function. This commentary function announces whenever a particular player gains more points in a turn than ever before. For example, `announce_highest(1)` ignores Player 0 entirely and just prints information about Player 1. (So does its return value; another commentary function about only Player 1.)

To compute the gain, it must compare the score from last turn (`last_score`) to the score from this turn for the player of interest (designated by the `who` argument). This function must also keep track of the highest gain for the player so far, which is stored as `running_high`.

The way in which `announce_highest` announces is very specific, and your implementation should match the doctests provided. Don't worry about singular versus plural when announcing point gains; you should simply use "point(s)" for both cases.

> **Hint:** The `announce_lead_changes` function provided to you is an example of how to keep track of information using commentary functions. If you are stuck, first make sure you understand how `announce_lead_changes` works.

> **Hint:** If you're getting a `local variable [var] reference before assignment` error:
>
> This happens because in Python, you aren't normally allowed to modify variables defined in parent frames. Instead of reassigning `[var]`, the interpreter thinks you're trying to define a new variable within the current frame. We'll learn about how to work around this in a future lecture, but it is not required for this problem.
>
> To fix this, you have two options:
>
> 1) Rather than reassigning `[var]` to its new value, create a new variable to hold that new value. Use that new variable in future calculations.
>
> 2) For this problem specifically, avoid this issue entirely by not using assignment statements at all. Instead, pass new values in as arguments to a call to `announce_highest`.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 7 > Suite 1 > Case 1
(cases remaining: 5)

Q: What does announce_highest return?
Choose the number of the correct choice:
0) A string containing the largest point increase for the
   current player.
1) The current largest point increase between both
   players.
2) A commentary function that prints information about the
   biggest point increase for the current player.
? 2
-- OK! --

---------------------------------------------------------------------
Question 7 > Suite 1 > Case 2
(cases remaining: 4)

Q: When does the commentary function returned by announce_highest
print something out?
Choose the number of the correct choice:
0) After each turn.
1) When the current player, given by the parameter `who`,
   earns the biggest point increase yet between both
   players in the game.
2) When the current player, given by the parameter `who`,
   earns their biggest point increase yet in the game.
? 2
-- OK! --

---------------------------------------------------------------------
Question 7 > Suite 1 > Case 3
(cases remaining: 3)

Q: What does the parameter last_score represent?
Choose the number of the correct choice:
0) The relevant player's score before this turn.
1) The opponent's score before this turn.
2) The last highest gain for the current player.
? 0
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 07
```

When you are done, you will see commentary in the GUI:

```
python3 hog_gui.py
```

The commentary in the GUI is generated by passing the following function as the `say` argument to `play`.

```
both(announce_highest(0), both(announce_highest(1), announce_lead_changes()))
```

Great work! You just finished Phase 2 of the project!

[Pair programming?](https://cs61a.org/articles/pair-programming) Celebrate, take a break, and switch roles!

## Phase 3: Strategies

In the third phase, you will experiment with ways to improve upon the basic strategy of always rolling a fixed number of dice. First, you need to develop some tools to evaluate strategies.

### Problem 8 (2 pt)

Implement the `make_averaged` function, which is a higher-order function that takes a function `original_function` as an argument.

The return value of `make_averaged` is a function that takes in the same number of arguments as `original function`. When we call this returned function on arguments, it will return the average value of repeatedly calling `original_function` on the arguments passed in.

Specifically, this function should call `original_function` a total of `trials_count` times and return the average of the results of these calls.

> **Important:** To implement this function, you will need to use a new piece of Python syntax. We would like to write a function that accepts an arbitrary number of arguments, and then calls another function using exactly those arguments. Here's how it works.
>
> Instead of listing formal parameters for a function, you can write `*args`, which represents all of the **arg**ument**s** that get passed into the function. We can then call another function with these same arguments by passing these `*args` into this other function. For example:
>
> ```
> >>> def printed(f):
> ...     def print_and_return(*args):
> ...         result = f(*args)
> ...         print('Result:', result)
> ...         return result
> ...     return print_and_return
> >>> printed_pow = printed(pow)
> >>> printed_pow(2, 8)
> Result: 256
> 256
> >>> printed_abs = printed(abs)
> >>> printed_abs(-10)
> Result: 10
> 10
> ```
>
> Here, we can pass any number of arguments into `print_and_return` via the `*args` syntax. We can also use `*args` inside our `print_and_return` function to make another function call with the same arguments.

Read the docstring for `make_averaged` carefully to understand how it is meant to work.

Before writing any code, unlock the tests to verify your understanding of the question.

```python
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 8 > Suite 1 > Case 1
(cases remaining: 7)

Q: What is one reason that make_averaged is a higher order function?
Choose the number of the correct choice:
0) It uses the *args keyword
1) It calls a function that is not itself
2) It contains a nested function
3) It takes in a function as an argument
? 3
-- OK! --

---------------------------------------------------------------------
Question 8 > Suite 1 > Case 2
(cases remaining: 6)

Q: How many arguments does the function passed into make_averaged take?
Choose the number of the correct choice:
0) An arbitrary amount, which is why we need to use *args to call it
1) Two
2) None
? 0
-- OK! --

---------------------------------------------------------------------
Question 8 > Suite 2 > Case 1
(cases remaining: 5)

>>> from hog import *
>>> dice = make_test_dice(3, 1, 5, 6)
>>> averaged_dice = make_averaged(dice, 1000)
>>> # Average of calling dice 1000 times
>>> averaged_dice()
? 3.75
-- OK! --

---------------------------------------------------------------------
Question 8 > Suite 2 > Case 2
(cases remaining: 4)

>>> from hog import *
>>> dice = make_test_dice(3, 1, 5, 6)
>>> averaged_roll_dice = make_averaged(roll_dice, 1000)
>>> # Average of calling roll_dice 1000 times
>>> # Enter a float (e.g. 1.0) instead of an integer
>>> averaged_roll_dice(2, dice)
? 7.5
-- Not quite. Try again! --
# Because of Sow Sad, The points we get should be 1 and 11.
? 6.0
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 08
```

### Problem 9 (2 pt)

Implement the `max_scoring_num_rolls` function, which runs an experiment to determine the number of rolls (from 1 to 10) that gives the maximum average score for a turn. Your implementation should use `make_averaged` and `roll_dice`.

If two numbers of rolls are tied for the maximum average score, return the lower number. For example, if both 3 and 6 achieve a maximum average score, return 3.

You might find it useful to read the doctest and the example shown in the doctest for this problem before doing the unlocking test.

> **Important:** In order to pass all of our tests, please make sure that you are testing dice rolls starting from 1 going up to 10, rather than starting from 10 to 1.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 9 > Suite 1 > Case 1
(cases remaining: 9)

Q: If multiple num_rolls are tied for the highest scoring
average, which should you return?
Choose the number of the correct choice:
0) The highest num_rolls
1) A random num_rolls
2) The lowest num_rolls
? 2
-- OK! --

---------------------------------------------------------------------
Question 9 > Suite 2 > Case 1
(cases remaining: 8)

>>> from hog import *
>>> dice = make_test_dice(3)   # dice always returns 3
>>> max_scoring_num_rolls(dice, trials_count=1000)
? 10
-- OK! --

---------------------------------------------------------------------
Question 9 > Suite 3 > Case 1
(cases remaining: 5)

>>> from hog import *
>>> dice = make_test_dice(2)     # dice always rolls 2
>>> max_scoring_num_rolls(dice, trials_count=1000)
? 10
-- OK! --

---------------------------------------------------------------------
Question 9 > Suite 3 > Case 2
(cases remaining: 4)

>>> from hog import *
>>> dice = make_test_dice(1, 2)  # dice alternates 1 and 2
>>> max_scoring_num_rolls(dice, trials_count=1000)
? 1
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 09
```

**Running experiments:**

To run this experiment on randomized dice, call `run_experiments` using the `-r` option:

```
python3 hog.py -r
```

For the remainder of this project, you can change the implementation of `run_experiments` as you wish.  The function includes calls to `average_win_rate` for evaluating various Hog strategies, but most of the calls are currently commented out. You can un-comment the calls to try out strategies, like to compare the win rate for `always_roll(8)` to the win rate for `always_roll(6)`.

Some of the experiments may take up to a minute to run. You can always reduce the number of trials in your call to `make_averaged` to speed up experiments.

Running experiments won't affect your score on the project.

[Pair programming?](https://cs61a.org/articles/pair-programming) We suggest switching roles now, if you haven't recently. Almost done!

### Problem 10 (1 pt)

A strategy can try to take advantage of the *Picky Piggy* rule by rolling 0 when it is most beneficial to do so. Implement `picky_piggy_strategy`, which returns 0 whenever rolling 0 would give **at least** `cutoff` points and returns `num_rolls` otherwise.

> **Hint**: You can use the function `picky_piggy` you defined in Problem 2.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 10 > Suite 1 > Case 1
(cases remaining: 106)

>>> from hog import *
>>> picky_piggy_strategy(0, 4, cutoff=7, num_rolls=5)
? 0
-- OK! --

---------------------------------------------------------------------
Question 10 > Suite 1 > Case 2
(cases remaining: 105)

>>> from hog import *
>>> picky_piggy_strategy(9, 0, cutoff=6, num_rolls=5)
? 7
-- Not quite. Try again! --

? 0
-- OK! --

---------------------------------------------------------------------
Question 10 > Suite 1 > Case 3
(cases remaining: 104)

>>> from hog import *
>>> picky_piggy_strategy(50, 3, cutoff=7, num_rolls=5)
? 5
-- OK! --

---------------------------------------------------------------------
Question 10 > Suite 1 > Case 4
(cases remaining: 103)

>>> from hog import *
>>> picky_piggy_strategy(32, 0, cutoff=8, num_rolls=4)
? 4
-- OK! --

---------------------------------------------------------------------
Question 10 > Suite 1 > Case 5
(cases remaining: 102)

>>> from hog import *
>>> picky_piggy_strategy(20, 0, cutoff=1, num_rolls=4)
? 0
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 10
```

Once you have implemented this strategy, change `run_experiments` to evaluate your new strategy against the baseline. Is this strategy an improvement over the baseline?

### Problem 11 (1 pt)

A strategy can also take advantage of the *Hog Pile* rules. The Hog Pile strategy always rolls 0 if doing so triggers the rule. In other cases, it rolls 0 if rolling 0 would give **at least** `cutoff` points. Otherwise, the strategy rolls `num_rolls`.

> **Hint**: You can use the function `picky_piggy_strategy` you defined in Problem 10.
>
> **Hint**: Remember that the `hog_pile` check should be done after the points from `picky_piggy` have been added to the score.

Before writing any code, unlock the tests to verify your understanding of the question.

```
=====================================================================
Assignment: Project 1: Hog
OK, version v1.18.1
=====================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlocking tests

At each "? ", type what you would expect the output to be.
Type exit() to quit

---------------------------------------------------------------------
Question 11 > Suite 1 > Case 1
(cases remaining: 105)

>>> from hog import *
>>> hog_pile_strategy(2, 10, cutoff=10, num_rolls=6)
? 0
-- OK! --

---------------------------------------------------------------------
Question 11 > Suite 1 > Case 2
(cases remaining: 104)

>>> from hog import *
>>> hog_pile_strategy(30, 54, cutoff=10, num_rolls=6)
? 6
-- OK! --

---------------------------------------------------------------------
Question 11 > Suite 1 > Case 3
(cases remaining: 103)

>>> from hog import *
>>> hog_pile_strategy(20, 36, cutoff=7, num_rolls=6)
? 6
-- Not quite. Try again! --

? 0
-- OK! --

---------------------------------------------------------------------
Question 11 > Suite 1 > Case 4
(cases remaining: 102)

>>> from hog import *
>>> hog_pile_strategy(24, 5, cutoff=8, num_rolls=6)
? 6
-- OK! --
```

Once you are done unlocking, begin implementing your solution. You can check your correctness with:

```
python3 ok -q 11
```

Once you have implemented this strategy, update `run_experiments` to evaluate your new strategy against the baseline.

### Optional: Problem 12 (0 pt)

Implement `final_strategy`, which combines these ideas and any other ideas you have to achieve a high win rate against the baseline strategy. Some suggestions:

- `picky_piggy_strategy` or `hog_pile_strategy` are default strategies you can start with.
- If you know the goal score (by default it is 100), there's no point in scoring more than the goal. Check whether you can win by rolling 0, 1 or 2  dice. If you are in the lead, you might decide to take fewer risks.
- Choose the `num_rolls` and `cutoff` arguments carefully.
- Take the action that is most likely to win the game.

You can check that your final strategy is valid by running `ok`.

```
python3 ok -q 12
```

You can also play against your final strategy with the graphical user interface:

```
python3 hog_gui.py
```

The GUI will alternate which player is controlled by you.
