Project 3: Ants Vs. SomeBees

> The bees are coming!
> Create a better soldier
> With inherit-ants.

## Introduction

In this project, you will create a [tower defense](https://secure.wikimedia.org/wikipedia/en/wiki/Tower_defense) game called Ants Vs. SomeBees. As the ant queen, you populate your colony with the bravest ants you can muster. Your ants must protect their queen from the evil bees that invade your territory. Irritate the bees enough by throwing leaves at them, and they will be vanquished. Fail to pester the airborne intruders adequately, and your queen will succumb to the bees' wrath. This game is inspired by PopCap Games' [Plants Vs. Zombies](https://www.ea.com/studios/popcap/plants-vs-zombies).

This project uses an object-oriented programming paradigm, focusing on material from [Chapter 2.5](http://composingprograms.com/pages/25-object-oriented-programming.html) of Composing Programs. The project also involves understanding, extending, and testing a large program.

> When students in the past have tried to implement the functions without thoroughly reading the problem description, they’ve often run into issues. 😱 **Read each description thoroughly before starting to code.**

## Download starter files

The [ants.zip](https://cs61a.org/proj/ants/ants.zip) archive contains several files, but all of your changes will be made to `ants.py`.

- `ants.py`: The game logic of Ants Vs. SomeBees
- `ants_gui.py`: The original GUI for Ants Vs. SomeBees
- `gui.py:` A new GUI for Ants Vs. SomeBees.
- `graphics.py`: Utilities for displaying simple two-dimensional animations
- `utils.py`: Some functions to facilitate the game interface
- `ucb.py`: Utility functions for CS 61A
- `state.py`: Abstraction for gamestate for gui.py
- `assets`: A directory of images and files used by `gui.py`
- `img`: A directory of images used by `ants_gui.py`
- `ok`: The autograder
- `proj3.ok`: The `ok` configuration file
- `tests`: A directory of tests used by `ok`

## Logistics

You will turn in the following files:

- `ants.py`

For the functions that we ask you to complete, there may be some initial code that we provide. If you would rather not use that code, feel free to delete it and start from scratch. You may also add new function definitions as you see fit.

However, please do **not** modify any other functions.  Doing so may result in your code failing our autograder tests. Also, please do not change any function signatures (names, argument order, or number of arguments).

Throughout this project, you should be testing the correctness of your code. It is good practice to test often, so that it is easy to isolate any problems. However, you should not be testing *too* often, to allow yourself time to think through problems.

We have provided an **autograder** called `ok` to help you with testing your code and tracking your progress. The first time you run the autograder, you will be asked to **log in with your Ok account using your web browser**. Please do so. Each time you run `ok`, it will back up your work and progress on our servers.

The primary purpose of `ok` is to test your implementations.

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

## The Game

A game of Ants Vs. SomeBees consists of a series of turns. In each turn, new bees may enter the ant colony. Then, new ants are placed to defend their colony. Finally, all insects (ants, then bees) take individual actions. Bees either try to move toward the end of the tunnel or sting ants in their way. Ants perform a different action depending on their type, such as collecting more food or throwing leaves at the bees. The game ends either when a bee reaches the end of the tunnel (you lose), the bees destroy the `QueenAnt` if it exists (you lose), or the entire bee fleet has been vanquished (you win).

![image-20211212155721225](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211212155721225.png)

### Core concepts

**The Colony**. This is where the game takes place. The colony consists of several `Place`s that are chained together to form a tunnel where bees can travel through. The colony also has some quantity of food which can be expended in order to place an ant in a tunnel.

**Places**. A place links to another place to form a tunnel. The player can put a single ant into each place. However, there can be many bees in a single place.

**The Hive**. This is the place where bees originate. Bees exit the beehive to enter the ant colony.

**Ants**. Players place an ant into the colony by selecting from the available ant types at the top of the screen. Each type of ant takes a different action and requires a different amount of colony food to place. The two most basic ant types are the `HarvesterAnt`, which adds one food to the colony during each turn, and the `ThrowerAnt`, which throws a leaf at a bee each turn. You will be implementing many more!

**Bees**. In this game, bees are the antagonistic forces that the player must defend the ant colony from. Each turn, a bee either advances to the next place in the tunnel if no ant is in its way, or it stings the ant in its way. Bees win when at least one bee reaches the end of a tunnel.

### Core classes

The concepts described above each have a corresponding class that encapsulates the logic for that concept. Here is a summary of the main classes involved in this game:

- **`GameState`**: Represents the colony and some state information about the game,  including how much food is available, how much time has elapsed, where the  `AntHomeBase` is, and all the `Place`s in the game.
- **`Place`**: Represents a single place that holds insects. At most one `Ant` can  be in a single place, but there can be many `Bee`s in a single place. `Place` objects have an  `exit` to the left and an `entrance` to the right, which are also places. Bees travel through a tunnel by moving to a `Place`'s `exit`.
- **`Hive`**: Represents the place where `Bee`s start out (on the right of the tunnel).
- **`AntHomeBase`**: Represents the place `Ant`s are defending (on the left of the tunnel). If Bees get here, they win :(
- **`Insect`**: A superclass for `Ant` and `Bee`. All insects have `health`  attribute, representing their remaining health, and a `place` attribute, representing the `Place` where  they are currently located. Each turn, every active `Insect` in the game  performs its `action`.
- **`Ant`**: Represents ants. Each `Ant` subclass has special attributes or a special `action` that distinguish it from other `Ant` types. For example, a  `HarvesterAnt` gets food for the colony and a `ThrowerAnt` attacks `Bee`s.  Each ant type also has a `food_cost` attribute that indicates how much it costs to deploy one unit of that type of ant.
- **`Bee`**: Represents bees. Each turn, a bee either moves to the `exit` of its  current `Place` if the `Place` is not `blocked` by an ant, or stings the ant occupying its same `Place`.

### Game Layout

Below is a visualization of a GameState. As you work through the  unlocking tests and problems, we recommend drawing out similar diagrams  to help your understanding.

![image-20211212155734196](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211212155734196.png)

### Object map

To help visualize how all the classes fit together, we've also created an object map for you to reference as you work, which you can find [here](https://cs61a.org/proj/ants/diagram/ants_diagram.pdf):

### Playing the game

The game can be run in two modes: as a text-based game or using a graphical user interface (GUI). The game logic is the same in either case, but the GUI enforces a turn time limit that makes playing the game more exciting. The text-based interface is provided for debugging and development.

The files are separated according to these two modes.  `ants.py` knows nothing of graphics or turn time limits.

To start a text-based game, run

```
python3 ants_text.py
```

To start a graphical game, run

```
python3 gui.py
```

When you start the graphical version, a new browser window should appear. In the starter implementation, you have unlimited food and your ants can only throw leaves at bees in their current `Place`. Before you complete Problem 2, the GUI may crash since it doesn't have a full conception of what a Place is yet! Try playing the game anyway! You'll need to place a lot of `ThrowerAnt`s (the second type) in order to keep the bees from reaching your queen.

The game has several options that you will use throughout the project, which you can view with `python3 ants_text.py --help`.

```
usage: ants_text.py [-h] [-d DIFFICULTY] [-w] [--food FOOD]

Play Ants vs. SomeBees

optional arguments:
  -h, --help     show this help message and exit
  -d DIFFICULTY  sets difficulty of game (test/easy/normal/hard/extra-hard)
  -w, --water    loads a full layout with water
  --food FOOD    number of food to start with when testing
```

## Phase 1: Basic gameplay

In the first phase you will complete the implementation that will allow for basic gameplay with the two basic `Ant`s: the `HarvesterAnt` and the `ThrowerAnt`.

### Problem 0 (0 pt)

Answer the following questions with your partner after you have read the *entire* `ants.py` file.

To submit your answers, run:

```
python3 ok -q 00 -u
```

If you get stuck while answering these questions, you can try reading through `ants.py` again, consult the [core concepts](https://cs61a.org/proj/ants/#core-concepts)/[classes](https://cs61a.org/proj/ants/#core-classes) sections above, or ask a question in the Question 0 thread on Piazza.

1. What is the significance of an Insect's `health` attribute? Does this value change? If so, how?
2. Which of the following is a class attribute of the `Insect` class?
3. Is the `health` attribute of the `Ant` class an instance attribute or a class  attribute? Why?
4. Is the `damage` attribute of an `Ant` subclass (such as `ThrowerAnt`) an instance attribute or class attribute? Why?
5. Which class do both `Ant` and `Bee` inherit from?
6. What do instances of `Ant` and instances of `Bee` have in common?
7. How many insects can be in a single `Place` at any given time (before Problem 8)?
8. What does a `Bee` do during one of its turns?
9. When is the game lost?

```
---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 1
(cases remaining: 9)

Q: What is the significance of an Insect's health attribute? Does this
value change? If so, how?
Choose the number of the correct choice:
0) It represents the strength of an insect against attacks, which
   doesn't change throughout the game
1) It represents the amount of health the insect has left, so the
   insect is eliminated when it reaches 0
2) It represents health protecting the insect, so the insect can only
   be damaged when its health reaches 0
? 1
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 2
(cases remaining: 8)

Q: Which of the following is a class attribute of the Insect class?
Choose the number of the correct choice:
0) place
1) bees
2) health
3) damage
? 3
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 3
(cases remaining: 7)

Q: Is the health attribute of the Ant class an instance attribute or class attribute? Why?
Choose the number of the correct choice:
0) class, Ants of the same subclass all have the same amount of starting health
1) instance, each Ant starts out with a different amount of health
2) class, when one Ant gets damaged, all ants receive the same amount of damage
3) instance, each Ant instance needs its own health value
? 3
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 4
(cases remaining: 6)

Q: Is the damage attribute of an Ant subclass (such as ThrowerAnt) an
instance or class attribute? Why?
Choose the number of the correct choice:
0) instance, the damage an Ant depends on where the Ant is
1) class, all Ants deal the same damage
2) instance, each Ant does damage to bees at different rates
3) class, all Ants of the same subclass deal the same damage
? 3
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 5
(cases remaining: 5)

Q: Which class do both Ant and Bee inherit from?
Choose the number of the correct choice:
0) Bee
1) Ant
2) Insect
3) Place
? 2
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 6
(cases remaining: 4)

Q: What do instances of Ant and instances of Bee have in common? Please choose the most correct answer.
Choose the number of the correct choice:
0) Ants and Bees both have the attributes health, damage, and place
   and the methods reduce_health and action
1) Ants and Bees both take the same action each turn
2) Ants and Bees have nothing in common
3) Ants and Bees both have the attribute damage and the methods
   reduce_health and action
? 0
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 7
(cases remaining: 3)

Q: How many insects can be in a single Place at any given time in the
game (before Problem 8)?
Choose the number of the correct choice:
0) Only one insect can be in a single Place at a time
1) There is no limit on the number of insects of any type in a single Place
2) There can be one Ant and many Bees in a single Place
3) There can be one Bee and many Ants in a single Place
? 2
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 8
(cases remaining: 2)

Q: What does a Bee do during one of its turns?
Choose the number of the correct choice:
0) The bee stings the ant in its place and then moves to the next place
1) The bee flies to the nearest Ant and attacks it
2) The bee moves to the next place, then stings the ant in that place
3) The bee stings the ant in its place or moves to the next place if there is no ant in its place
? 3
-- OK! --

---------------------------------------------------------------------
Problem 0 > Suite 1 > Case 9
(cases remaining: 1)

Q: When is the game lost?
Choose the number of the correct choice:
0) When any bee reaches the end of the tunnel and the Queen Ant is killed
1) When any bee reaches the end of the tunnel or when the Queen Ant is killed
2) When the bees enter the colony
3) When no ants are left on the map
4) When the colony runs out of food
? 1
-- OK! --
```

### Problem 1 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 1 > Suite 1 > Case 1
(cases remaining: 5)

Q: What is the purpose of the food_cost attribute?
Choose the number of the correct choice:
0) Each turn, each Ant in the colony eats food_cost food from the
   colony's total available food
1) Each turn, each Ant in the colony adds food_cost food to the
   colony's total available food
2) Placing an ant into the colony will decrease the colony's total
   available food by that ant's food_cost
? 2
-- OK! --

---------------------------------------------------------------------
Problem 1 > Suite 1 > Case 2
(cases remaining: 4)

Q: What type of attribute is food_cost?
Choose the number of the correct choice:
0) instance, the food_cost of an Ant depends on the location it is placed
1) instance, the food_cost of an Ant is randomized upon initialization
2) class, all Ants cost the same to place no matter what type of Ant it is
3) class, all Ants of the same subclass cost the same to place
? 3
-- OK! --

