# Homework 1: Variables & Functions, Control                        

- **Readings:** You might find the following references  useful:
  - [Section 1.1](http://composingprograms.com/pages/11-getting-started.html)
  - [Section 1.2](http://composingprograms.com/pages/12-elements-of-programming.html)
  - [Section 1.3](http://composingprograms.com/pages/13-defining-new-functions.html)
  - [Section 1.4](http://composingprograms.com/pages/14-designing-functions.html)
  - [Section 1.5](http://composingprograms.com/pages/15-control.html)

# Required Questions

### Q2: A Plus Abs B (Failed)

Fill in the blanks in the following function for adding `a` to the absolute value of `b`, without calling `abs`. You may **not** modify any of the provided code other than the two blanks.

```python
def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs.

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    """
    if b < 0:
        f = _____
    else:
        f = _____
    return f(a, b)
```

#### Answer

```
f = a - b
f = a + b # ERROR 
```

#### Solution

```python
# Solution
f = sub
f = add
```

### Q3: Two of Three

Write a function that takes three *positive* numbers as arguments and returns the sum of the squares of the two smallest numbers. **Use only a single line for the body of the function.**

```
def two_of_three(x, y, z):
    """Return a*a + b*b, where a and b are the two smallest members of the
    positive numbers x, y, and z.

    >>> two_of_three(1, 2, 3)
    5
    >>> two_of_three(5, 3, 1)
    10
    >>> two_of_three(10, 2, 8)
    68
    >>> two_of_three(5, 5, 5)
    50
    """
    return _____
```

> **Hint:** Consider using the `max` or `min` function:
>
> ```
> >>> max(1, 2, 3)
> 3
> >>> min(-1, -2, -3)
> -3
> ```

#### Answer

```python
x*x + y*y + z*z - max(x, y, z)*max(x, y, z)
```

#### Solution

```python
# Solution
return min(x*x+y*y, x*x+z*z, y*y+z*z)
# Alternate solution
return x**2 + y**2 + z**2 - max(x, y, z)**2
```

We use the fact that if `x>y` and `y>0`, then `square(x)>square(y)`. So, we can take the `min` of the sum of squares of all pairs. The `min` function can take an arbitrary number of arguments.

Alternatively, we can do the sum of squares of all the numbers. Then we pick the largest value, and subtract the square of that.

### Q4: Largest Factor

Write a function that takes an integer `n` that is **greater than 1** and returns the largest integer that is smaller than `n` and evenly divides `n`.

```
def largest_factor(n):
    """Return the largest factor of n that is smaller than n.

    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    "*** YOUR CODE HERE ***"
```

> **Hint:** To check if `b` evenly divides `a`, you can use the expression `a % b == 0`, which can be read as, "the remainder of dividing `a` by `b` is 0."

#### Answer

```python
    k = n - 1
    while k > 0:
        if n % k == 0:
            return k
        k -= 1
```

#### Solution

```python
    factor = n - 1
    while factor > 0:
        if n % factor == 0:
            return factor
        factor -= 1
```

### Q5: If Function Refactor (Failed)

Here are two functions that have a similar structure. In both, `if` prevents a `ZeroDivisionError` when `x` is 0.

```python
def invert(x, limit):
    """Return 1/x, but with a limit.

    >>> x = 0.2
    >>> 1/x
    5.0
    >>> invert(x, 100)
    5.0
    >>> invert(x, 2)    # 2 is smaller than 5
    2

    >>> x = 0
    >>> invert(x, 100)  # No error, even though 1/x divides by 0!
    100
    """
    if x != 0:
        return min(1/x, limit)
    else:
        return limit

def change(x, y, limit):
    """Return abs(y - x) as a fraction of x, but with a limit.

    >>> x, y = 2, 5
    >>> abs(y - x) / x
    1.5
    >>> change(x, y, 100)
    1.5
    >>> change(x, y, 1)    # 1 is smaller than 1.5
    1

    >>> x = 0
    >>> change(x, y, 100)  # No error, even though abs(y - x) / x divides by 0!
    100
    """
    if x != 0:
        return min(abs(y - x) / x, limit)
    else:
        return limit
```

To "refactor" a program means to rewrite it so that it has the same behavior but with some change to the design. Below is an attempt to refactor both functions to have short one-line definitions by defining a new function `limited` that contains their common structure.

```python
def limited(x, z, limit):
    """Logic that is common to invert and change."""
    if x != 0:
        return min(z, limit)
    else:
        return limit

def invert_short(x, limit):
    """Return 1/x, but with a limit.

    >>> x = 0.2
    >>> 1/x
    5.0
    >>> invert_short(x, 100)
    5.0
    >>> invert_short(x, 2)    # 2 is smaller than 5
    2

    >>> x = 0
    >>> invert_short(x, 100)  # No error, even though 1/x divides by 0!
    100
    """
    return limited(x, 1/x, limit)

def change_short(x, y, limit):
    """Return abs(y - x) as a fraction of x, but with a limit.

    >>> x, y = 2, 5
    >>> abs(y - x) / x
    1.5
    >>> change_short(x, y, 100)
    1.5
    >>> change_short(x, y, 1)    # 1 is smaller than 1.5
    1

    >>> x = 0
    >>> change_short(x, y, 100)  # No error, even though abs(y - x) / x divides by 0!
    100
    """
    return limited(x, abs(y - x) / x, limit)
```

There's a problem with this refactored code! Try `invert_short(0, 100)` and see. It causes a `ZeroDivisionError` while `invert(0, 100)` did not.

Your first job is to understand why the behavior changed. In `invert`, division by `x` only happens when `x` is not 0, but in `invert_short` it always happens. Read the [rules of evaluation for `if` statements](http://composingprograms.com/pages/15-control.html#conditional-statements) and [call expressions](http://composingprograms.com/pages/12-elements-of-programming.html#call-expressions) to see why.

Your second job is to edit `invert_short` and `change_short` so that they have the same behavior as `invert` and `change` but **still have just one line each**. You will also need to edit `limited`. You don't need to use `and` or `or` or `if` in `invert`; just pay attention to when the division takes place.

#### Solution

```python
def limited(x, z, limit):
    """Logic that is common to invert and change."""
    if x != 0:
        return min(z / x, limit)	# EDITED
    else:
        return limit

def invert_short(x, limit):
    """Return 1/x, but with a limit.

    >>> x = 0.2
    >>> 1/x
    5.0
    >>> invert_short(x, 100)
    5.0
    >>> invert_short(x, 2)    # 2 is smaller than 5
    2

    >>> x = 0
    >>> invert_short(x, 100)  # No error, even though 1/x divides by 0!
    100
    """
    return limited(x, 1, limit)	# EDITED

def change_short(x, y, limit):
    """Return abs(y - x) as a fraction of x, but with a limit.

    >>> x, y = 2, 5
    >>> abs(y - x) / x
    1.5
    >>> change_short(x, y, 100)
    1.5
    >>> change_short(x, y, 1)    # 1 is smaller than 1.5
    1

    >>> x = 0
    >>> change_short(x, y, 100)  # No error, even though abs(y - x) / x divides by 0!
    100
    """
    return limited(x, abs(y - x), limit)	# EDITED
```

In the initial `invert_short` and `change_short`, we will first evaluate the arguments to the `limited` function call, which gives us a `ZeroDivisionError` before the call to `limited` was made.

Thus, we want to postpone the evaluation of the division so that it occurs inside the `if` statement in `limited`, **observing that dividing by `x` is another common piece of logic between `invert_short` and `change_short`.**

We can now update `invert_short` and `change_short` so they only pass in the numerator of the expression, as the denominator is the common `x` expression and now abstracted into `limited` instead. No more `ZeroDivisionError`!

### Q6: Hailstone

Douglas Hofstadter's Pulitzer-prize-winning book, *Gödel, Escher, Bach*, poses the following mathematical puzzle.

1. Pick a positive integer `n` as the start.
2. If `n` is even, divide it by 2.
3. If `n` is odd, multiply it by 3 and add 1.
4. Continue this process until `n` is 1.

The number `n` will travel up and down but eventually end at 1 (at least for all numbers that have ever been tried -- nobody has ever proved that the sequence will terminate). Analogously, a hailstone travels up and down in the atmosphere before eventually landing on earth.

This sequence of values of `n` is often called a Hailstone sequence. Write a function that takes a single argument with formal parameter name `n`, prints out the hailstone sequence starting at `n`, and returns the number of steps in the sequence:

```
def hailstone(n):
    """Print the hailstone sequence starting at n and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
```

Hailstone sequences can get quite long! Try 27. What's the longest you can find?

**Curious about hailstones or hailstone sequences? Take a look at these articles:**

- Check out [this article](https://www.nationalgeographic.org/encyclopedia/hail/) to learn more about how hailstones work!
- In 2019, there was a major [development](https://www.quantamagazine.org/mathematician-terence-tao-and-the-collatz-conjecture-20191211/) in understanding how the hailstone conjecture works for most numbers!

#### Answer

```python
    cnt = 1
    while n != 1:
        print(n)
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        cnt += 1
    print(1)
    return cnt
```

#### Solution

```python
    length = 1
    while n != 1:
        print(n)
        if n % 2 == 0:
            n = n // 2      # Integer division prevents "1.0" output
        else:
            n = 3 * n + 1
        length = length + 1
    print(n)                # n is now 1
    return length
```

We keep track of the current length of the hailstone sequence and the current value of the hailstone sequence. From there, we loop until we hit the end of the sequence, updating the length in each step.

> Note: **we need to do floor division `//` to remove decimals.**

