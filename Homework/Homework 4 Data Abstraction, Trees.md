# Homework 4: Data Abstraction, Trees

# Required questions

### Arms-length recursion

Before we get started, a quick comment on recursion with tree data structures. Consider the following function.

```
def min_depth(t):
    """A simple function to return the distance between t's root and its closest leaf"""
    if is_leaf(t):
        return 0 # Base case---the distance between a node and itself is zero
    h = float('inf') # Python's version of infinity
    for b in branches(t):
        if is_leaf(b): return 1 # !!!
        h = min(h, 1 + min_depth(b))
    return h
```

The line flagged with `!!!` is an "arms-length" recursion violation. Although our code works correctly when it is present, by  performing this check we are doing work that should be done by the next level of recursion — we already have an if-statement that handles any inputs to `min_depth` that are leaves, so we should not include this line to eliminate redundancy in our code.

```
def min_depth(t):
    """A simple function to return the distance between t's root and its closest leaf"""
    if is_leaf(t):
        return 0
    h = float('inf')
    for b in branches(t):
        # Still works fine!
        h = min(h, 1 + min_depth(b))
    return h
```

Arms-length recursion is not only redundant but often complicates our code and obscures the functionality of recursive functions, making writing recursive functions much more difficult. We always want our recursive case to be handling one and only one recursive level. We may or may not be checking your code periodically for things like this.

## Mobiles