---------------------------------------------------------------------
Problem 1 > Suite 2 > Case 1
(cases remaining: 3)

>>> from ants import *
>>> from ants_plans import *
>>> Ant.food_cost
? 0
-- OK! --

>>> HarvesterAnt.food_cost
? 0
-- Not quite. Try again! --

? 2
-- OK! --

>>> ThrowerAnt.food_cost
? 3
-- OK! --

---------------------------------------------------------------------
Problem 1 > Suite 2 > Case 2
(cases remaining: 2)

>>> from ants import *
>>> from ants_plans import *
>>> # Testing HarvesterAnt action
>>> # Create a test layout where the colony is a single row with 9 tiles
>>> beehive = Hive(make_test_assault_plan())
>>> gamestate = GameState(None, beehive, ant_types(), dry_layout, (1, 9))
>>> #
>>> gamestate.food = 4
>>> harvester = HarvesterAnt()
>>> # Note that initializing an Ant here doesn't cost food, only
>>> # deploying an Ant in the game simulation does
>>> #
>>> gamestate.food
? 4
-- OK! --

>>> harvester.action(gamestate)
>>> gamestate.food
? 2
-- Not quite. Try again! --

? 5
-- OK! --

>>> harvester.action(gamestate)
>>> gamestate.food
? 6
-- OK! --
```

**Part A**: Currently, there is no cost for placing any type of `Ant`, and so there is no challenge to the game. The base class `Ant` has a `food_cost` of zero. Override this class attribute for `HarvesterAnt` and `ThrowerAnt` according to the "Food Cost" column in the table below.

| **Class**      | **Food Cost** | **Initial Health** |
| -------------- | ------------- | ------------------ |
| `HarvesterAnt` | 2             | 1                  |
| `ThrowerAnt`   | 3             | 1                  |

**Part B**: Now that placing an `Ant` costs food, we need to be able to gather more food! To fix this issue, implement the `HarvesterAnt` class. A `HarvesterAnt` is a type of `Ant` that adds one food to the `gamestate.food` total as its `action`.

After writing code, test your implementation:

```
python3 ok -q 01
```

Try playing the game by running `python3 gui.py`. Once you have placed a `HarvesterAnt`, you should accumulate food each turn. You can also place `ThrowerAnt`s, but you'll see that they can only attack bees that are in their `Place`, making it a little difficult to win.

### Problem 2 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 2 > Suite 1 > Case 1
(cases remaining: 5)

Q: What does a Place represent in the game?
Choose the number of the correct choice:
0) Where the bees start out in the game
1) The entire space where the game takes place
2) A single tile that an Ant can be placed on and that connects to
   other Places
3) The tunnel that bees travel through
? 2
-- OK! --

---------------------------------------------------------------------
Problem 2 > Suite 1 > Case 2
(cases remaining: 4)

Q: p is a Place whose entrance is q and exit is r (q and r are not None). When is p.entrance first set to a non-None value?
Choose the number of the correct choice:
0) Never, it is always set to None
1) When q is constructed
2) When p is constructed
? 1
-- OK! --

---------------------------------------------------------------------
Problem 2 > Suite 1 > Case 3
(cases remaining: 3)

Q: p is a Place whose entrance is q and exit is r (q and r are not None). When is p.exit first set to a non-None value?
Choose the number of the correct choice:
0) When q is constructed
1) Never, it is always set to None
2) When p is constructed
? 2
-- OK! --

---------------------------------------------------------------------
Problem 2 > Suite 2 > Case 1
(cases remaining: 2)

>>> from ants import *
>>> from ants_plans import *
>>> #
>>> # Create a test layout where the gamestate is a single row with 3 tiles
>>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
>>> dimensions = (1, 3)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Simple test for Place
>>> place0 = Place('place_0')
>>> print(place0.exit)
? None
-- OK! --

>>> print(place0.entrance)
? None
-- OK! --

>>> place1 = Place('place_1', place0)
>>> place1.exit is place0
? True
-- OK! --

>>> place0.entrance is place1
? True
-- OK! --
```

In this problem, you'll complete `Place.__init__` by adding code that tracks entrances. Right now, a `Place` keeps track only of its `exit`. We would like a `Place` to keep track of its entrance as well. A `Place` needs to track only one `entrance`. Tracking entrances will be useful when an `Ant` needs to see what `Bee`s are in front of it in the tunnel.

However, simply passing an entrance to a `Place` constructor will be problematic; we would need to have both the exit and the entrance before creating a `Place`! (It's a [chicken or the egg](https://en.wikipedia.org/wiki/Chicken_or_the_egg) problem.) To get around this problem, we will keep track of entrances in the following way instead. `Place.__init__` should use this logic:

- A newly created `Place` always starts with its `entrance` as `None`.
- If the `Place` has an `exit`, then the `exit`'s `entrance` is set to  that `Place`.

> *Hint:* Remember that when the `__init__` method is called, the first parameter, `self`, is bound to the newly created object

> *Hint:* Try drawing out two `Place`s next to each other if things get confusing. In the GUI, a place's `entrance` is to its right while the `exit` is to its left.

> *Hint:* Remember that `Places` are not stored in a list, so you can't index into anything to access them. This means that you **can't** do something like `colony[index + 1]` to access an adjacent `Place`. How *can* you move from one place to another?

![image-20211212155734196](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211212155734196.png)

After writing code, test your implementation:

```
python3 ok -q 02
```

### Problem 3 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 1
(cases remaining: 12)

Q: What Bee should a ThrowerAnt throw at?
Choose the number of the correct choice:
0) The ThrowerAnt throws at a random Bee in its own Place
1) The ThrowerAnt finds the nearest place behind its own place
   that has Bees and throws at a random Bee in that place
