# Lab 1: Variables & Functions, Control

# Quick Logistics Review

## Using Python

When running a Python file, you can use options on the command line to inspect your code further. Here are a few that will come in handy. If you want to learn more about other Python command-line options, take a look at the [documentation](https://docs.python.org/3.9/using/cmdline.html).

- Using no command-line options will run the code in the file you  provide and return you to the command line. For example, if we want to run  `lab00.py` this way, we would write in the terminal:

  ```
  python3 lab00.py
  ```

- **`-i`**: The `-i` option runs your Python script, then opens an interactive session. In an interactive session, you run Python code line by line and get immediate feedback instead of running an entire file all at once. To exit,  type `exit()` into the interpreter prompt. You can also use the keyboard  shortcut `Ctrl-D` on Linux/Mac machines or `Ctrl-Z  Enter` on Windows.

  If you edit the Python file while running it interactively, you will need to exit and restart the interpreter in order for those changes to take effect.

  Here's how we can run `lab00.py` interactively:

  ```
  python3 -i lab00.py
  ```

- **`-m doctest`**: Runs doctests in a particular file. Doctests are surrounded by triple quotes (`"""`) within functions.

  Each test in the file consists of `>>>` followed by some Python code and the expected output (though the `>>>` are not seen in the output of the doctest command).

  To run doctests for `lab00.py`, we can run:

  ```
   python3 -m doctest lab00.py
  ```

## Using OK

In 61A, we use a program called Ok for autograding labs, homeworks, and projects. You should have Ok in the starter files downloaded at the start of this lab. For more information on using Ok commands, learn more [here](https://cs61a.org/articles/using-ok/).

**You can quickly generate most ok commands at [ok-help](https://go.cs61a.org/ok-help).**

To use Ok to run doctests for a specified function, run the following command:

```
python3 ok -q <specified function>
```

By default, only tests that did not pass will show up. You can use the `-v` option to show all tests, including tests you have passed:

```
python3 ok -v
```

You can also use the debug printing feature in OK by writing

```
print("DEBUG:", x)
```

## Pair programming

Pair programming is a way to program collaboratively with a partner. It's a great approach when you're learning how to program, plus it's used by many companies in the tech industry.

In pair programming, partners are working together *at the same time*. One partner is the "driver," who actually types the code. The other partner is the "navigator," who observes, asks questions, suggests solutions, and thinks about slightly longer-term strategies.

It's very important for partners to switch roles throughout an assignment, either every 10-20 minutes or alternating each problem.

Pair programming is as much about communication styles as it is about  coding styles, so it's important to find a partner that you are able to  communicate well with.

### Pairing Setup

#### Pairing in Person

This is the traditional approach to pair programming. Partners sit together at the same computer, ideally one with a large or double monitor. The driver controls the keyboard and mouse, while the navigator looks at the code and assignment description.

#### Remote Pairing

Fortunately, it is also very possible to do pair programming online, thanks to the wide range of collaborative cloud applications.

You'll need two things:

- A way to hear each other.
- A way to share code and the command line.

For hearing each other, you can set up a Zoom call, Google Meet, or Discord call.

For sharing code, you can follow the instructions for your editor of choice:

- [VSCode](https://cs61a.org/articles/vscode/#pair-programming)
- [Atom](https://cs61a.org/articles/atom/#pair-programming)

You'll generally want to both be using the same editor, so you'll  either want to find a partner using the same editor or be willing to try a new editor. That can be a part of the learning experience, too!

If for some reason you're unable to do actual pairing in an editor,  you can always fall back to a shared Google Doc. Just make sure to turn  off the auto-correct in your document, or your code will get infused  with new and exciting syntax errors.

# Topics

Consult this section if you need a refresher on the material for this lab. It's okay to skip directly to [the questions](https://cs61a.org/lab/lab01/#required-questions) and refer back here should you get stuck.

## Division, Floor Div, and Modulo

Let's compare the different division-related operators in Python 3:

![image-20211104194103653](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211104194103653.png)

Notice that Python outputs `ZeroDivisionError` for certain cases. We will go over this later in this lab under [Error Messages](https://cs61a.org/lab/lab01/#error-messages).

One useful technique involving the `%` operator is to check whether a number `x` is divisible by another number `y`:

```
x % y == 0
```

For example, in order to check if `x` is an even number:

```
x % 2 == 0
```

## Functions

If we want to execute a series of statements over and over, we can abstract them away into a function to avoid repeating code.

For example, let's say we want to know the results of multiplying the numbers 1-3 by 3 and then adding 2 to it. Here's one way to do it:

```
>>> 1 * 3 + 2
5
>>> 2 * 3 + 2
8
>>> 3 * 3 + 2
11
```

If we wanted to do this with a larger set of numbers, that'd be a lot of repeated code! Let's write a function to capture this operation given any input number.

```
def foo(x):
    return x * 3 + 2
```

This function, called `foo`, takes in a single **argument** and will **return** the result of multiplying that argument by 3 and adding 2.

Now we can **call** this function whenever we want this operation to be done:

```
>>> foo(1)
5
>>> foo(2)
8
>>> foo(1000)
3002
```

Applying a function to some arguments is done with a **call expression**.

### Call expressions

A call expression applies a function, which may or may not accept arguments. The call expression evaluates to the function's return value.

The syntax of a function call:

```
  add   (    2   ,    3   )
   |         |        |
operator  operand  operand
```

Every call expression requires a set of parentheses delimiting its comma-separated operands.

To evaluate a function call:

1. Evaluate the operator, and then the operands (from left to right).
2. Apply the operator to the operands (the values of the operands).

If an operand is a nested call expression, then these two steps are applied to that inner operand first in order to evaluate the outer operand.

### `return` and `print`

Most functions that you define will contain a `return` statement. The `return` statement will give the result of some computation back to the caller of the function and exit the function. For example, the function `square` below takes in a number `x` and returns its square.

```
def square(x):
    """
    >>> square(4)
    16
    """
    return x * x
```

When Python executes a `return` statement, the function terminates immediately. If Python reaches the end of the function body without executing a `return` statement, it will automatically return `None`.

In contrast, the `print` function is used to display values in the Terminal. This can lead to some confusion between `print` and `return` because calling a function in the Python interpreter will print out the function's return value.

However, unlike a `return` statement, when Python evaluates a `print` expression, the function does *not* terminate immediately.

```
def what_prints():
    print('Hello World!')
    return 'Exiting this function.'
    print('61A is awesome!')

>>> what_prints()
Hello World!
'Exiting this function.'
```

> Notice also that `print` will display text **without the quotes**, but `return` will preserve the quotes.

## Control

### Boolean Operators

Python supports three boolean operators: `and`, `or`, and `not`:

```
>>> a = 4
>>> a < 2 and a > 0
False
>>> a < 2 or a > 0
True
>>> not (a > 0)
False
```

- `and` evaluates to `True` only if both operands evaluate to `True`.  If at least one operand is `False`, then `and` evaluates to `False`.
- `or` evaluates to `True` if at least one operand evaluates to `True`.  If both operands are `False`, then `or` evaluates to `False`.
- `not` evaluates to `True` if its operand evaluates to `False`. It evaluates  to `False` if its operand evalutes to `True`.

What do you think the following expression evaluates to? Try it out in the Python interpreter.

```
>>> True and not False or not True and False
```

It is difficult to read complex expressions, like the one above, and understand how a program will behave. Using parentheses can make your code easier to understand. Python interprets that expression in the following way:

```
>>> (True and (not False)) or ((not True) and False)
```

This is because boolean operators, like arithmetic operators, have an order of operation:

- `not` has the highest priority
- `and`
- `or` has the lowest priority

**Truthy and Falsey Values**: It turns out `and` and `or` work on more than just booleans (`True`, `False`). Python values such as `0`, `None`, `''` (the empty string), and `[]` (the empty list) are considered false values. *All* other values are considered true values.

What do you think will happen if we type the following into Python?

```
1 / 0
```

Try it out in Python! You should see a `ZeroDivisionError`. But what about this expression?

```
True or 1 / 0
```

It evaluates to `True` because Python's `and` and `or` operators *short-circuit*. That is, they don't necessarily evaluate every operand.

| Operator | Checks if:                 | Evaluates from left to right up to: | Example                                |
| -------- | -------------------------- | ----------------------------------- | -------------------------------------- |
| AND      | All values are true        | The first false value               | `False and 1 / 0` evaluates to `False` |
| OR       | At least one value is true | The first true value                | `True or 1 / 0` evaluates to `True`    |

Short-circuiting happens when the operator reaches an operand that  allows them to make a conclusion about the expression. For example, `and` will short-circuit as soon as it reaches the first false value because it then knows that not all the values are true.

**If `and` and `or` do not *short-circuit*, they just return the last value**; another way to remember this is that `and` and `or` always return the last thing they evaluate, whether they short circuit or not. **Keep in mind that `and` and `or` don't always return booleans when using values other than `True` and `False`.**

### If Statements

You can review the syntax of `if` statements in [Section 1.5.4](http://composingprograms.com/pages/15-control.html#conditional-statements) of Composing Programs.

> *Tip*: We sometimes see code that looks like this:
>
> ```
> if x > 3:
>     return True
> else:
>     return False
> ```
>
> This can be written more concisely as `return x > 3`. If your code looks like the code above, see if you can rewrite it more clearly!

### While Loops

You can review the syntax of `while` loops in [Section 1.5.5](http://composingprograms.com/pages/15-control.html#iteration) of Composing Programs.

## Error Messages

By now, you've probably seen a couple of error messages. They might look intimidating, but error messages are very helpful for debugging code. The following are some common types of errors:

| Error Types       | Descriptions                                                 |
| ----------------- | ------------------------------------------------------------ |
| SyntaxError       | Contained improper syntax (e.g. missing a colon after an `if` statement or forgetting to close parentheses/quotes) |
| IndentationError  | Contained improper indentation (e.g. inconsistent indentation of a function body) |
| TypeError         | Attempted operation on incompatible types (e.g.  trying to add a function and a number) or called function with the wrong number of arguments |
| ZeroDivisionError | Attempted division by zero                                   |

Using these descriptions of error messages, you should be able to get a better idea of what went wrong with your code. **If you run into error messages, try to identify the problem before asking for help.** You can often Google unfamiliar error messages to see if others have made similar mistakes to help you debug.

For example:

```
>>> square(3, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: square() takes 1 positional argument but 2 were given
```

Note:

- The last line of an error message tells us the type of the error. In the  example above, we have a `TypeError`.
- The error message tells us what we did wrong -- we gave `square` 2 arguments  when it can only take in 1 argument. In general, the last line is the most  helpful.
- The second to last line of the error message tells us on which line the  error occurred. This helps us track down the error. In the example above,  `TypeError` occurred at `line 1`.  

# Required Questions

## What Would Python Display? (WWPD)

### Q1: WWPD: Control

```
>>> def xk(c, d):
...     if c == 4:
...         return 6
...     elif d >= 4:
...         return 6 + 7 + c
...     else:
...         return 25
>>> xk(10, 10)
23
>>> xk(10, 6)
23
>>> xk(4, 6)
6
>>> xk(0, 0)
25
```

```
>>> def how_big(x):
...     if x > 10:
...         print('huge')
...     elif x > 5:
...         return 'big'
...     elif x > 0:
...         print('small')
...     else:
...         print("nothing")
>>> how_big(7)
'big'
>>> how_big(12)
'huge'
-- Not quite. Try again! --
huge
-- OK! --
>>> how_big(1)
small
>>> how_big(-1)
nothing
```

```
>>> n = 3
>>> while n >= 0:
...     n -= 1
...     print(n)
(line 1)? 2
(line 2)? 1
(line 3)? 0
(line 4)? -1
```

> *Hint*: Make sure your `while` loop conditions eventually evaluate to a false value, or they'll never stop! Typing `Ctrl-C` will stop infinite loops in the interpreter.

```
>>> positive = 28
>>> while positive:
...    print("positive?")
...    positive -= 3
Infinite Loop
```

```
>>> positive = -9
>>> negative = -12
>>> while negative:
...    if positive:
...        print(negative)
...    positive += 3
...    negative += 3
(line 1)? -12
(line 2)? -9
(line 3)? -6
```

### Q2: WWPD: Veritasiness

```
>>> True and 13
? True
-- Not quite. Try again! --
? 13
-- OK! --
>>> False or 0
0F
>>> not 10
False
>>> not None
True
```

```
>>> True and 1 / 0 and False
Error
>>> True or 1 / 0 or False
True
>>> True and 0
False
-- Not quite. Try again! --
0
-- OK! --
>>> False or 1
1
>>> 1 and 3 and 6 and 10 and 15
15
>>> -1 and 1 > 0
True
>>> 0 or False or 2 or 1 / 0
2
```

```
>>> not 0
True
>>> (1 + 1) and 1
1
>>> 1/0 or True
Error
>>> (True or False) and False
False
```

### Q3: Debugging Quiz

The following is a quick quiz on different debugging techniques that will be helpful for you to use in this class. You can refer to the [debugging article](https://cs61a.org/articles/debugging/) to answer the questions.

```
Q: In the following traceback, what is the most recent function call?
Traceback (most recent call last):
    File "temp.py", line 10, in <module>
      f("hi")
    File "temp.py", line 2, in f
      return g(x + x, x)
    File "temp.py", line 5, in g
      return h(x + y * 5)
    File "temp.py", line 8, in h
      return x + 0
  TypeError: must be str, not int
Choose the number of the correct choice:
0) g(x + x, x)
1) h(x + y * 5)
2) f("hi")
? 1
-- OK! --

Q: In the following traceback, what is the cause of this error?
Traceback (most recent call last):
    File "temp.py", line 10, in <module>
      f("hi")
    File "temp.py", line 2, in f
      return g(x + x, x)
    File "temp.py", line 5, in g
      return h(x + y * 5)
    File "temp.py", line 8, in h
      return x + 0
  TypeError: must be str, not int
Choose the number of the correct choice:
0) the code looped infinitely
1) there was a missing return statement
2) the code attempted to add a string to an integer
? 2
-- OK! --

Q: How do you write a doctest asserting that square(2) == 4?
Choose the number of the correct choice:
0) def square(x):
       '''
       square(2)
       4
       '''
       return x * x
1) def square(x):
       '''
       input: 2
       output: 4
       '''
       return x * x
2) def square(x):
       '''
       >>> square(2)
       4
       '''
       return x * x
3) def square(x):
       '''
       doctest: (2, 4)
       '''
       return x * x
? 2
-- OK! -

Q: When should you use print statements?
Choose the number of the correct choice:
0) To investigate the values of variables at certain points in your code
1) For permanant debugging so you can have long term confidence in your code
2) To ensure that certain conditions are true at certain points in your code
? 0
-- OK! --

Q: How do you prevent the ok autograder from interpreting print statements as output?
Choose the number of the correct choice:
0) You don't need to do anything, ok only looks at returned values, not printed values
1) Print with # at the front of the outputted line
2) Print with 'DEBUG:' at the front of the outputted line
? 2
-- OK! --

Q: What is the best way to open an interactive terminal to investigate a failing test for question sum_digits in assignment lab01?
Choose the number of the correct choice:
0) python3 ok -q sum_digits --trace
1) python3 -i lab01.py
2) python3 ok -q sum_digits -i
3) python3 ok -q sum_digits
? 2
-- OK! --

Q: What is the best way to look at an environment diagram to investigate a failing test for question sum_digits in assignment lab01?
Choose the number of the correct choice:
0) python3 ok -q sum_digits
1) python3 ok -q sum_digits --trace
2) python3 ok -q sum_digits -i
3) python3 -i lab01.py
? 1
-- OK! --W

Q: Which of the following is NOT true?
Choose the number of the correct choice:
0) It is generally bad practice to release code with debugging print statements left in
1) Debugging is not a substitute for testing
2) It is generally good practice to release code with assertion statements left in
3) Code that returns a wrong answer instead of crashing is generally better as it at least works fine
4) Testing is very important to ensure robust code
? 3
-- OK! --
```

## Coding Practice

### Q4: Falling Factorial

Let's write a function `falling`, which is a "falling" factorial that takes two arguments, `n` and `k`, and returns the product of `k` consecutive numbers, starting from `n` and working downwards. When `k` is 0, the function should return 1.

```
def falling(n, k):
    """Compute the falling factorial of n to depth k.

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    >>> falling(4, 0)
    1
    """
    "*** YOUR CODE HERE ***"
```


#### Solution

```
    total, stop = 1, n-k
    while n > stop:
        total, n = total*n, n-1
    return total
```

#### Answer

```
    ans = 1
    while k > 0:
        k -= 1 
        ans *= n
        n -= 1
    return ans
```


### Q5: Sum Digits

Write a function that takes in a nonnegative integer and sums its digits. (Using floor division and modulo might be helpful here!)

```
def sum_digits(y):
    """Sum all the digits of y.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123) # make sure that you are using return rather than print
    >>> a
    6
    """
    "*** YOUR CODE HERE ***"
```


#### Answer

```
    sum = 0
    while y != 0:
        sum += y % 10
        y = y // 10
    return sum
```

#### Solution

```
    total = 0
    while y > 0:
        total, y = total + y % 10, y // 10
    return total
```

# Extra Practice

> These questions are optional and will not affect your score on this assignment. However, they are **great practice** for future assignments, projects, and exams. Attempting these questions can be valuable in helping cement your knowledge of course concepts.

### Q6: WWPD: What If?

> **Hint**: `print` (unlike `return`) does *not* cause the function to exit.

```
>>> def ab(c, d):
...     if c > 5:
...         print(c)
...     elif c > 7:
...         print(d)
...     print('foo')
>>> ab(10, 20)
(line 1)? 10
(line 2)? foo
-- OK! --
>>> def bake(cake, make):
...     if cake == 0:
...         cake = cake + 1
...         print(cake)
...     if cake == 1:
...         print(make)
...     else:
...         return cake
...     return make
>>> bake(0, 29)
(line 1)? 1
(line 2)? 29
(line 3)? 29
-- OK! --
>>> bake(1, "mashed potatoes")
(line 1)? mashed potatoes
(line 2)? "mashed potatoes"
-- OK! --
```

### Q7: Double Eights

Write a function that takes in a number and determines if the digits contain two adjacent 8s.

```
def double_eights(n):
    """Return true if n has two eights in a row.
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```
    flag = False # one eight's appearance flag
    while n > 0:
        if n % 10 != 8:
            flag = False
        elif flag:
            return True
        else:
            flag = True
        n = n // 10
    return False
```

#### Solution

```
    prev_eight = False
    while n > 0:
        last_digit = n % 10
        if last_digit == 8 and prev_eight:
            return True
        elif last_digit == 8:
            prev_eight = True
        else:
            prev_eight = False
        n = n // 10
    return False
```