**Acknowledgements** This mobile example is based on a classic problem from MIT Structure and Interpretation of Computer Programs, [Section 2.2.2](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-15.html#%_sec_2.2.2).

![image-20211122230931013](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211122230931013.png)

We are making a planetarium mobile. A mobile is a type of hanging sculpture. A binary mobile consists of two arms. Each arm is a rod of a certain length, from which hangs either a planet or another mobile. For example, the below diagram shows the left and right arms of Mobile A, and what hangs at the ends of each of those arms.

![image-20211122230940408](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211122230940408.png)

We will represent a binary mobile using the data abstractions below.

- A `mobile` must have both a left `arm` and a right `arm`.
- An `arm` has a positive length and must have something hanging at the end, either a `mobile` or `planet`.
- A `planet` has a positive size, and nothing hanging from it.

### Q2: Weights

Implement the `planet` data abstraction by completing the `planet` constructor and the `size` selector so that a planet is represented using a two-element list where the first element is the string `'planet'` and the second element is its size.

```
def mobile(left, right):
    """Construct a mobile from a left arm and a right arm."""
    assert is_arm(left), "left must be a arm"
    assert is_arm(right), "right must be a arm"
    return ['mobile', left, right]

def is_mobile(m):
    """Return whether m is a mobile."""
    return type(m) == list and len(m) == 3 and m[0] == 'mobile'

def left(m):
    """Select the left arm of a mobile."""
    assert is_mobile(m), "must call left on a mobile"
    return m[1]

def right(m):
    """Select the right arm of a mobile."""
    assert is_mobile(m), "must call right on a mobile"
    return m[2]
    
def arm(length, mobile_or_planet):
    """Construct a arm: a length of rod with a mobile or planet at the end."""
    assert is_mobile(mobile_or_planet) or is_planet(mobile_or_planet)
    return ['arm', length, mobile_or_planet]

def is_arm(s):
    """Return whether s is a arm."""
    return type(s) == list and len(s) == 3 and s[0] == 'arm'

def length(s):
    """Select the length of a arm."""
    assert is_arm(s), "must call length on a arm"
    return s[1]

def end(s):
    """Select the mobile or planet hanging at the end of a arm."""
    assert is_arm(s), "must call end on a arm"
    return s[2]
    
def planet(size):
    """Construct a planet of some size."""
    assert size > 0
    "*** YOUR CODE HERE ***"

def size(w):
    """Select the size of a planet."""
    assert is_planet(w), 'must call size on a planet'
    "*** YOUR CODE HERE ***"

def is_planet(w):
    """Whether w is a planet."""
    return type(w) == list and len(w) == 2 and w[0] == 'planet'
    
def examples():
    t = mobile(arm(1, planet(2)),
               arm(2, planet(1)))
    u = mobile(arm(5, planet(1)),
               arm(1, mobile(arm(2, planet(3)),
                              arm(3, planet(2)))))
    v = mobile(arm(4, t), arm(2, u))
    return (t, u, v)
```

The `total_weight` example is provided to demonstrate use of the mobile, arm, and planet abstractions.

```
def total_weight(m):
    """Return the total weight of m, a planet or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    >>> from construct_check import check
    >>> # checking for abstraction barrier violations by banning indexing
    >>> check(HW_SOURCE_FILE, 'total_weight', ['Index'])
    True
    """
    if is_planet(m):
        return size(m)
    else:
        assert is_mobile(m), "must get total weight of a mobile or a planet"
        return total_weight(end(left(m))) + total_weight(end(right(m)))
```

#### Answer

```python
def planet(size):
    """Construct a planet of some size."""
    assert size > 0
    return ['planet', size]


def size(w):
    """Select the size of a planet."""
    assert is_planet(w), 'must call size on a planet'
    return w[1]
```

### Q3: Balanced

Implement the `balanced` function, which returns whether `m` is a balanced mobile. A mobile is balanced if both of the following conditions are met:

1. The torque applied by its left arm is equal to that applied by its right  arm. The torque of the left arm is the length of the left rod multiplied by the total weight hanging from that rod. Likewise for the right. For example,  if the left arm has a length of `5`, and there is a `mobile` hanging at the end  of the left arm of weight `10`, the torque on the left side of our mobile is `50`.
2. Each of the mobiles hanging at the end of its arms is balanced.

Planets themselves are balanced, as there is nothing hanging off of them.

```
def balanced(m):
    """Return whether m is balanced.

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(arm(3, t), arm(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(arm(1, v), arm(1, w)))
    False
    >>> balanced(mobile(arm(1, w), arm(1, v)))
    False
    >>> from construct_check import check
    >>> # checking for abstraction barrier violations by banning indexing
    >>> check(HW_SOURCE_FILE, 'balanced', ['Index'])
    True
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    if is_planet(m):
        return True
    torque_equ = length(left(m)) * total_weight(end(left(m))) == length(right(m)) * total_weight(end(right(m)))
    return  torque_equ and balanced(end(left(m))) and balanced(end(right(m)))

```

#### Solution

```python
    if is_planet(m):
        return True
    else:
        left_end, right_end = end(left(m)), end(right(m))
        torque_left = length(left(m)) * total_weight(left_end)
        torque_right = length(right(m)) * total_weight(right_end)
        return torque_left == torque_right and balanced(left_end) and balanced(right_end)
```

The fact that planets are balanced is important, since we will be solving this recursively like many other tree problems (even though this is not explicitly a tree).

- **Base case:** if we are checking a planet, then we know that this is balanced. Why is this an appropriate base case? There are two possible approaches to this:
  1. Because we know that our data structures so far are trees, planets are the simplest possible tree since we have chosen to implement them as leaves.
  2. We also know that from a data abstraction standpoint, planets are the terminal item in a mobile. There can be no further mobile structures under this planet, so it makes sense to stop check here.
- **Otherwise:** note that it is important to do a recursive call to check if both arms are balanced. However, we also need to do the basic comparison of looking at the total weight of both arms as well as their length. For example if both arms are a planet, trivially, they will both be balanced. However, the torque must be equal in order for the entire mobile to balanced (i.e. it's insufficient to just check if the arms are balanced).

### Q4: Totals

Implement `totals_tree`, which takes in a `mobile` or `planet` and returns a `tree` whose root is the total weight of the input. For a `planet`, `totals_tree` should return a leaf. For a `mobile`, `totals_tree` should return a tree whose label is that `mobile`'s total weight, and whose branches are `totals_tree`s for the ends of its arms. As a reminder, the description of the tree data abstraction can be found [here](http://composingprograms.com/pages/23-sequences.html#trees).

```
def totals_tree(m):
    """Return a tree representing the mobile with its total weight at the root.

    >>> t, u, v = examples()
    >>> print_tree(totals_tree(t))
    3
      2
      1
    >>> print_tree(totals_tree(u))
    6
      1
      5
        3
        2
    >>> print_tree(totals_tree(v))
    9
      3
        2
        1
      6
        1
        5
          3
          2
    >>> from construct_check import check
    >>> # checking for abstraction barrier violations by banning indexing
    >>> check(HW_SOURCE_FILE, 'totals_tree', ['Index'])
    True
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    if is_planet(m):
        return tree(size(m))
    else:
        return tree(total_weight(m), [totals_tree(end(left(m))), totals_tree(end(right(m)))])
```

#### Solution

```python
    if is_planet(m):
        return tree(size(m))
    else:
        branches = [totals_tree(end(f(m))) for f in [left, right]]
        return tree(sum([label(b) for b in branches]), branches)
```

## More Trees

### Q5: Replace Loki at Leaf

Define `replace_loki_at_leaf`, which takes a tree `t` and a value `lokis_replacement`. `replace_loki_at_leaf` returns a new tree that's the same as `t` except that every leaf label equal to `"loki"` has been replaced with `lokis_replacement`.

If you want to learn about the Norse mythology referenced in this problem, you can read about it [here](https://en.wikipedia.org/wiki/Yggdrasil).

```
def replace_loki_at_leaf(t, lokis_replacement):
    """Returns a new tree where every leaf value equal to "loki" has
    been replaced with lokis_replacement.

    >>> yggdrasil = tree('odin',
    ...                  [tree('balder',
    ...                        [tree('loki'),
    ...                         tree('freya')]),
    ...                   tree('frigg',
    ...                        [tree('loki')]),
    ...                   tree('loki',
    ...                        [tree('sif'),
    ...                         tree('loki')]),
    ...                   tree('loki')])
    >>> laerad = copy_tree(yggdrasil) # copy yggdrasil for testing purposes
    >>> print_tree(replace_loki_at_leaf(yggdrasil, 'freya'))
    odin
      balder
        freya
        freya
      frigg
        freya
      loki
        sif
        freya
      freya
    >>> laerad == yggdrasil # Make sure original tree is unmodified
    True
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    if is_leaf(t):
        if label(t) == 'loki':
            return tree(lokis_replacement)
        else:
            return tree(label(t))
    else:
        return tree(label(t), [replace_loki_at_leaf(b, lokis_replacement) for b in branches(t)])
```

#### Solution

```python
    if is_leaf(t) and label(t) == "loki":
        return tree(lokis_replacement)
    else:
        bs = [replace_loki_at_leaf(b, lokis_replacement) for b in branches(t)]
        return tree(label(t), bs)
```

### Q6: Has Path

Write a function `has_path` that takes in a tree `t` and a string `word`. It returns `True` if there is a path that starts from the root where the entries along the path spell out the `word`, and `False` otherwise. (This data structure is called a trie, and it has a lot of cool applications, such as autocomplete). You may assume that every node's `label` is exactly one character.

```
def has_path(t, word):
    """Return whether there is a path in a tree where the entries along the path
    spell out a particular word.

    >>> greetings = tree('h', [tree('i'),
    ...                        tree('e', [tree('l', [tree('l', [tree('o')])]),
    ...                                   tree('y')])])
    >>> print_tree(greetings)
    h
      i
      e
        l
          l
            o
        y
    >>> has_path(greetings, 'h')
    True
    >>> has_path(greetings, 'i')
    False
    >>> has_path(greetings, 'hi')
    True
    >>> has_path(greetings, 'hello')
    True
    >>> has_path(greetings, 'hey')
    True
    >>> has_path(greetings, 'bye')
    False
    >>> has_path(greetings, 'hint')
    False
    """
    assert len(word) > 0, 'no path for empty word.'
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    if label(t) == word[0]:
        if not word[1:]:
            return True
        else:
            return True in [has_path(b, word[1:]) for b in branches(t)]
    else:
        return False
```

#### Solution

```python
    if label(t) != word[0]:
        return False
    elif len(word) == 1:
        return True
    for b in branches(t):
        if has_path(b, word[1:]):
            return True
    return False
```

# Optional Questions

## Trees

### Q7: Preorder

Define the function `preorder`, which takes in a tree as an argument and returns a list of all the entries in the tree in the order that `print_tree` would print them.

The following diagram shows the order that the nodes would get printed, with the arrows representing function calls.

![image-20211123134729325](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211123134729325.png)

> Note: This ordering of the nodes in a tree is called a preorder traversal.

```
def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal (see problem description).

    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> preorder(numbers)
    [1, 2, 3, 4, 5, 6, 7]
    >>> preorder(tree(2, [tree(4, [tree(6)])]))
    [2, 4, 6]
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal (see problem description).

    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> preorder(numbers)
    [1, 2, 3, 4, 5, 6, 7]
    >>> preorder(tree(2, [tree(4, [tree(6)])]))
    [2, 4, 6]
    """
    if is_leaf(t):
        return [label(t)]
    else:
        return [label(t)] + sum([preorder(b) for b in branches(t)], [])
    
    
    # Improved
    return sum([preorder(b) for b in branches(t)], [label(t)])
```

#### Solution

```python
   if branches(t) == []:
        return [label(t)]
    flattened_branches = []
    for child in branches(t):
        flattened_branches += preorder(child)
    return [label(t)] + flattened_branches

# Alternate solution
from functools import reduce

def preorder_alt(t):
    return reduce(add, [preorder_alt(child) for child in branches(t)], [label(t)])
```

## Data Abstraction

> Feel free to reference [Section 2.2](http://composingprograms.com/pages/22-data-abstraction.html) for more information on data abstraction.

**Acknowledgements.** This interval arithmetic example is based on a classic problem from Structure and Interpretation of Computer Programs, [Section 2.1.4](https://sarabander.github.io/sicp/html/2_002e1.xhtml#g_t2_002e1_002e4).

**Introduction.** Alyssa P. Hacker is designing a system to help people solve engineering problems. One feature she wants to provide in her system is the ability to manipulate inexact quantities (such as measurements from physical devices) with known precision, so that when computations are done with such approximate quantities the results will be numbers of known precision. For example, if a measured quantity x lies between two numbers a and b, Alyssa would like her system to use this range in computations involving x.

Alyssa's idea is to implement interval arithmetic as a set of arithmetic operations for combining "intervals" (objects that represent the range of possible values of an inexact quantity). The result of adding, subracting, multiplying, or dividing two intervals is also an interval, one that represents the range of the result.

Alyssa suggests the existence of an abstraction called an "interval" that has two endpoints: a lower bound and an upper bound. She also presumes that, given the endpoints of an interval, she can create the interval using data abstraction. Using this constructor and the appropriate selectors, she defines the following operations:

```
def str_interval(x):
    """Return a string representation of interval x."""
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))

def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y."""
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)
```

### Q8: Interval Abstraction

Alyssa's program is incomplete because she has not specified the implementation of the interval abstraction. She has implemented the constructor for you; fill in the implementation of the selectors.

```
def interval(a, b):
    """Construct an interval from a to b."""
    assert a <= b, 'Lower bound cannot be greater than upper bound'
    return [a, b]

def lower_bound(x):
    """Return the lower bound of interval x."""
    "*** YOUR CODE HERE ***"

def upper_bound(x):
    """Return the upper bound of interval x."""
    "*** YOUR CODE HERE ***"
```

Use Ok to unlock and test your code:

```
>>> import hw04
>>> from hw04 import *
>>> str_interval(interval(-1, 2))
? -1 to 2
-- Not quite. Try again! --

? '-1 to 2'
-- OK! --

>>> str_interval(add_interval(interval(-1, 2), interval(4, 8)))
? '3 to 10'
-- OK! --
```

#### Answer

```python
def lower_bound(x):
    """Return the lower bound of interval x."""
    return x[0]


def upper_bound(x):
    """Return the upper bound of interval x."""
    return x[1]
```

### Q9: Interval Arithmetic

After implementing the abstraction, Alyssa decided to implement a few interval arithmetic functions.

This is her current implementation for **interval multiplication**. Unfortunately there are some data abstraction violations, so your task is to fix this code before [someone sets it on fire](https://youtu.be/7zu30DhJLKU?t=444).

```
def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y."""
    p1 = x[0] * y[0]
    p2 = x[0] * y[1]
    p3 = x[1] * y[0]
    p4 = x[1] * y[1]
    return [min(p1, p2, p3, p4), max(p1, p2, p3, p4)]
```

Use Ok to unlock and test your code:

```
python3 ok -q mul_interval -umul_interval > Suite 1 > Case 1
(cases remaining: 2)

>>> import hw04
>>> from hw04 import *
>>> str_interval(mul_interval(interval(-1, 2), interval(4, 8)))
? '-8 to 16'
-- OK! --
```

#### Answer

```python
def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y."""
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))	# watch out!
```

**Interval Subtraction**

Using a similar approach as `mul_interval` and `add_interval`, define a subtraction function for intervals. If you find yourself repeating code, see if you can reuse functions that have already been implemented.

```
def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y."""
    "*** YOUR CODE HERE ***"
```

Use Ok to unlock and test your code:

```
sub_interval > Suite 1 > Case 1
(cases remaining: 2)

>>> import hw04
>>> from hw04 import *
>>> str_interval(sub_interval(interval(-1, 2), interval(4, 8)))
? '-9 to -2'
-- OK! --
```

#### Answer

```python
def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y."""
    p1 = lower_bound(x) - lower_bound(y)
    p2 = lower_bound(x) - upper_bound(y)
    p3 = upper_bound(x) - lower_bound(y)
    p4 = upper_bound(x) - upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))
```

#### Solution

```python
def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y."""
    negative_y = interval(-upper_bound(y), -lower_bound(y))
    return add_interval(x, negative_y)
```

**Interval Division**

Alyssa implements division below by multiplying by the reciprocal of `y`. A systems programmer looks over Alyssa's shoulder and comments that it is not clear what it means to divide by an interval that spans zero. Add an `assert` statement to Alyssa's code to ensure that no such interval is used as a divisor:

```
def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided by
    any value in y. Division is implemented as the multiplication of x by the
    reciprocal of y."""
    "*** YOUR CODE HERE ***"
    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
div_interval > Suite 1 > Case 1
(cases remaining: 2)

>>> import hw04
>>> from hw04 import *
>>> # Type AssertionError if you think an AssertionError is raised
>>> str_interval(div_interval(interval(-1, 2), interval(4, 8)))
? '-0.125 to 0.5'
-- Not quite. Try again! --

? '-0.125 to 0'
-- Not quite. Try again! --

? AssertionError
-- Not quite. Try again! --

? -0.25 to 0.5
-- Not quite. Try again! --

? '-0.25 to 0.5'
-- OK! --

---------------------------------------------------------------------
div_interval > Suite 1 > Case 1
(cases remaining: 2)

>>> import hw04
>>> from hw04 import *
>>> # Type AssertionError if you think an AssertionError is raised
>>> str_interval(div_interval(interval(-1, 2), interval(4, 8)))
'-0.25 to 0.5'
>>> str_interval(div_interval(interval(4, 8), interval(-1, 2)))
? AssertionError
-- OK! --
```

#### Answer

```python
def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided by
    any value in y. Division is implemented as the multiplication of x by the
    reciprocal of y."""
    assert not lower_bound(y) <= 0 <= upper_bound(y), 'Spans zero'
    reciprocal_y = interval(1 / upper_bound(y), 1 / lower_bound(y))
    return mul_interval(x, reciprocal_y)
```

#### Solution

```python
    assert not (lower_bound(y) <= 0 <= upper_bound(y)), 'Divide by zero'
```

assert 后的条件应该被满足，不被满足则抛出AssertionError

### Q10: Par Diff

After considerable work, Alyssa P. Hacker delivers her finished system.  Several years later, after she has forgotten all about it, she gets a frenzied call from an irate user, Lem E. Tweakit. It seems that Lem has noticed that the [formula for parallel resistors](https://en.wikipedia.org/wiki/Series_and_parallel_circuits#Resistors_2) can be written in two algebraically equivalent ways:

```
par1(r1, r2) = (r1 * r2) / (r1 + r2)
```

or

```
par2(r1, r2) = 1 / (1/r1 + 1/r2)
```

He has written the following two programs, each of which computes the `parallel_resistors` formula differently:

```
def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))

def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))
```

Lem points out that Alyssa's program gives different answers for the two ways of computing. Find two intervals `r1` and `r2` that demonstrate the difference in behavior between `par1` and `par2` when passed into each of the two functions.

Demonstrate that Lem is right. Investigate the behavior of the system on a variety of arithmetic expressions. Make some intervals `r1` and `r2`, and show that `par1` and `par2` can give different results.

```
def check_par():
    """Return two intervals that give different results for parallel resistors.

    >>> r1, r2 = check_par()
    >>> x = par1(r1, r2)
    >>> y = par2(r1, r2)
    >>> lower_bound(x) != lower_bound(y) or upper_bound(x) != upper_bound(y)
    True
    """
    r1 = interval(1, 1) # Replace this line!
    r2 = interval(1, 1) # Replace this line!
    return r1, r2
```

#### Solution (?)

```python
    r1 = interval(1, 2)
    r2 = interval(3, 4)
```

### Q11: Multiple References (Not Finished)

Eva Lu Ator, another user, has also noticed the different intervals computed by different but algebraically equivalent expressions. She says that the problem is multiple references to the same interval.

The Multiple References Problem: a formula to compute with intervals using Alyssa's system will produce tighter error bounds if it can be written in such a form that no variable that represents an uncertain number is repeated.

Thus, she says, `par2` is a better program for parallel resistances than `par1` (see Q10: Par Diff for these functions!). Is she right? Why? Write a function that returns a string containing a written explanation of your answer:

Note: To make a multi-line string, you must use triple quotes `""" like this """`.

```
def multiple_references_explanation():
    return """The multiple reference problem..."""
```

#### Solution

```python
def multiple_references_explanation():
    return """The multiple reference problem exists.  The true value
    within a particular interval is fixed (though unknown).  Nested
    combinations that refer to the same interval twice may assume two different
    true values for the same interval, which is an error that results in
    intervals that are larger than they should be.

    Consider the case of i * i, where i is an interval from -1 to 1.  No value
    within this interval, when squared, will give a negative result.  However,
    our mul_interval function will allow us to choose 1 from the first
    reference to i and -1 from the second, giving an erroneous lower bound of
    -1.

    Hence, a program like par2 is better than par1 because it never combines
    the same interval more than once.
    """
```

### Q12: Quadratic (Not Finished)

Write a function `quadratic` that returns the interval of all values `f(t)` such that `t` is in the argument interval `x` and `f(t)` is a [quadratic function](http://en.wikipedia.org/wiki/Quadratic_function):

```
f(t) = a*t*t + b*t + c
```

Make sure that your implementation returns the smallest such interval, one that does not suffer from the multiple references problem.

*Hint*: the derivative `f'(t) = 2*a*t + b`, and so the extreme point of the quadratic is `-b/(2*a)`:

```
def quadratic(x, a, b, c):
    """Return the interval that is the range of the quadratic defined by
    coefficients a, b, and c, for domain interval x.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    "*** YOUR CODE HERE ***"
```

#### Solution

```
    extremum = -b / (2*a)
    f = lambda x: a * x * x + b * x + c
    l, u, e = map(f, (lower_bound(x), upper_bound(x), extremum))
    if extremum >= lower_bound(x) and extremum <= upper_bound(x):
        return interval(min(l, u, e), max(l, u, e))
    else:
        return interval(min(l, u), max(l, u))
```