2) The ThrowerAnt finds the nearest place including and in front of its
   own place that has Bees and throws at a random Bee in that place
3) The ThrowerAnt finds the nearest place in either direction that has
   Bees and throws at a random Bee in that place
? 2
-- OK! --

---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 2
(cases remaining: 11)

Q: How do you get the Place object in front of another Place object?
Choose the number of the correct choice:
0) Decrement the place by 1
1) The place's exit instance attribute
2) Increment the place by 1
3) The place's entrance instance attribute
? 3
-- OK! --

---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 3
(cases remaining: 10)

Q: What is the entrance of the first Place in a tunnel (i.e. where do the bees enter from)?
Choose the number of the correct choice:
0) None
1) The Hive
2) An empty Place
? 1
-- OK! --

---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 4
(cases remaining: 9)

Q: How can you determine if a given Place is the Hive?
Choose the number of the correct choice:
0) by checking the bees attribute of the place instance
1) by using the is_hive attribute of the place instance
2) by checking the ant attribute of the place instance
? 1
-- OK! --

---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 5
(cases remaining: 8)

Q: What should nearest_bee return if there is no Bee in front of the ThrowerAnt in the tunnel?
Choose the number of the correct choice:
0) The closest Bee behind the ThrowerAnt
1) A random Bee in the Hive
2) None
? 2
-- OK! --

---------------------------------------------------------------------
Problem 3 > Suite 2 > Case 1
(cases remaining: 7)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> thrower = ThrowerAnt()
>>> ant_place = gamestate.places["tunnel_0_0"]
>>> ant_place.add_insect(thrower)
>>> #
>>> # Testing nearest_bee
>>> near_bee = Bee(2) # A Bee with 2 health
>>> far_bee = Bee(3)  # A Bee with 3 health
>>> hive_bee = Bee(4) # A Bee with 4 health
>>> hive_place = gamestate.beehive
>>> hive_place.is_hive # Check if this place is the Hive
? True
-- OK! --

>>> hive_place.add_insect(hive_bee)
>>> thrower.nearest_bee() is hive_bee # Bees in the Hive can never be attacked
? True
-- Not quite. Try again! --

? False
-- OK! --

>>> near_place = gamestate.places['tunnel_0_3']
>>> far_place = gamestate.places['tunnel_0_6']
>>> near_place.is_hive # Check if this place is the Hive
? False
-- OK! --

>>> near_place.add_insect(near_bee)
>>> far_place.add_insect(far_bee)
>>> nearest_bee = thrower.nearest_bee()
>>> nearest_bee is far_bee
? False
-- OK! --

>>> nearest_bee is near_bee
? True
-- OK! --

>>> nearest_bee.health
? 1
-- Not quite. Try again! --

? 2
-- OK! --

>>> thrower.action(gamestate)    # Attack! ThrowerAnts do 1 damage
>>> near_bee.health
? 1
-- OK! --

>>> far_bee.health
? 3
-- OK! --

>>> thrower.place is ant_place    # Don't change self.place!
? True
-- OK! --
```

In order for a `ThrowerAnt` to throw a leaf, it must know which bee to hit. The provided implementation of the `nearest_bee` method in the `ThrowerAnt` class only allows them to hit bees in the same `Place`. Your job is to fix it so that a `ThrowerAnt` will `throw_at` the nearest bee in front of it **that is not still in the `Hive`.** This includes bees that are in the same `Place` as a `ThrowerAnt`

> *Hint:* All `Place`s have an `is_hive` attribute which is `True` when that place is the `Hive`.

Change `nearest_bee` so that it returns a random `Bee` from the nearest place that contains bees. Your implementation should follow this logic:

- Start from the current `Place` of the `ThrowerAnt`.
- For each place, return a random bee if there is any, and if not,  inspect the place in front of it (stored as the current place's `entrance`).
- If there is no bee to attack, return `None`.

> *Hint*: The `random_bee` function provided in `ants.py` returns a random bee from a list of bees or `None` if the list is empty.

> *Hint*: As a reminder, if there are no bees present at a `Place`, then the `bees` attribute of that `Place` instance will be an empty list.

> *Hint*: Having trouble visualizing the test cases? Try drawing them out on paper! The sample diagram provided in [Game Layout](https://cs61a.org/proj/ants/#game-layout) shows the first test case for this problem.

After writing code, test your implementation:

```
python3 ok -q 03
```

After implementing `nearest_bee`, a `ThrowerAnt` should be able to `throw_at` a `Bee` in front of it that is not still in the `Hive`.  Make sure that your ants do the right thing! To start a game with ten food (for easy testing):

```
python3 gui.py --food 10
```

Make sure to submit by the checkpoint deadline using the following command:

```
python3 ok --submit
```

You can check to ensure that you have completed Phase 1's problems by running:

```
python3 ok --score
```

Congratulations! You have finished Phase 1 of this project!

## Phase 2: Ants!

Now that you've implemented basic gameplay with two types of `Ant`s, let's add some flavor to the ways ants can attack bees. In this phase, you'll be implementing several different `Ant`s with different attack strategies.

After you implement each `Ant` subclass in this section, you'll need to set its `implemented` class attribute to `True` so that that type of ant will show up in the GUI. Feel free to try out the game with each new ant to test the functionality!

With your Phase 2 ants, try `python3 gui.py -d easy` to play against a full swarm of bees in a multi-tunnel layout and try `-d normal`, `-d hard`, or `-d extra-hard` if you want a real challenge! If the bees are too numerous to vanquish, you might need to create some new ants.

### Problem 4 (2 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 1
(cases remaining: 25)

Q: What class do ShortThrower and LongThrower inherit from?
Choose the number of the correct choice:
0) Bee
1) ShortThrower
2) ThrowerAnt
3) LongThrower
? 2
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 2
(cases remaining: 24)

Q: What constraint does a regular ThrowerAnt have on its throwing distance?
Choose the number of the correct choice:
0) There is no restriction on how far a regular ThrowerAnt can throw
1) A regular ThrowerAnt can only attack Bees at most 3 places away
2) A regular ThrowerAnt can only attack Bees at most 5 places away
3) A regular ThrowerAnt can only attack Bees at least 3 places away
? 0
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 3
(cases remaining: 23)

Q: What constraint does a LongThrower have on its throwing distance?
Choose the number of the correct choice:
0) A LongThrower can only attack Bees at most 5 places away
1) There is no restriction on how far a LongThrower can throw
2) A LongThrower can only attack Bees at least 5 places away
3) A LongThrower can only attack Bees at least 3 places away
? 2
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 4
(cases remaining: 22)

Q: What constraint does a ShortThrower have on its throwing distance?
Choose the number of the correct choice:
0) A ShortThrower can only attack Bees at most 5 places away
1) A ShortThrower can only attack Bees at least 3 places away
2) There is no restriction on how far a ShortThrower can throw
3) A ShortThrower can only attack Bees at most 3 places away
? 3
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 5
(cases remaining: 21)

Q: With the addition of these new ThrowerAnt subclasses, we must modify
our definition of nearest_bee. Now what Bee should ThrowerAnts throw
at?
Choose the number of the correct choice:
0) The closest Bee behind it within range
1) Any Bee within range
2) The closest Bee in front of it within range
3) Any Bee in its current Place
? 2
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 2 > Case 1
(cases remaining: 20)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing Long/ShortThrower parameters
>>> ShortThrower.food_cost
? 2
-- OK! --

>>> LongThrower.food_cost
? 2
-- OK! --

>>> short_t = ShortThrower()
>>> long_t = LongThrower()
>>> short_t.health
? 1
-- OK! --

>>> long_t.health
? 1
-- OK! --
```

A `ThrowerAnt` is a powerful threat to the bees, but it has a high food cost. In this problem, you'll implement two subclasses of `ThrowerAnt` that are less costly but have constraints on the distance they can throw:

- The `LongThrower` can only `throw_at` a `Bee` that is found after following  at least 5 `entrance` transitions. It cannot hit `Bee`s that are in the same  `Place` as it or the first 4 `Place`s in front of it. If there are two  `Bees`, one too close to the `LongThrower` and the other within its range,  the `LongThrower` should only throw at the farther `Bee`, which is within its range, instead of trying to hit the closer `Bee`.
- The `ShortThrower` can only `throw_at` a `Bee` that is found after following  at most 3 `entrance` transitions. It cannot throw at any bees further than 3  `Place`s in front of it.

Neither of these specialized throwers can `throw_at` a `Bee` that is exactly 4 `Place`s away.

| **Class**      | **Food Cost** | **Initial Health** |
| -------------- | ------------- | ------------------ |
| `ShortThrower` | 2             | 1                  |
| `LongThrower`  | 2             | 1                  |

To implement these new throwing ants, your `ShortThrower` and `LongThrower` classes should inherit the `nearest_bee` method from the base `ThrowerAnt` class. The logic of choosing which bee a thrower ant will attack is the same, except the `ShortThrower` and `LongThrower` ants have a maximum and minimum range, respectively.

To do this, modify the `nearest_bee` method to reference `min_range` and `max_range` attributes, and only return a bee if it is within range.

Make sure to give these `min_range` and `max_range` attributes appropriate values in the `ThrowerAnt` class so that the behavior of `ThrowerAnt` is unchanged. Then, implement the subclasses `LongThrower` and `ShortThrower` with appropriately constrained ranges.

You should **not** need to repeat any code between `ThrowerAnt`, `ShortThrower`, and `LongThrower`.

> *Hint:* `float('inf')` returns an infinite positive value represented as a float that can be compared with other numbers.

> *Hint:* You can chain inequalities in Python: e.g. `2 < x < 6` will check if `x` is between 2 and 6. Also, `min_range` and `max_range` should mark an inclusive range.

> **Important:** Make sure your class attributes are called `max_range` and `min_range` The tests directly reference these attribute names, and will error if you use another name for these attributes.

Don't forget to set the `implemented` class attribute of `LongThrower` and `ShortThrower` to `True`.

After writing code, test your implementation (rerun the tests for 03 to make sure they still work):

```
python3 ok -q 03
python3 ok -q 04
```

[Pair programming?](https://cs61a.org/articles/pair-programming) Remember to alternate between driver and navigator roles. The driver controls the keyboard; the navigator watches, asks questions, and suggests ideas.

### Problem 5 (3 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 5 > Suite 1 > Case 1
(cases remaining: 16)

Q: How can you obtain the current place of a FireAnt?
Choose the number of the correct choice:
0) By calling the FireAnt constructor
1) By accessing the place instance attribute, which is the name of
   some Place object
2) By accessing the place instance attribute, which is a Place object
3) By calling the Place constructor, passing in the FireAnt instance
? 1
-- Not quite. Try again! --

? 2
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 1 > Case 2
(cases remaining: 15)

Q: How can you obtain all of the Bees currently in a given place?
Choose the number of the correct choice:
0) By calling the Bee constructor, passing in the place instance
1) By accessing the bees instance attribute, which is a dictionary of
   Bee objects
2) By calling the add_insect method on the place instance
3) By accessing the bees instance attribute, which is a list of Bee
   objects
? 3
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 1 > Case 3
(cases remaining: 14)

Q: Can you iterate over a list while mutating it?
Choose the number of the correct choice:
0) Yes, you can mutate a list while iterating over it with no problems
1) Yes, but you should iterate over a copy of the list to avoid skipping
   elements
2) No, Python doesn't allow list mutation on a list that is being
   iterated through
? 1
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 2 > Case 1
(cases remaining: 13)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing FireAnt parameters
>>> fire = FireAnt()
>>> FireAnt.food_cost
? 5
-- OK! --

>>> fire.health
? 3
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 2 > Case 3
(cases remaining: 11)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing fire does damage to all Bees in its Place
>>> place = gamestate.places['tunnel_0_4']
>>> fire = FireAnt(health=1)
>>> place.add_insect(fire)        # Add a FireAnt with 1 health
>>> place.add_insect(Bee(3))      # Add a Bee with 3 health
>>> place.add_insect(Bee(5))      # Add a Bee with 5 health
>>> len(place.bees)               # How many bees are there?
? 1
-- Not quite. Try again! --

? 0
-- Not quite. Try again! --

? 2
-- OK! --

>>> place.bees[0].action(gamestate)  # The first Bee attacks FireAnt
>>> fire.health
? 0
-- OK! --

>>> fire.place is None
? False
-- Not quite. Try again! --

? True
-- OK! --

>>> len(place.bees)               # How many bees are left?
? 1
-- OK! --

>>> place.bees[0].health           # What is the health of the remaining Bee?
? 0
-- Not quite. Try again! --

? -1
-- Not quite. Try again! --

? 1
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 2 > Case 4
(cases remaining: 10)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> place = gamestate.places['tunnel_0_4']
>>> ant = FireAnt(health=1)           # Create a FireAnt with 1 health
>>> place.add_insect(ant)      # Add a FireAnt to place
>>> ant.place is place
? True
-- OK! --

>>> place.remove_insect(ant)   # Remove FireAnt from place
>>> ant.place is place         # Is the ant's place still that place?
? True
-- Not quite. Try again! --

? False
-- OK! --
```

Implement the `FireAnt`, which does damage when it receives damage. Specifically, if it is damaged by `amount` health units, it does a damage of `amount` to all bees in its place (this is called *reflected damage*). If it dies, it does an additional amount of damage, as specified by its `damage` attribute, which has a default value of `3` as defined in the `FireAnt` class.

To implement this, override `FireAnt`'s `reduce_health` method. Your overridden method should call the `reduce_health` method inherited from the superclass (`Ant`) to reduce the current `FireAnt` instance's health. Calling the *inherited* `reduce_health` method on a `FireAnt` instance reduces the insect's `health` by the given `amount` and removes the insect from its place if its `health` reaches zero or lower.

> *Hint:* Do *not* call `self.reduce_health`, or you'll end up stuck in a recursive loop. (Can you see why?)

However, your method needs to also include the reflective damage logic:

- Determine the reflective damage amount:  start with the `amount` inflicted on the ant,  and then add `damage` if the ant's health has dropped to 0.
- For each bee in the place, damage them with the total amount by  calling the appropriate `reduce_health` method for each bee.

> **Important:** The `FireAnt` must do its damage *before* being removed from its `place`, so pay careful attention to the order of your logic in `reduce_health`.

| **Class** | **Food Cost** | **Initial Health** |
| --------- | ------------- | ------------------ |
| `FireAnt` | 5             | 3                  |

> *Hint:* Damaging a bee may cause it to be removed from its place. If you iterate over a list, but change the contents of that list at the same time, you [may not visit all the elements](https://docs.python.org/3/tutorial/controlflow.html#for-statements). This can be prevented by making a copy of the list. You can either use a list slice, or use the built-in `list` function.
>
> ```
>  >>> lst = [1,2,3,4]
>  >>> lst[:]
>  [1, 2, 3, 4]
>  >>> list(lst)
>  [1, 2, 3, 4]
>  >>> lst[:] is not lst and list(lst) is not lst
>  True
> ```

Once you've finished implementing the `FireAnt`, give it a class attribute `implemented` with the value `True`.

> *Note:* Even though you are overriding the superclass's `reduce_health` function (`Ant.reduce_health`), you can still use this method in your implementation by calling it. Note this is not recursion. (Why not?)

After writing code, test your implementation:

```
python3 ok -q 05
```

You can also test your program by playing a game or two! A `FireAnt` should destroy all co-located Bees when it is stung. To start a game with ten food (for easy testing):

```
python3 gui.py --food 10
```

## Phase 3: More Ants!

### Problem 6 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 1
(cases remaining: 9)

Q: What class does WallAnt inherit from?
Choose the number of the correct choice:
0) The WallAnt class does not inherit from any class
1) ThrowerAnt
2) Ant
3) HungryAnt
? 2
-- OK! --

---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 2
(cases remaining: 8)

Q: What is a WallAnt's action?
Choose the number of the correct choice:
0) A WallAnt attacks all the Bees in its place each turn
1) A WallAnt increases its own health by 1 each turn
2) A WallAnt reduces its own health by 1 each turn
3) A WallAnt takes no action each turn
? 3
-- OK! --

---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 3
(cases remaining: 7)

Q: Where do Ant subclasses inherit the action method from?
Choose the number of the correct choice:
0) Ant subclasses inherit the action method from the Ant class
1) Ant subclasses inherit the action method from the Insect class
2) Ant subclasses do not inherit the action method from any class
? 1
-- OK! --

---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 4
(cases remaining: 6)

Q: If a subclass of Ant does not override the action method, what is the
default action?
Choose the number of the correct choice:
0) Move to the next place
1) Nothing
2) Reduce the health of all Bees in its place
3) Throw a leaf at the nearest Bee
? 1
-- OK! --

---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 5
(cases remaining: 5)

Q: What type of attribute is health?
Choose the number of the correct choice:
0) class, all Ants have the same health no matter what type of Ant it is
1) instance, all Ants have different default starting healths
2) class, all Ants of the same subclass have the same health
3) instance, all Ants keep track of their own health
? 2
-- Not quite. Try again! --

? 3
-- OK! --
```

We are going to add some protection to our glorious home base by implementing the `WallAnt`, an ant that does nothing each turn. A `WallAnt` is useful because it has a large `health` value.

| **Class** | **Food Cost** | **Initial Health** |
| --------- | ------------- | ------------------ |
| `WallAnt` | 4             | 4                  |

Unlike with previous ants, we have not provided you with a class header. Implement the `WallAnt` class from scratch. Give it a class attribute `name` with the value `'Wall'` (so that the graphics work) and a class attribute `implemented` with the value `True` (so that you can use it in a game).

> *Hint*: To start, take a look at how the previous problems' ants were implemented!

After writing code, test your implementation:

```
python3 ok -q 06
```

### Problem 7 (3 pt)

Implement the `HungryAnt`, which will select a random `Bee` from its `place` and eat it whole. After eating a `Bee`, a `HungryAnt` must spend 3 turns chewing before eating again. If there is no bee available to eat, `HungryAnt` will do nothing.

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 7 > Suite 1 > Case 1
(cases remaining: 14)

Q: Should chew_countdown be an instance or class attribute? Why?
Choose the number of the correct choice:
0) class, all HungryAnt instances in the game chew simultaneously
1) instance, all HungryAnt instances in the game chew simultaneously
2) instance, each HungryAnt instance chews independently of other
   HungryAnt instances
3) class, each HungryAnt instance chews independently of other
   HungryAnt instances
? 2
-- OK! --

---------------------------------------------------------------------
Problem 7 > Suite 1 > Case 2
(cases remaining: 13)

Q: When is a HungryAnt able to eat a Bee?
Choose the number of the correct choice:
0) Whenever a Bee is in its place
1) When it is chewing, i.e. when its chew_countdown attribute is at least 1
2) Each turn
3) When it is not chewing, i.e. when its chew_countdown attribute is 0
? 3
-- OK! --

---------------------------------------------------------------------
Problem 7 > Suite 1 > Case 3
(cases remaining: 12)

Q: When a HungryAnt is able to eat, which Bee does it eat?
Choose the number of the correct choice:
0) The closest Bee behind it
1) The closest Bee in either direction
2) A random Bee in the same place as itself
3) The closest Bee in front of it
? 2
-- OK! --

---------------------------------------------------------------------
Problem 7 > Suite 2 > Case 1
(cases remaining: 11)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing HungryAnt parameters
>>> hungry = HungryAnt()
>>> HungryAnt.food_cost
? 4
-- OK! --

>>> hungry.health
? 1
-- OK! --

>>> hungry.chew_duration
? 3
-- OK! --

>>> hungry.chew_countdown
? 0
-- OK! --

---------------------------------------------------------------------
Problem 7 > Suite 2 > Case 4
(cases remaining: 8)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing HungryAnt eats and chews
>>> hungry = HungryAnt()
>>> super_bee, wimpy_bee = Bee(1000), Bee(1)
>>> place = gamestate.places["tunnel_0_0"]
>>> place.add_insect(hungry)
>>> place.add_insect(super_bee)
>>> hungry.action(gamestate)         # super_bee is no match for HungryAnt!
>>> super_bee.health
? 0
-- OK! --

>>> place.add_insect(wimpy_bee)
>>> for _ in range(3):
...     hungry.action(gamestate)     # chewing...not eating
>>> wimpy_bee.health
? 1
-- OK! --

>>> hungry.action(gamestate)         # back to eating!
>>> wimpy_bee.health
? 0
-- OK! --
```

We have not provided you with a class header. Implement the `HungryAnt` class from scratch. Give it a class attribute `name` with the value `'Hungry'` (so that the graphics work) and a class attribute `implemented` with the value `True` (so that you can use it in a game).

> *Hint:* When a `Bee` is eaten, it should lose all its health. Is there an existing function we can call on a `Bee` that can reduce its health to 0?

| **Class**   | **Food Cost** | **Initial Health** |
| ----------- | ------------- | ------------------ |
| `HungryAnt` | 4             | 1                  |

Give `HungryAnt` a `chew_duration` **class** attribute that stores the number of turns that it will take a `HungryAnt` to chew (set to 3). Also, give each `HungryAnt` an **instance** attribute `chew_countdown` that counts the number of turns it has left to chew (initialized to 0, since it hasn't eaten anything at the beginning. You can also think of `chew_countdown` as the number of turns until a `HungryAnt` can eat another `Bee`).

Implement the `action` method of the `HungryAnt`: First, check if it is chewing; if so, decrement its `chew_countdown`. Otherwise, eat a random `Bee` in its `place` by reducing the `Bee`'s health to 0. Make sure to set the `chew_countdown` when a Bee is eaten!

> *Hint*: Other than the `action` method, make sure you implement the `__init__` method too so the `HungryAnt` starts off with the appropriate amount of `health`!

After writing code, test your implementation:

```
python3 ok -q 07
```

We now have some great offensive troops to help vanquish the bees, but let's make sure we're also keeping our defensive efforts up. In this phase you will implement ants that have special defensive capabilities such as increased health and the ability to protect other ants.

[Pair programming?](https://cs61a.org/articles/pair-programming) This would be a good time to switch roles. Switching roles makes sure that you both benefit from the learning experience of being in each role.

### Problem 8 (3 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 1
(cases remaining: 20)

Q: Which Ant does a BodyguardAnt guard?
Choose the number of the correct choice:
0) All the Ant instances in the gamestate
1) The Ant instance in the place closest to its own place
2) The Ant instance that is in the same place as itself
3) A random Ant instance in the gamestate
? 2
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 2
(cases remaining: 19)

Q: How does a BodyguardAnt guard its ant?
Choose the number of the correct choice:
0) By allowing Bees to pass without attacking
1) By attacking Bees that try to attack it
2) By increasing the ant's health
3) By protecting the ant from Bees and allowing it to perform its original action
? 2
-- Not quite. Try again! --

? 3
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 3
(cases remaining: 18)

Q: Where is the ant contained by a BodyguardAnt stored?
Choose the number of the correct choice:
0) In its place's ant instance attribute
1) Nowhere, a BodyguardAnt has no knowledge of the ant that it's protecting
2) In the BodyguardAnt's ant_contained instance attribute
3) In the BodyguardAnt's ant_contained class attribute
? 2
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 4
(cases remaining: 17)

Q: When can a second Ant be added to a place that already contains an Ant?
Choose the number of the correct choice:
0) When both Ant instances are containers
1) When exactly one of the Ant instances is a container and the
   container ant does not already contain another ant
2) There can never be two Ant instances in the same place
3) When exactly one of the Ant instances is a container
? 1
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 5
(cases remaining: 16)

Q: If two Ants occupy the same Place, what is stored in that place's ant
instance attribute?
Choose the number of the correct choice:
0) The Ant being contained
1) Whichever Ant was placed there first
2) The Container Ant
3) A list containing both Ants
? 2
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 2 > Case 1
(cases remaining: 15)

>>> from ants import *
>>> # Testing BodyguardAnt parameters
>>> bodyguard = BodyguardAnt()
>>> BodyguardAnt.food_cost
? 4
-- OK! --

>>> bodyguard.health
? 2
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 3 > Case 2
(cases remaining: 12)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
>>> #
>>> # Bodyguard ant added before another ant
>>> bodyguard = BodyguardAnt()
>>> other_ant = ThrowerAnt()
>>> place = gamestate.places['tunnel_0_0']
>>> place.add_insect(bodyguard)  # Bodyguard in place first
>>> place.add_insect(other_ant)
>>> place.ant is bodyguard
? True
-- OK! --

>>> bodyguard.ant_contained is other_ant
? True
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 3 > Case 3
(cases remaining: 11)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
>>> #
>>> # Bodyguard ant can be added after another ant
>>> bodyguard = BodyguardAnt()
>>> other_ant = ThrowerAnt()
>>> place = gamestate.places['tunnel_0_0']
>>> place.add_insect(other_ant)  # Other ant in place first
>>> place.ant is other_ant
? True
-- OK! --

>>> place.add_insect(bodyguard)
>>> place.ant is bodyguard
? True
-- OK! --

>>> bodyguard.ant_contained is other_ant
? True
-- OK! --
```

Right now, our ants are quite frail. We'd like to provide a way to help them last longer against the onslaught of the bees. Enter the `BodyguardAnt`.

| **Class**      | **Food Cost** | **Initial Health** |
| -------------- | ------------- | ------------------ |
| `BodyguardAnt` | 4             | 2                  |

A `BodyguardAnt` differs from a normal ant because it is a `ContainerAnt`; it can contain another ant and protect it, all in one `Place`. When a `Bee` stings the ant in a `Place` where one ant contains another, only the container is damaged. The ant inside the container can still perform its original action. If the container perishes, the contained ant still remains in the place (and can then be damaged).

Each `ContainerAnt` has an instance attribute `ant_contained` that stores the ant it contains. This ant, `ant_contained`, initially starts off as `None` to indicate that there is no ant being stored yet. Implement the `store_ant` method so that it sets the `ContainerAnt`'s `ant_contained` instance attribute to the passed in `ant` argument. Also implement the `ContainerAnt`'s `action` method to perform its `ant_contained`'s action if it is currently containing an ant.

In addition, you will need to make the following modifications throughout your program so that a container and its contained ant can both occupy a place at the same time (a maximum of two ants per place), but only if exactly one is a container:

1. There is an `Ant.can_contain` method, but it always returns `False`.  Override the method `ContainerAnt.can_contain` so that it takes an ant `other` as an  argument and returns `True` if:
   - This `ContainerAnt` does not already contain another ant.
   - The other ant is not a container.
2. Modify `Ant.add_to` to allow a container and a non-container ant  to occupy the same place according to the following rules:
   - If the ant originally occupying a place can contain the ant being added, then both ants occupy the place and original ant contains the ant being added.
   - If the ant being added can contain the ant originally in the space, then both ants occupy the place and the (container) ant being added contains the original ant.
   - If neither `Ant` can contain the other, raise the same `AssertionError` as before (the one already present in the starter code).
   - **Important:** If there are two ants in a specific `Place`, the `ant` attribute of the `Place` instance should refer to the container ant, and the container ant should contain the non-container ant.
3. Add a `BodyguardAnt.__init__` that sets the initial amount of health for the ant.

> *Hint*: You may find the `is_container` attribute that each `Ant` has useful for checking if a specific `Ant` is a container. You should also take advantage of the `can_contain` method you wrote and avoid repeating code.

> The constructor of `ContainerAnt.__init__` is implemented as follows:
>
> ```
>     def __init__(self, *args, **kwargs):
>         super().__init__(*args, **kwargs)
>         self.ant_contained = None
> ```
>
> As we saw in Hog, `args` is bound to all positional arguments (which are all arguments passed without keywords), and `kwargs` is bound to all the keyword arguments. This ensures that both sets of arguments are passed to the Ant constructor.
>
> Effectively, this means the constructor is exactly the same as its parent class's constructor (`Ant.__init__`) but here we also set `self.ant_contained = None`.

Once you've finished implementing the `BodyguardAnt`, give it a class attribute `implemented` with the value `True`.

After writing code, test your implementation:

```
python3 ok -q 08
```

### Problem 9 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
Problem 9 > Suite 1 > Case 1
(cases remaining: 13)

Q: Besides costing more to place, what is the only difference between a
TankAnt and a BodyguardAnt?
Choose the number of the correct choice:
0) A TankAnt increases the damage of the ant it contains
1) A TankAnt has greater health than a BodyguardAnt
2) A TankAnt does damage to all Bees in its place each turn
3) A TankAnt can contain multiple ants
? 2
-- OK! --

---------------------------------------------------------------------
Problem 9 > Suite 2 > Case 1
(cases remaining: 12)

>>> from ants_plans import *
>>> from ants import *
>>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing TankAnt parameters
>>> TankAnt.food_cost
? 6
-- OK! --

>>> TankAnt.damage
? 1
-- OK! --

>>> tank = TankAnt()
>>> tank.health
? 2
-- OK! --
```

The `BodyguardAnt` provides great defense, but they say the best defense is a good offense. The `TankAnt` is a container that protects an ant in its place and also deals 1 damage to all bees in its place each turn.

| **Class** | **Food Cost** | **Initial Health** |
| --------- | ------------- | ------------------ |
| `TankAnt` | 6             | 2                  |

We have not provided you with a class header. Implement the `TankAnt` class from scratch. Give it a class attribute `name` with the value `'Tank'` (so that the graphics work) and a class attribute `implemented` with the value `True` (so that you can use it in a game).

You should not need to modify any code outside of the `TankAnt` class. If you find yourself needing to make changes elsewhere, look for a way to write your code for the previous question such that it applies not just to `BodyguardAnt` and `TankAnt` objects, but to container ants in general.

> *Hint*: The only methods you need to override from `TankAnt`'s parent class are `__init__` and `action`.

> *Hint*: Like with `FireAnt`, it is possible that damaging a bee will cause it to be removed from its place.

After writing code, test your implementation:

```
python3 ok -q 09
```

## Phase 4: Water and Might

In the final phase, you're going to add one last kick to the game by introducing a new type of place and new ants that are able to occupy this place. One of these ants is the most important ant of them all: the queen of the colony!

### Problem 10 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 10 > Suite 1 > Case 1
(cases remaining: 8)

Q: What happens when an insect is added to a Water Place?
Choose the number of the correct choice:
0) The insect goes for a swim.
1) The insect's health is reduced to 0.
2) If the insect is not waterproof, its health is reduced to 0.
   Otherwise, nothing happens.
3) Nothing happens.
? 2
-- OK! --

---------------------------------------------------------------------
Problem 10 > Suite 1 > Case 2
(cases remaining: 7)

Q: What type of attribute should "is_waterproof" be?
Choose the number of the correct choice:
0) instance, the is_waterproof attribute depends on the given place of an ant
1) class, all ants should be waterproof
2) instance, the is_waterproof attribute depends on the amount of health a given ant has left
3) class, all ants of a subclass should either be waterproof or not
? 3
-- OK! --

---------------------------------------------------------------------
Problem 10 > Suite 1 > Case 3
(cases remaining: 6)

Q: What method deals damage to an Insect and removes it from its place
if its health reaches 0?
Choose the number of the correct choice:
0) sting, in the Bee class
1) remove_ant, in the GameState class
2) reduce_health, in the Insect class
3) remove_insect, in the Place class
? 2
-- OK! --

---------------------------------------------------------------------
Problem 10 > Suite 2 > Case 2
(cases remaining: 4)

>>> from ants import *
>>> from ants_plans import *
>>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing water with soggy (non-waterproof) bees
>>> test_bee = Bee(1000000)
>>> test_bee.is_waterproof = False    # Make Bee non-waterproof
>>> test_water = Water('Water Test2')
>>> test_water.add_insect(test_bee)
>>> test_bee.health
? 0
-- OK! --

>>> test_water.bees
? []
-- OK! --

---------------------------------------------------------------------
Problem 10 > Suite 2 > Case 3
(cases remaining: 3)

>>> from ants import *
>>> from ants_plans import *
>>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing water with waterproof bees
>>> test_bee = Bee(1)
>>> test_water = Water('Water Test3')
>>> test_water.add_insect(test_bee)
>>> test_bee.health
? 1
-- OK! --

>>> test_bee in test_water.bees
? True
-- OK! --
```

Let's add water to the colony! Currently there are only two types of places, the `Hive` and a basic `Place`. To make things more interesting, we're going to create a new type of `Place` called `Water`.

Only an insect that is waterproof can be placed in `Water`. In order to determine whether an `Insect` is waterproof, add a new class attribute to the `Insect` class named `is_waterproof` that is set to `False`. Since bees can fly, set their `is_waterproof` attribute to `True`, overriding the inherited value.

Now, implement the `add_insect` method for `Water`. First, add the insect to the place regardless of whether it is waterproof.  Then, if the insect is not waterproof, reduce the insect's health to 0. *Do not repeat code from elsewhere in the program.* Instead, use methods that have already been defined.

After writing code, test your implementation:

```
python3 ok -q 10
```

Once you've finished this problem, play a game that includes water. To access the `wet_layout`, which includes water, add the `--water` option (or `-w` for short) when you start the game.

```
python3 gui.py --water
```

[Pair programming?](https://cs61a.org/articles/pair-programming) Remember to alternate between driver and navigator roles. The driver controls the keyboard; the navigator watches, asks questions, and suggests ideas.

### Problem 11 (1 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 11 > Suite 1 > Case 1
(cases remaining: 9)

Q: How is a ScubaThrower different from a regular ThrowerAnt?
Choose the number of the correct choice:
0) It is not waterproof, so its health will be reduced to 0 when it is
   placed in a Water Place
1) It throws water pellets instead of leaves
2) It is waterproof, so its health won't be reduced to 0 when it is
   placed in a Water Place

? 2
-- OK! --

---------------------------------------------------------------------
Problem 11 > Suite 1 > Case 2
(cases remaining: 8)

Q: Which inherited attributes and/or methods should ScubaThrower
override?
Choose the number of the correct choice:
0) is_waterproof, action
1) name, nearest_bee, is_waterproof
2) food_cost, action, damage
3) name, is_waterproof, food_cost
? 2
-- Not quite. Try again! --

? 3
-- OK! --

---------------------------------------------------------------------
Problem 11 > Suite 2 > Case 1
(cases remaining: 7)

>>> from ants import *
>>> # Testing ScubaThrower parameters
>>> scuba = ScubaThrower()
>>> ScubaThrower.food_cost
? 6
-- OK! --

>>> scuba.health
? 1
-- OK! --

---------------------------------------------------------------------
Problem 11 > Suite 3 > Case 1
(cases remaining: 6)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing if ScubaThrower is waterproof
>>> water = Water('Water')
>>> ant = ScubaThrower()
>>> water.add_insect(ant)
>>> ant.place is water
? True
-- OK! --

>>> ant.health
? 1
-- OK! --

---------------------------------------------------------------------
Problem 11 > Suite 3 > Case 2
(cases remaining: 5)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing that ThrowerAnt is not waterproof
>>> water = Water('Water')
>>> ant = ThrowerAnt()
>>> water.add_insect(ant)
>>> ant.place is water
? True
-- Not quite. Try again! --

? False
-- OK! --

>>> ant.health
? 0
-- OK! --
```

Currently there are no ants that can be placed on `Water`. Implement the `ScubaThrower`, which is a subclass of `ThrowerAnt` that is more costly and waterproof, *but otherwise identical to its base class*. A `ScubaThrower` should not lose its health when placed in `Water`.

| **Class**      | **Food Cost** | **Initial Health** |
| -------------- | ------------- | ------------------ |
| `ScubaThrower` | 6             | 1                  |

We have not provided you with a class header. Implement the `ScubaThrower` class from scratch. Give it a class attribute `name` with the value `'Scuba'` (so that the graphics work) and remember to set the class attribute `implemented` with the value `True` (so that you can use it in a game).

After writing code, test your implementation:

```
python3 ok -q 11
```

### Problem 12 (3 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem 12 > Suite 1 > Case 1
(cases remaining: 16)

Q: What class does QueenAnt inherit from?
Choose the number of the correct choice:
0) GameState
1) Ant
2) ScubaThrower
3) Insect
? 2
-- OK! --

---------------------------------------------------------------------
Problem 12 > Suite 1 > Case 2
(cases remaining: 15)

Q: What does the true QueenAnt do each turn?
Choose the number of the correct choice:
0) Doubles the damage of all the ants in the colony (that haven't
   already been doubled)
1) Doubles the damage of all the ants behind her (that haven't
   already been doubled)
2) Doubles the damage of all the ants in front of her (that haven't
   already been doubled)
3) Attacks the nearest bee and doubles the damage of all the ants
   behind her (that haven't already been doubled)
? 1
-- Not quite. Try again! --

? 3
-- OK! --

---------------------------------------------------------------------
Problem 12 > Suite 1 > Case 3
(cases remaining: 14)

Q: Under what circumstances do Ants lose the game?
Choose the number of the correct choice:
0) If a second QueenAnt is placed in the colony
1) If a Bee attacks the true QueenAnt
2) If a Bee reaches the end of a tunnel or the true QueenAnt dies
3) If there are no ants left in the colony
? 2
-- OK! --

---------------------------------------------------------------------
Problem 12 > Suite 2 > Case 1
(cases remaining: 13)

>>> from ants import *
>>> beehive = Hive(AssaultPlan())
>>> dimensions = (2, 9)
>>> gamestate = GameState(None, beehive, ant_types(), dry_layout, dimensions, food=100)
>>> # Testing QueenAnt parameters
>>> QueenAnt.food_cost
? 7
-- OK! --

>>> queen = QueenAnt()
>>> queen.health
? 1
-- OK! --
```

Finally, implement the `QueenAnt`. The queen is a waterproof `ScubaThrower` that inspires her fellow ants through her bravery. In addition to the standard `ScubaThrower` action, the `QueenAnt` doubles the damage of all the ants behind her each time she performs an action. Once an ant's damage has been doubled, it is *not* doubled again for subsequent turns.

> Note: The reflected damage of a `FireAnt` should not be doubled, only the extra damage it deals when its health is reduced to 0.

| **Class**  | **Food Cost** | **Initial Health** |
| ---------- | ------------- | ------------------ |
| `QueenAnt` | 7             | 1                  |

However, with great power comes great responsibility. The `QueenAnt` is governed by three special rules:

1. If the queen ever has its health reduced to 0, the ants lose.  You will need to override `Ant.reduce_health` in `QueenAnt`  and call `ants_lose()` in that case in order to signal to the simulator  that the game is over.  (The ants also still lose if any bee reaches the end of a tunnel.)
2. There can be only one queen. A second queen cannot be constructed. To check  if an Ant can be constructed, we use the `Ant.construct()` class method to either construct an Ant if possible, or return `None` if not. You will need to override  `Ant.construct` as a class method of `QueenAnt` in order to add this check. To keep track of whether a queen has already been created, you can use an instance variable added to the current `GameState`.
3. The queen cannot be removed. Attempts to remove the queen  should have no effect (but should not cause an error). You will need to override `Ant.remove_from` in `QueenAnt` to enforce this condition.

> *Hint:* Think about how you can call the `construct` method of the superclass of `QueenAnt`. Remember that you ultimately want to construct a `QueenAnt`, not a regular `Ant` or a `ScubaThrower`.

> *Hint:* You can find each `Place` in a tunnel behind the `QueenAnt` by starting at the ant's `place.exit` and then repeatedly following its `exit`. The `exit` of a `Place` at the end of a tunnel is `None`.

> *Hint:* To avoid doubling an ant's damage twice, mark the ants that have been buffed in some way, in a way that persists across calls to `QueenAnt.action`.

> *Hint:* When buffing the ants' damage, keep in mind that there can be more than one ant in a `Place`, such as if one ant is guarding another.

After writing code, test your implementation:

```
python3 ok -q 12
```

### Extra Credit (2 pt)

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem EC > Suite 1 > Case 1
(cases remaining: 10)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> # Testing status parameters
>>> slow = SlowThrower()
>>> scary = ScaryThrower()
>>> SlowThrower.food_cost
? 4
-- OK! --

>>> ScaryThrower.food_cost
? 6
-- OK! --

>>> slow.health
? 1
-- OK! --

>>> scary.health
? 1
-- OK! --

---------------------------------------------------------------------
Problem EC > Suite 1 > Case 2
(cases remaining: 9)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> # Testing Slow
>>> slow = SlowThrower()
>>> bee = Bee(3)
>>> gamestate.places["tunnel_0_0"].add_insect(slow)
>>> gamestate.places["tunnel_0_4"].add_insect(bee)
>>> slow.action(gamestate)
>>> gamestate.time = 1
>>> bee.action(gamestate)
>>> bee.place.name # SlowThrower should cause slowness on odd turns
? "tunnel_0_4"
-- OK! --

>>> gamestate.time += 1
>>> bee.action(gamestate)
>>> bee.place.name # SlowThrower should cause slowness on odd turns
? "tunnel_0_3"
-- OK! --

>>> for _ in range(3):
...    gamestate.time += 1
...    bee.action(gamestate)
>>> bee.place.name
? "tunnel_0_2"
-- Not quite. Try again! --

? "tunnel_0_1"
-- OK! --

---------------------------------------------------------------------
Problem EC > Suite 1 > Case 3
(cases remaining: 8)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> # Testing Scare
>>> scary = ScaryThrower()
>>> bee = Bee(3)
>>> gamestate.places["tunnel_0_0"].add_insect(scary)
>>> gamestate.places["tunnel_0_4"].add_insect(bee)
>>> scary.action(gamestate)
>>> bee.action(gamestate)
>>> bee.place.name # ScaryThrower should scare for two turns
? "tunnel_0_4"
-- Not quite. Try again! --

? "tunnel_0_5"
-- OK! --

>>> bee.action(gamestate)
>>> bee.place.name # ScaryThrower should scare for two turns
? "tunnel_0_5"
-- Not quite. Try again! --

? "tunnel_0_6"
-- OK! --

>>> bee.action(gamestate)
>>> bee.place.name
? "tunnel_0_5"
-- OK! --

---------------------------------------------------------------------
Problem EC > Suite 1 > Case 4
(cases remaining: 7)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> # Scary stings an ant
>>> scary = ScaryThrower()
>>> harvester = HarvesterAnt()
>>> bee = Bee(3)
>>> gamestate.places["tunnel_0_0"].add_insect(scary)
>>> gamestate.places["tunnel_0_4"].add_insect(bee)
>>> gamestate.places["tunnel_0_5"].add_insect(harvester)
>>> scary.action(gamestate)
>>> bee.action(gamestate)
>>> bee.place.name # ScaryThrower should scare for two turns
? "tunnel_0_5"
-- OK! --

>>> harvester.health
? 1
-- OK! --

>>> bee.action(gamestate)
>>> harvester.health
? 0
-- OK! --

---------------------------------------------------------------------
Problem EC > Suite 1 > Case 10
(cases remaining: 1)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> ScaryThrower.implemented
? True
-- OK! --

>>> SlowThrower.implemented
? True
-- OK! -- 
```

Implement two final thrower ants that do zero damage, but instead apply a temporary "status" on the `action` method of a `Bee` instance that they `throw_at`. This "status" lasts for a certain number of turns, after which it ceases to take effect.

We will be implementing two new ants that inherit from `ThrowerAnt`.

- `SlowThrower` throws sticky syrup at a bee, slowing it for 3 turns. When a bee is slowed, it can only move on turns when `gamestate.time` is even, and **can do nothing otherwise**. If a bee is hit by syrup while  it is already slowed, it is slowed for an additional 3 turns.
- `ScaryThrower` intimidates a nearby bee, causing it to back away instead of  advancing. (If the bee is already right next to the Hive and cannot go back further,  it should not move. To check if a bee is next to the Hive, you might find the `is_hive` instance attribute of `Place`s useful).  Bees remain scared until they have tried to back away twice. Bees cannot try to back away if they are slowed and `gamestate.time` is odd. *Once a bee has been scared once, it can't be scared ever again.*

| **Class**      | **Food Cost** | **Initial Health** |
| -------------- | ------------- | ------------------ |
| `SlowThrower`  | 4             | 1                  |
| `ScaryThrower` | 6             | 1                  |

In order to complete the implementations of these two ants, you will need to set their class attributes appropriately and implement the `slow` and `scare` methods on `Bee`, which apply their respective statuses on a particular bee. You may also have to edit some other methods of `Bee`.

You can run some provided tests, but they are not exhaustive:

```
python3 ok -q EC
```

Make sure to test your code!  Your code should be able to apply multiple statuses on a target; each new status applies to the current (possibly previously affected) action method of the bee.

## Optional Problems

### Optional Problem 1

Before writing any code, read the instructions and test your understanding of the problem:

```
---------------------------------------------------------------------
Problem Optional 1 > Suite 1 > Case 1
(cases remaining: 15)

Q: Which Ant types have a blocks_path attribute?
Choose the number of the correct choice:
0) All Ant types except for NinjaAnt have a blocks_path attribute
1) Only the NinjaAnt has a blocks_path attribute
2) All Ant types have a blocks_path attribute that is inherited from
   the Ant superclass
3) None of the Ant subclasses have a blocks_path attribute
? 2
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 1 > Case 2
(cases remaining: 14)

Q: What is the value of blocks_path for each Ant subclass?
Choose the number of the correct choice:
0) blocks_path is False for all Ants
1) blocks_path is False for every Ant subclass except NinjaAnt
2) blocks_path is True for all Ants
3) blocks_path is True for every Ant subclass except NinjaAnt
? 3
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 1 > Case 3
(cases remaining: 13)

Q: When is the path of a Bee blocked?
Choose the number of the correct choice:
0) When there is not an NinjaAnt in the Bee's place
1) When there are no Ants in the Bee's place
2) When there is an Ant in the Bee's place
3) When there is an Ant whose blocks_path attribute is True in the
   Bee's place
? 3
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 1 > Case 4
(cases remaining: 12)

Q: What does a NinjaAnt do to each Bee that flies in its place?
Choose the number of the correct choice:
0) Nothing, the NinjaAnt doesn't damage Bees
1) Reduces the Bee's health by the NinjaAnt's damage attribute
2) Blocks the Bee's path
3) Reduces the Bee's health to 0
? 1
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 2 > Case 1
(cases remaining: 11)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing NinjaAnt parameters
>>> ninja = NinjaAnt()
>>> ninja.health
? 1
-- OK! --

>>> NinjaAnt.food_cost
? 5
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 2 > Case 2
(cases remaining: 10)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing blocks_path
>>> NinjaAnt.blocks_path
? False
-- OK! --

>>> HungryAnt.blocks_path
? True
-- OK! --

>>> FireAnt.blocks_path
? False
-- Not quite. Try again! --

? True
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 2 > Case 3
(cases remaining: 9)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing NinjaAnts do not block bees
>>> p0 = gamestate.places["tunnel_0_0"]
>>> p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
>>> bee = Bee(2)
>>> ninja = NinjaAnt()
>>> thrower = ThrowerAnt()
>>> p0.add_insect(thrower)            # Add ThrowerAnt to p0
>>> p1.add_insect(bee)
>>> p1.add_insect(ninja)              # Add the Bee and NinjaAnt to p1
>>> bee.action(gamestate)
>>> bee.place is ninja.place          # Did NinjaAnt block the Bee from moving?
? True
-- Not quite. Try again! --

? False
-- OK! --

>>> bee.place is p0
? True
-- OK! --

>>> ninja.health
? 1
-- OK! --

>>> bee.action(gamestate)
>>> bee.place is p0                   # Did ThrowerAnt block the Bee from moving?
? True
-- OK! --

---------------------------------------------------------------------
Problem Optional 1 > Suite 2 > Case 4
(cases remaining: 8)

>>> from ants import *
>>> beehive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
>>> #
>>> # Testing non-blocking ants do not block bees
>>> p0 = gamestate.places["tunnel_0_0"]
>>> p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
>>> bee = Bee(2)
>>> ninja_fire = FireAnt(1)
>>> ninja_fire.blocks_path = False
>>> thrower = ThrowerAnt()
>>> p0.add_insect(thrower)            # Add ThrowerAnt to p0
>>> p1.add_insect(bee)
>>> p1.add_insect(ninja_fire)              # Add the Bee and NinjaAnt to p1
>>> bee.action(gamestate)
>>> bee.place is ninja_fire.place          # Did the "ninjaish" FireAnt block the Bee from moving?
? True
-- Not quite. Try again! --

? False
-- OK! --

>>> bee.place is p0
? True
-- OK! --

>>> ninja_fire.health
? 0
-- Not quite. Try again! --

? 1
-- OK! --

>>> bee.action(gamestate)
>>> bee.place is p0                   # Did ThrowerAnt block the Bee from moving?
? True
-- OK! --
```

Implement the `NinjaAnt`, which damages all `Bee`s that pass by, but can never be stung.

| **Class**  | **Food Cost** | **Initial Health** |
| ---------- | ------------- | ------------------ |
| `NinjaAnt` | 5             | 1                  |

A `NinjaAnt` does not block the path of a `Bee` that flies by. To implement this behavior, first modify the `Ant` class to include a new class attribute `blocks_path` that is set to `True`, then override the value of `blocks_path` to `False` in the `NinjaAnt` class.

Second, modify the `Bee`'s method `blocked` to return `False` if either there is no `Ant` in the `Bee`'s `place` or if there is an `Ant`, but its `blocks_path` attribute is `False`. Now `Bee`s will just fly past `NinjaAnt`s.

Finally, we want to make the `NinjaAnt` damage all `Bee`s that fly past. Implement the `action` method in `NinjaAnt` to reduce the health of all `Bee`s in the same `place` as the `NinjaAnt` by its `damage` attribute. Similar to the `FireAnt`, you must iterate over a potentially changing list of bees.

> *Hint*: Having trouble visualizing the test cases? Try drawing them out on paper! See the example in [Game Layout](https://cs61a.org/proj/ants/#game-layout) for help.

After writing code, test your implementation:

```
python3 ok -q optional1
```

For a challenge, try to win a game using only `HarvesterAnt` and `NinjaAnt`.

### Optional Problem 2

We've been developing this ant for a long time in secret. It's so dangerous that we had to lock it in the super hidden CS61A underground vault, but we finally think it is ready to go out on the field. In this problem, you'll be implementing the final ant -- `LaserAnt`, a `ThrowerAnt` with a twist.

> *Note:* There are no unlocking tests for this question.

| **Class**  | **Food Cost** | **Initial Health** |
| ---------- | ------------- | ------------------ |
| `LaserAnt` | 10            | 1                  |

The `LaserAnt` shoots out a powerful laser, damaging all that dare to stand in its path. Both `Bee`s and `Ant`s, of all types, are at risk of being damaged by `LaserAnt`. When a `LaserAnt` takes its action, it will damage all `Insect`s in its place (excluding itself, but including its container if it has one) and the `Place`s in front of it, excluding the `Hive`.

If that were it, `LaserAnt` would be too powerful for us to contain. The `LaserAnt` has a base damage of `2`. But, `LaserAnt`'s laser comes with some quirks. The laser is weakened by `0.25` each place it travels away from `LaserAnt`'s place. Additionally, `LaserAnt` has limited battery. Each time `LaserAnt` actually damages an `Insect` its laser's total damage goes down by `0.0625` (1/16). If `LaserAnt`'s damage becomes negative due to these restrictions, it simply does 0 damage instead.

> The exact order in which things are damaged within a turn is unspecified.

In order to complete the implementation of this ultimate ant, read through the `LaserAnt` class, set the class attributes appropriately, and implement the following two functions:

1. `insects_in_front` is an instance method, called by the `action` method,  that returns a dictionary where each key is an `Insect` and each  corresponding value is the distance (in places) that that `Insect` is away  from `LaserAnt`. The dictionary should include all `Insects` on the same  place or in front of the `LaserAnt`, excluding `LaserAnt` itself.
2. `calculate_damage` is an instance method that takes in `distance`, the  distance that an insect is away from the `LaserAnt` instance. It  returns the damage that the `LaserAnt` instance should afflict based on:
3. The `distance` away from the `LaserAnt` instance that an `Insect` is.
4. The number of `Insects` that this `LaserAnt` has damaged, stored in  the `insects_shot` instance attribute.

In addition to implementing the methods above, you may need to modify, add, or use class or instance attributes in the `LaserAnt` class as needed.

You can run the provided test, but it is not exhaustive:

```
python3 ok -q optional2
```

Make sure to test your code!

## Project submission

At this point, run the entire autograder to see if there are any tests that don't pass:

```
python3 ok --score
```

**You are now done with the project!**  If you haven't yet, you should try playing the game!

```
python3 gui.py [-h] [-d DIFFICULTY] [-w] [--food FOOD]
```

