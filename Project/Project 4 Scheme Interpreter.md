# Project 4: Scheme Interpreter

> Eval calls apply,
> which just calls eval again!
> When does it all end?

## Introduction

> **Note:** If you're interested in an alternate "extreme" version of this project that gives you *considerably less* guidance, you can try the [Scheme Challenge Version](https://cs61a.org/proj/scheme_stubbed/)! For grading purposes, completing either version of the project (this version or the Challenge version) will be equivalent.

In this project, you will develop an interpreter for a subset of the Scheme language. As you proceed, think about the issues that arise in the design of a programming language; many quirks of languages are byproducts of implementation decisions in interpreters and compilers. The subset of the language used in this project is described in the [functional programming](http://composingprograms.com/pages/32-functional-programming.html) section of Composing Programs, as well as this [language specification](https://cs61a.org/articles/scheme-spec/) and [built-in procedure reference](https://cs61a.org/articles/scheme-builtins/) for the CS 61A subset of Scheme that you'll be building in this project.

Watch (or attend) the lectures on Calculator and Interpreters for an overview of the project.

![Money Tree](https://cs61a.org/proj/scheme/images/money_tree.png)

In addition, there will be a completely optional open-ended art contest (released separately) that challenges you to produce recursive images in only a few lines of Scheme. As an example, the picture above abstractly depicts all the ways of making change for $0.50 using U.S. currency. All flowers appear at the end of a branch with length 50. Small angles in a branch indicate an additional coin, while large angles indicate a new currency denomination. In the contest, you too will have the chance to unleash your inner recursive artist.

## Download starter files

You can download all of the project code as a [zip archive](https://cs61a.org/proj/scheme/scheme.zip).

Files you will edit:

- `scheme_eval_apply.py`: the recursive evaluator for Scheme expressions
- `scheme_forms.py`: evaluation for special forms
- `scheme_classes.py`: classes that describe Scheme expressions
- `questions.scm`: contains skeleton code for Part III

The rest of the files in the project:

- `scheme.py`: the interpreter REPL
- `pair.py`: defines the `Pair` class and the `nil` object
- `scheme_builtins.py`: built-in Scheme procedures
- `scheme_reader.py`: the reader for Scheme input (this file is obfuscated so that you can implement it in lab)
- `scheme_tokens.py`: the tokenizer for Scheme input
- `scheme_utils.py`: functions for inspecting Scheme expressions
- `ucb.py`: utility functions for use in 61A projects
- `tests.scm`: a collection of test cases written in Scheme
- `ok`: the autograder
- `tests`: a directory of tests used by `ok`
- `mytests.rst`: a file where you can add your own tests

## Logistics

28 points are assigned for correctness, which is including 1 point for passing `tests.scm`. 

You can get 2 EC points for submitting the extra credit problem.

You will turn in the following files:

- `scheme_eval_apply.py`
- `scheme_forms.py`
- `scheme_classes.py`
- `questions.scm`

You do not need to modify or turn in any other files to complete the project.

For the functions that we ask you to complete, there may be some initial code that we provide. If you would rather not use that code, feel free to delete it and start from scratch. You may also add new function definitions as you see fit.

However, please do **not** modify any other functions.  Doing so may result in your code failing our autograder tests. Also, please do not change any function signatures (names, argument order, or number of arguments).

Throughout this project, you should be testing the correctness of your code. It is good practice to test often, so that it is easy to isolate any problems. However, you should not be testing *too* often, to allow yourself time to think through problems.

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

## Interpreter details

### Scheme features

**Read-Eval-Print.** The interpreter reads Scheme expressions, evaluates them, and displays the results.

```
scm> 2
2
scm> (+ 2 3)
5
scm> ((lambda (x) (* x x)) 5)
25
```

The starter code for your Scheme interpreter can successfully evaluate the first expression above, since it consists of a single number. The second (a call to a built-in procedure) and the third (a computation of 5 squared) will not work just yet.

**Load.** You can load a file by passing in a symbol for the file name. For example, to load `tests.scm`, evaluate the following call expression.

```
scm> (load 'tests)
```

**Symbols.** Various dialects of Scheme are more or less permissive about identifiers (which serve as symbols and variable names).

Our rule is that:

> An identifier is a sequence of letters (a-z and A-Z), digits, and characters in `!$%&*/:<=>?@^_~-+.` that do not form a valid integer or floating-point numeral and are not existing special form shorthands.

Our version of Scheme is case-insensitive: two identifiers are considered identical if they match except possibly in the capitalization of letters. They are internally represented and printed in lower case:

```
scm> 'Hello
hello
```

**Turtle Graphics.** In addition to standard Scheme procedures, we include procedure calls to the Python `turtle` package. This will come in handy for the contest. You **do not** have to install this package in order to participate.

If you're curious, you can read the [turtle module documentation](http://docs.python.org/py3k/library/turtle.html) online.

### Running the interpreter

To start an interactive Scheme interpreter session, type:

```
python3 scheme.py
```

Currently, your Scheme interpreter can handle a few simple expressions, such as:

```
scm> 1
1
scm> 42
42
scm> true
#t
```

To exit the Scheme interpreter, press `Ctrl-d` or evaluate the `exit` procedure (after completing problems 3 and 4):

```
scm> (exit)
```

You can use your Scheme interpreter to evaluate the expressions in an input file by passing the file name as a command-line argument to `scheme.py`:

```
python3 scheme.py tests.scm
```

The `tests.scm` file contains a long list of sample Scheme expressions and their expected values. Many of these examples are from Chapters 1 and 2 of [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-4.html#%_toc_start), the textbook from which Composing Programs is adapted.

## Part I: The Evaluator

In Part I, you will develop the following features of the interpreter:

- Symbol evaluation
- Calling built-in procedures
- Definitions

In the starter implementation given to you, the evaluator can only evaluate self-evaluating expressions: numbers, booleans, and `nil`.

First, read the relevant code.  In the "Eval/Apply" section of `scheme_eval_apply.py`:

- `scheme_eval` evaluates a Scheme expression in the given environment. This  function is nearly complete but is missing the logic for call expressions.
- When evaluating a special form, `scheme_eval` redirects evaluation to an  appropriate `do_?_form` function found in `scheme_forms.py`
- `scheme_apply` applies a procedure to some arguments. This function has cases  for the various types of procedures (builtin procedures, user-defined  procedures, and so forth) that you will implement.

In the "Environments and Procedures" section of `scheme_classes.py`:

- The `Frame` class implements an environment frame.
- The `LambdaProcedure` class (in the Procedures section) represents  user-defined procedures.

These are all of the essential components of the interpreter. `scheme_forms.py` defines special forms, `scheme_builtins.py` defines the various functions built into the standard library,  and `scheme.py` defines input/output behavior.

Use Ok to test your understanding:

```
---------------------------------------------------------------------
Understanding Eval/Apply > Suite 1 > Case 1
(cases remaining: 5)

Q: What types of expressions are represented as Pairs?
Choose the number of the correct choice:
0) All expressions are represented as Pairs
1) Only call expressions
2) Call expressions and special forms
3) Only special forms
? 0
-- Not quite. Try again! --

? 2
-- OK! --

---------------------------------------------------------------------
Understanding Eval/Apply > Suite 1 > Case 2
(cases remaining: 4)

Q: What expression in the body of scheme_eval finds the value of a name?
Choose the number of the correct choice:
0) scheme_forms.SPECIAL_FORMS[first](rest, env)
1) scheme_symbolp(expr)
2) env.lookup(expr)
3) env.find(name)
? 2
-- OK! --

---------------------------------------------------------------------
Understanding Eval/Apply > Suite 1 > Case 3
(cases remaining: 3)

Q: How do we know if a given combination is a special form?
Choose the number of the correct choice:
0) Check if the first element in the list is a symbol
1) Check if the first element in the list is a symbol and that the
   symbol is in the dictionary SPECIAL_FORMS
2) Check if the expression is in the dictionary SPECIAL_FORMS
? 1
-- OK! --

---------------------------------------------------------------------
Understanding Eval/Apply > Suite 1 > Case 4
(cases remaining: 2)

Q: What is the difference between applying builtins and applying user-defined procedures?
(Choose all that apply)

I.   User-defined procedures open a new frame; builtins do not
II.  Builtins simply execute a predefined function; user-defined
     procedures must evaluate additional expressions in the body
III. Builtins have a fixed number of arguments; user-defined procedures do not

---
Choose the number of the correct choice:
0) III only
1) II only
2) I only
3) I, II and III
4) I and II
5) I and III
6) II and III
0 1 6
-- Not quite. Try again! --

? 4
-- OK! --

---------------------------------------------------------------------
Understanding Eval/Apply > Suite 1 > Case 5
(cases remaining: 1)

Q: What exception should be raised for the expression (1)?
Choose the number of the correct choice:
0) SchemeError("malformed list: (1)")
1) AssertionError
2) SchemeError("unknown identifier: 1")
3) SchemeError("1 is not callable")
? 3
-- OK! --
```

[Builtin-Function in Python create frame](https://www.youtube.com/watch?v=NGlzYXvDk5o&t=606s)

### Problem 1 (1 pt)

Implement the `define` and `lookup` methods of the `Frame` class, in `scheme_classes.py`. Each `Frame` object has the following instance attributes:

- `bindings` is a dictionary representing the bindings in the frame. It maps  Scheme symbols (represented as Python strings) to Scheme values.
- `parent` is the parent `Frame` instance. The parent of the Global Frame is  `None`.

\1) `define` takes a symbol (represented by a Python string) and a value. It   binds the symbol to the value in the `Frame` instance.

\2) `lookup` takes a symbol and returns the value bound to that symbol in the   first frame of the environment in which the symbol is bound. The   *environment* for a `Frame` instance consists of that frame, its parent frame, and all its ancestor frames, including the Global Frame.

- If the symbol is bound in the current frame, return its value.
- If the symbol is not bound in the current frame, and the frame has a parent frame, continue lookup in the parent frame.
- If the symbol is not found in the current frame and there is no parent frame,   raise a `SchemeError`.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 1 > Suite 1 > Case 1
(cases remaining: 5)

>>> from scheme import *
>>> global_frame = create_global_frame()
>>> global_frame.define("x", 3)
>>> global_frame.parent is None
? True
-- OK! --

>>> global_frame.lookup("x")
? 3
-- OK! --

>>> global_frame.define("x", 2)
>>> global_frame.lookup("x")
? 2
-- OK! --

>>> global_frame.lookup("foo")
Choose the number of the correct choice:
0) SchemeError
1) 3
2) None
? 0
-- OK! --

---------------------------------------------------------------------
Problem 1 > Suite 1 > Case 2
(cases remaining: 4)

>>> from scheme import *
>>> first_frame = create_global_frame()
>>> first_frame.define("x", 3)
>>> first_frame.define("y", False)
>>> second_frame = Frame(first_frame)
>>> second_frame.parent == first_frame
? True
-- OK! --

>>> second_frame.lookup("x")
? 3
-- OK! --

>>> second_frame.lookup("y")
? False
-- OK! --
```

After you complete this problem, you can start your Scheme interpreter (with `python3 scheme.py`). You should be able to look up built-in procedure names:

```
scm> +
#[+]
scm> odd?
#[odd?]
```

However, your Scheme interpreter will still not be able to call these procedures. Let's fix that.

Remember, at this point you can only exit the interpreter by pressing `Ctrl-d`.

### Problem 2 (2 pt)

To be able to call built-in procedures, such as `+`, you need to complete the `BuiltinProcedure` case within the `scheme_apply` function in `scheme_eval_apply.py`. Built-in procedures are applied by calling a corresponding Python function that implements the procedure.

> To see a list of all Scheme built-in procedures used in the project, look in the `scheme_builtins.py` file. Any function decorated with `@builtin` will be added to the globally-defined `BUILTINS` list.

A `BuiltinProcedure` has two instance attributes:

- `py_func`: the *Python* function that implements the built-in Scheme procedure.
- `expect_env`: a Boolean flag that indicates whether or not this built-in  procedure will expect the current environment to be passed in as the last  argument. The environment is required, for instance, to implement the built-in  `eval` procedure.

`scheme_apply` takes the `procedure` object, a list of argument values, and the current environment. `args` is a Scheme list represented as a `Pair` object or `nil`. Your implementation should do the following:

- Convert the Scheme list to a Python list of arguments. *Hint:* `args` is a  Pair, which has a `.first` and `.rest` similar to a Linked List. Think about  how you would put the values of a Linked List into a list.
- If `procedure.expect_env` is `True`, then add the current environment `env`  as the last argument to this Python list.
- Call `procedure.py_func` on all of those arguments using `*args` notation (`f(1, 2,  3)` is equivalent to `f(*[1, 2, 3]`)).
- If calling the function results in a `TypeError` exception being raised, then  the wrong number of arguments were passed. Use a `try`/`except` block to  intercept the exception and raise a `SchemeError` with the message  `'incorrect number of arguments'`.
- Otherwise, `scheme_apply` should return the value obtained by calling `procedure.py_func`

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 2 > Suite 1 > Case 1
(cases remaining: 9)

>>> from scheme import *
>>> env = create_global_frame()
>>> twos = Pair(2, Pair(2, nil))
>>> plus = BuiltinProcedure(scheme_add) # + procedure
>>> scheme_apply(plus, twos, env) # Type SchemeError if you think this errors
? 4
-- OK! --

---------------------------------------------------------------------
Problem 2 > Suite 1 > Case 2
(cases remaining: 8)

>>> from scheme import *
>>> env = create_global_frame()
>>> plus = BuiltinProcedure(scheme_add) # + procedure
>>> scheme_apply(plus, nil, env) # Remember what (+) evaluates to in scheme
? 0
-- OK! --

---------------------------------------------------------------------
Problem 2 > Suite 1 > Case 3
(cases remaining: 7)

>>> from scheme import *
>>> env = create_global_frame()
>>> twos = Pair(2, Pair(2, nil))
>>> oddp = BuiltinProcedure(scheme_oddp) # odd? procedure
>>> scheme_apply(oddp, twos, env) # Type SchemeError if you think this errors
? SchemeError
-- OK! --
```

[Pair programming?](https://cs61a.org/articles/pair-programming) Remember to alternate between driver and navigator roles. The driver controls the keyboard; the navigator watches, asks questions, and suggests ideas.

### Problem 3 (2 pt)

The `scheme_eval` function (in `scheme_eval_apply.py`) evaluates a Scheme expression (represented as a `Pair`) in a given environment. The provided code already looks up names in the current environment, returns self-evaluating expressions (such as numbers) and evaluates special forms.

Implement the missing part of `scheme_eval`, which evaluates a call expression. To evaluate a call expression:

1. Evaluate the operator (which should evaluate to an instance of `Procedure`)
2. Evaluate all of the operands
3. Apply the procedure on the evaluated operands by calling `scheme_apply`, then return the result

You'll have to recursively call `scheme_eval` in the first two steps. Here are some other functions/methods you should use:

- The `map` method of `Pair` returns a new Scheme list constructed by applying a  *one-argument function* to every item in a Scheme list.
- The `scheme_apply` function applies a Scheme procedure to arguments  represented as a Scheme list (a `Pair` instance).

Important: do not mutate the passed-in `expr`. That would change a program as it's being evaluated, creating strange and incorrect effects.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 3 > Suite 1 > Case 1
(cases remaining: 5)

>>> from scheme_reader import *
>>> from scheme import *
>>> expr = read_line('(+ 2 2)')
>>> scheme_eval(expr, create_global_frame()) # Type SchemeError if you think this errors
? 4
-- OK! --

>>> scheme_eval(Pair('+', Pair(2, Pair(2, nil))), create_global_frame()) # Type SchemeError if you think this errors
? 4
-- OK! --

>>> expr = read_line('(+ (+ 2 2) (+ 1 3) (* 1 4))')
>>> scheme_eval(expr, create_global_frame()) # Type SchemeError if you think this errors
? 12
-- OK! --

>>> expr = read_line('(yolo)')
>>> scheme_eval(expr, create_global_frame()) # Type SchemeError if you think this errors
? SchemeError
-- OK! --

---------------------------------------------------------------------
Problem 3 > Suite 2 > Case 1
(cases remaining: 4)


scm> (* (+ 3 2) (+ 1 7)) ; Type SchemeError if you think this errors
? 40
-- OK! --

scm> (1 2) ; Type SchemeError if you think this errors
? SchemeError
-- OK! --

scm> (1 (print 0)) ; validate_procedure should be called before operands are evaluated
? SchemeError
-- OK! --
```

> Some of these tests call a primitive (built-in) procedure called `print-then-return`. This procedure doesn't exist in Scheme, but was added to this project just to test this question. `print-then-return` takes two arguments. It prints out its first argument and returns the second.

Your interpreter should now be able to evaluate built-in procedure calls, giving you the functionality of the Calculator language and more. Run `python3 scheme.py`, and you can now add and multiply!

```
scm> (+ 1 2)
3
scm> (* 3 4 (- 5 2) 1)
36
scm> (odd? 31)
#t
```

### Problem 4 (2 pt)

The `define` special form ([spec](https://cs61a.org/articles/scheme-spec/#define)) in Scheme can be used either to assign a name to the value of a given expression or to create a procedure and bind it to a name:

```
scm> (define a (+ 2 3))  ; Binds the name a to the value of (+ 2 3)
a
scm> (define (foo x) x)  ; Creates a procedure and binds it to the name foo
foo
```

The type of the first operand tells us what is being defined:

- If it is a symbol, e.g. `a`, then the expression is defining a name
- If it is a list, e.g. `(foo x)`, then the expression is defining a procedure.

The `do_define_form` function in `scheme_forms.py` evaluates `(define ...)` expressions. There are two missing parts in this function. For this problem, implement **just the first part**, which evaluates the second operand to obtain a value and binds the first operand, a symbol, to that value. Then, `do_define_form` returns the symbol that was bound.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 1
(cases remaining: 7)

Q: What is the structure of the expressions argument to do_define_form?
Choose the number of the correct choice:
0) Pair(A, B), where:
       A is the symbol being bound,
       B is an expression whose value should be evaluated and bound to A
1) Pair('define', Pair(A, Pair(B, nil))), where:
       A is the symbol being bound,
       B is an expression whose value should be evaluated and bound to A
2) Pair(A, Pair(B, nil)), where:
       A is the symbol being bound,
       B is an expression whose value should be evaluated and bound to A
3) Pair(A, Pair(B, nil)), where:
       A is the symbol being bound,
       B is the value that should be bound to A
4) Pair(A, B), where:
       A is the symbol being bound,
       B is the value that should be bound to A
? 2
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 1 > Case 2
(cases remaining: 6)

Q: What method of a Frame instance will bind
a value to a symbol in that frame?
Choose the number of the correct choice:
0) bindings
1) define
2) lookup
3) make_child_frame
? 1
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 2 > Case 1
(cases remaining: 5)


scm> (define size 2)
? size
-- OK! --

scm> size
? 2
-- OK! --

---------------------------------------------------------------------
Problem 4 > Suite 2 > Case 2
(cases remaining: 4)


scm> (define x (+ 2 3))
? x
-- OK! --

scm> x
? 5
-- OK! --

scm> (define x (+ 2 7))
? x
-- OK! --

scm> x
? 9
-- OK! --

scm> (eval (define tau 6.28)) ; eval takes an expression represented as a list and evaluates it
? 6.28
-- OK! --
```

You should now be able to give names to values and evaluate the resulting symbols.

```
scm> (define x 15)
x
scm> (define y (* 2 x))
y
scm> y
30
scm> (+ y (* y 2) 1)
91
scm> (define x 20)
x
scm> x
20
```

Consider the following test:

```
(define x 0)
; expect x
((define x (+ x 1)) 2)
; expect Error
x
; expect 1
```

Here, an Error is raised because the operator does not evaluate to a procedure. However, if the operator is evaluated multiple times before raising an error, `x` will be bound to 2 instead of 1, causing the test to fail. Therefore, if your interpreter fails this test, you'll want to make sure you only evaluate the operator once in `scheme_eval`.

### Problem 5 (1 pt)

In Scheme, you can quote expressions in two ways: with the `quote` special form ([spec](https://cs61a.org/articles/scheme-spec/#quote)) or with the symbol `'`.  The reader converts `'...` into `(quote ...)`, so that your interpreter only needs to evaluate the `(quote ...)` syntax. The `quote` special form returns its operand expression without evaluating it:

```
scm> (quote hello)
hello
scm> '(cons 1 2)  ; Equivalent to (quote (cons 1 2))
(cons 1 2)
```

Implement the `do_quote_form` function in `scheme_forms.py` so that it simply returns the unevaluated operand of the `(quote ...)` expression.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 5 > Suite 1 > Case 1
(cases remaining: 4)

Q: What is the structure of the expressions argument to do_quote_form?
Choose the number of the correct choice:
0) A, where:
       A is the quoted expression
1) [A], where:
       A is the quoted expression
2) Pair('quote', Pair(A, nil)), where:
       A is the quoted expression
3) Pair(A, nil), where:
       A is the quoted expression
? 3
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 2 > Case 1
(cases remaining: 3)

>>> from scheme import *
>>> global_frame = create_global_frame()
>>> do_quote_form(Pair(3, nil), global_frame)
? Pair(3, nil)
-- Not quite. Try again! --

? (3)
-- OK! --

>>> do_quote_form(Pair('hi', nil), global_frame)
? ('hi')
-- OK! --

>>> expr = Pair(Pair('+', Pair('x', Pair(2, nil))), nil)
>>> do_quote_form(expr, global_frame) # Make sure to use Pair notation
? (+ x 2)
-- Not quite. Try again! --

? Pair('+', Pair('x', Pair(2, nil)))
-- OK! --

---------------------------------------------------------------------
Problem 5 > Suite 3 > Case 1
(cases remaining: 2)


scm> ''hello
Choose the number of the correct choice:
0) (quote (quote (hello)))
1) hello
2) (hello)
3) (quote hello)
? 0
-- Not quite. Try again! --

Choose the number of the correct choice:
0) (quote (quote (hello)))
1) hello
2) (hello)
3) (quote hello)
? 3
-- OK! --

scm> (quote (1 2))
? (1 2)
-- OK! --

scm> (car '(1 2 3))
? (2 3)
-- Not quite. Try again! --

? (1)
-- Not quite. Try again! --

? 1
-- OK! --

scm> (cdr '(1 2))
? (2)
-- OK! --

scm> (cons 'car '('(4 2)))
? (car ('4 2))
-- Not quite. Try again! --

? (car '(4 2))
-- OK! --

scm> (eval (cons 'car '('(4 2))))
? 4
-- OK! --
```

After completing this function, you should be able to evaluate quoted expressions. Try out some of the following in your interpreter!

```
scm> (quote a)
a
scm> (quote (1 2))
(1 2)
scm> (quote (1 (2 three (4 5))))
(1 (2 three (4 5)))
scm> (car (quote (a b)))
a
scm> 'hello
hello
scm> '(1 2)
(1 2)
scm> '(1 (2 three (4 5)))
(1 (2 three (4 5)))
scm> (car '(a b))
a
scm> (eval (cons 'car '('(1 2))))
1
scm> (eval (define tau 6.28))
6.28
scm> (eval 'tau)
6.28
scm> tau
6.28
```

## Part II: Procedures

In Part II, you will add the ability to create and call user-defined procedures. You will add the following features to the interpreter:

- Lambda procedures, using the `(lambda ...)` special form
- Named lambda procedures, using the `(define (...) ...)` special form
- Mu procedures, with *dynamic scope*

### User-Defined Procedures

User-defined lambda procedures are represented as instances of the `LambdaProcedure` class. A `LambdaProcedure` instance has three instance attributes:

- `formals` is a Scheme list of the formal parameters (symbols) that name the  arguments of the procedure.
- `body` is a Scheme list of expressions; the body of the procedure.
- `env` is the environment in which the procedure was **defined**.

### Problem 6 (1 pt)

Change the `eval_all` function in `scheme_eval_apply.py` (which is called from `do_begin_form` in `scheme_forms.py`) to complete the implementation of the `begin` special form ([spec](https://cs61a.org/articles/scheme-spec/#begin)). A `begin` expression is evaluated by evaluating all sub-expressions in order. The value of the `begin` expression is the value of the final sub-expression.

```
scm> (begin (+ 2 3) (+ 5 6))
11
scm> (define x (begin (display 3) (newline) (+ 2 3)))
3
x
scm> (+ x 3)
8
scm> (begin (print 3) '(+ 2 3))
3
(+ 2 3)
```

If `eval_all` is passed an empty list of expressions (`nil`), then it should return the Python value `None`, which represents the Scheme value `undefined`.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 1
(cases remaining: 6)

>>> from scheme import *
>>> env = create_global_frame()
>>> eval_all(Pair(2, nil), env)
Choose the number of the correct choice:
0) SchemeError
1) 2
? 2
-- OK! --

>>> eval_all(Pair(4, Pair(5, nil)), env)
Choose the number of the correct choice:
0) 4
1) 5
2) (4 5)
3) SchemeError
? 3
-- Not quite. Try again! --

Choose the number of the correct choice:
0) 4
1) 5
2) (4 5)
3) SchemeError
? 2
-- Not quite. Try again! --

Choose the number of the correct choice:
0) 4
1) 5
2) (4 5)
3) SchemeError
? 1
-- OK! --

>>> eval_all(nil, env) # return None (meaning undefined)
---------------------------------------------------------------------
Problem 6 > Suite 1 > Case 2
(cases remaining: 5)

>>> from scheme import *
>>> env = create_global_frame()
>>> lst = Pair(1, Pair(2, Pair(3, nil)))
>>> eval_all(lst, env)
? 3
-- OK! --

>>> lst     # The list should not be mutated!
? Pair(1, Pair(2, Pair(3, nil)))
-- OK! --

---------------------------------------------------------------------
Problem 6 > Suite 2 > Case 1
(cases remaining: 4)


scm> (begin (+ 2 3) (+ 5 6))
? 11
-- OK! --

scm> (begin (define x 3) x)
? 3
-- OK! --

---------------------------------------------------------------------
Problem 6 > Suite 2 > Case 2
(cases remaining: 3)


scm> (begin 30 '(+ 2 2))
Choose the number of the correct choice:
0) 4
1) '(+ 2 2)
2) 30
3) (+ 2 2)
? 3
-- OK! --

scm> (define x 0)
? x
-- OK! --

scm> (begin (define x (+ x 1)) 42 (define y (+ x 1)))
? 2
-- Not quite. Try again! --

? y
-- OK! --

scm> x
? 1
-- OK! --

scm> y
? 2
-- OK! --
```

[Pair programming?](https://cs61a.org/articles/pair-programming) This would be a good time to switch roles. Switching roles makes sure that you both benefit from the learning experience of being in each role.

### Problem 7 (2 pt)

Implement the `do_lambda_form` function ([spec](https://cs61a.org/articles/scheme-spec/#lambda)), which creates and returns a `LambdaProcedure` instance. While you cannot call a user-defined procedure yet, you can verify that you have created the procedure correctly by typing a lambda expression into the interpreter prompt:

```
scm> (lambda (x y) (+ x y))
(lambda (x y) (+ x y))
```

In Scheme, it is legal to place more than one expression in the body of a procedure. (There must be at least one expression.) The `body` attribute of a `LambdaProcedure` instance is therefore a Scheme list of body expressions. Like a `begin` special form, evaluating the body of a procedure evaluates all body expressions in order. The return value of a procedure is the value of its last body expression.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 7 > Suite 1 > Case 1
(cases remaining: 5)


scm> (lambda (x y) (+ x y))
? (lambda (x y) (+ x y))
-- OK! --

scm> (lambda (x)) ; type SchemeError if you think this causes an error
? (lambda (x))
-- Not quite. Try again! --

? SchemeError
-- OK! --

---------------------------------------------------------------------
Problem 7 > Suite 2 > Case 1
(cases remaining: 2)

>>> from scheme_reader import *
>>> from scheme import *
>>> env = create_global_frame()
>>> lambda_line = read_line("(lambda (a b c) (+ a b c))")
>>> lambda_proc = do_lambda_form(lambda_line.rest, env)
>>> lambda_proc.formals # use single quotes ' around strings in your answer
? Pair(a, Pair(b, Pair(c, nil)))
-- Not quite. Try again! --

? Pair('a', Pair('b', Pair('c', nil)))
-- OK! --

>>> lambda_proc.body # the body is a *list* of expressions! Make sure your answer is a properly nested Pair.
? Pair('+', Pair('a', Pair('b', Pair('c', nil))))
-- Not quite. Try again! --

? Pair(Pair('+', Pair('a', Pair('b', Pair('c', nil)))), nil)
-- OK! --
```

### Problem 8 (2 pt)

Implement the `make_child_frame` method of the `Frame` class (`scheme_classes.py`), which will be used to create new frames when calling user-defined procedures. This method takes in two arguments: `formals`, which is a Scheme list of symbols, and `vals`, which is a Scheme list of values. It should return a new child frame, binding the formal parameters to the values.

To do this:

- If the number of argument values does not match with the number of formal parameters, raise a `SchemeError`.
- Create a new `Frame` instance, the parent of which is `self`.
- Bind each formal parameter to its corresponding argument value in the newly  created frame. The first symbol in `formals` should be bound to the first  value in `vals`, and so on.
- Return the new frame.

> *Hint:* The `define` method of a `Frame` instance creates a binding in that frame.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 1
(cases remaining: 6)

>>> from scheme import *
>>> global_frame = create_global_frame()
>>> formals = Pair('a', Pair('b', Pair('c', nil)))
>>> vals = Pair(1, Pair(2, Pair(3, nil)))
>>> frame = global_frame.make_child_frame(formals, vals)
>>> global_frame.lookup('a') # Type SchemeError if you think this errors
? 1
-- Not quite. Try again! --

? SchemeError
-- OK! --

>>> frame.lookup('a')        # Type SchemeError if you think this errors
? 1
-- OK! --

>>> frame.lookup('b')        # Type SchemeError if you think this errors
? 2
-- OK! --

>>> frame.lookup('c')        # Type SchemeError if you think this errors
? 3
-- OK! --

---------------------------------------------------------------------
Problem 8 > Suite 1 > Case 2
(cases remaining: 5)

>>> from scheme import *
>>> global_frame = create_global_frame()
>>> frame = global_frame.make_child_frame(nil, nil)
>>> frame.parent is global_frame
? True
-- OK! --
```

### Problem 9 (2 pt)

Implement the `LambdaProcedure` case in the `scheme_apply` function (`scheme_eval_apply.py`).

You should first create a new `Frame` instance using the `make_child_frame` method of the appropriate parent frame, binding formal parameters to argument values. Then, evaluate each of the expressions of the body of the procedure using `eval_all` within this new frame.

Your new frame should be a child of the frame in which the lambda is defined. Note that the `env` provided as an argument to `scheme_apply` is instead the frame in which the procedure is called. See [User-Defined Procedures](https://cs61a.org/proj/scheme/#user-defined-procedures) to remind yourself of the attributes of `LambdaProcedure`.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 9 > Suite 3 > Case 1
(cases remaining: 2)


scm> (define outer (lambda (x y)
....   (define inner (lambda (z x)
....     (+ x (* y 2) (* z 3))))
....   (inner x 10)))
? outer
-- OK! --

? 17
-- OK! --

scm> (define outer-func (lambda (x y)
....   (define inner (lambda (z x)
....     (+ x (* y 2) (* z 3))))
....   inner))
? outer-func
-- OK! --

scm> ((outer-func 1 2) 1 10)
? inner
-- Not quite. Try again! --

? 'inner
-- Not quite. Try again! --

? 17
-- OK! --
```

### Problem 10 (1 pt)

Currently, your Scheme interpreter is able to bind symbols to user-defined procedures in the following manner:

```
scm> (define f (lambda (x) (* x 2)))
f
```

However, we'd like to be able to use the shorthand form of defining named procedures:

```
scm> (define (f x) (* x 2))
f
```

Modify the `do_define_form` function in `scheme_forms.py` so that it correctly handles `define (...) ...)` expressions ([spec](https://cs61a.org/articles/scheme-spec/#define)).

Make sure that it can handle multi-expression bodies. For example,

```
scm> (define (g y) (print y) (+ y 1))
g
scm> (g 3)
3
4
```

Your implementation should do the following:

- Using the given variables `signature` and `expressions`, find the defined  function's name (symbol), formals, and body.
- Create a `LambdaProcedure` instance using the formals and body. *Hint:* You  can use what you've done in Problem 8 and call `do_lambda_form` on the  appropriate arguments.
- Bind the symbol to this new `LambdaProcedure` instance.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 10 > Suite 1 > Case 1
(cases remaining: 7)


scm> (define (f x y) (+ x y))
? f
-- OK! --

scm> f
Choose the number of the correct choice:
0) (define f (lambda (x y) (+ x y)))
1) (lambda (f x y) (+ x y))
2) (lambda (x y) (+ x y))
3) (f (x y) (+ x y))
? 0
-- Not quite. Try again! --

? 2
-- OK! --
```

### Problem 11 (1 pt)

All of the Scheme procedures we've seen so far use *lexical scoping*: the parent of the new call frame is the environment in which the procedure was **defined**. Another type of scoping, which is not standard in Scheme but appears in other variants of Lisp, is called *dynamic scoping*: the parent of the new call frame is the environment in which the call expression was **evaluated**. With dynamic scoping, calling the same procedure with the same arguments from different parts of your code can create different behavior (due to different parent frames).

The `mu` special form ([spec](https://cs61a.org/articles/scheme-spec/#mu); invented for this project) evaluates to a dynamically scoped procedure.

```
scm> (define f (mu () (* a b)))
f
scm> (define g (lambda () (define a 4) (define b 5) (f)))
g
scm> (g)
20
```

Above, the procedure `f` does not have `a` or `b` as arguments; however, because `f` gets called within the procedure `g`, it has access to the `a` and `b` defined in `g`'s frame.

Implement `do_mu_form` in `scheme_forms.py` to evaluate the `mu` special form. A `mu` expression  evaluates to a `MuProcedure`. Most of the `MuProcedure` class (defined in `scheme_classes.py`) has been provided for you.

In addition to implementing `do_mu_form`, complete the `MuProcedure` case within the `scheme_apply` function 13nt. When a `MuProcedure` is called, the parent of the new call frame is the environment in which that call expression was **evaluated**. As a result, a `MuProcedure` does not need to store an environment as an instance attribute.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 11 > Suite 1 > Case 1
(cases remaining: 2)


scm> (define y 1)
? y
-- OK! --

scm> (define f (mu (x) (+ x y)))
? f
-- OK! --

scm> (define g (lambda (x y) (f (+ x x))))
? g
-- OK! --

scm> (g 3 7)
? 13
-- OK! --
```

At this point in the project, your Scheme interpreter should support the following features:

- Creating procedures using `lambda` and `mu` expressions,
- Defining named procedures using `define` expressions, and
- Calling user-defined procedures.

## Part III: Special Forms

Logical special forms include `if`, `and`, `or`, and `cond`. These expressions are special because not all of their sub-expressions may be evaluated.

In Scheme, only `#f` is a false value. All other values (including `0` and `nil`) are true values. You can test whether a value is a true or false value using the provided Python functions `is_scheme_true` and `is_scheme_false`, defined in `scheme_builtins.py`.

> Scheme traditionally uses `#f` to indicate the false Boolean value. In our interpreter, that is equivalent to `false` or `False`. Similarly, `true`, `True`, and `#t` are all equivalent. However when unlocking tests, use `#t` and `#f`.

To get you started, we've provided an implementation of the `if` special form in the `do_if_form` function. Make sure you understand that implementation before starting the following questions.

### Problem 12 (2 pt)

Implement `do_and_form` and `do_or_form` so that `and` and `or` expressions ([spec](https://cs61a.org/articles/scheme-spec/#and)) are evaluated correctly.

The logical forms `and` and `or` are *short-circuiting*. For `and`, your interpreter should evaluate each sub-expression from left to right, and if any of these is a false value, return that value. Otherwise, return the value of the last sub-expression. If there are no sub-expressions in an `and` expression, it evaluates to `#t`.

```
scm> (and)
#t
scm> (and 4 5 6)  ; all operands are true values
6
scm> (and 4 5 (+ 3 3))
6
scm> (and #t #f 42 (/ 1 0))  ; short-circuiting behavior of and
#f
```

> For the `and` and `or` forms, remember to use our internal Python representations of `#t` and `#f`. See [internal representations](https://cs61a.org/lab/lab11/#internal-representations) from Lab 11.

For `or`, evaluate each sub-expression from left to right. If any sub-expression evaluates to a true value, return that value. Otherwise, return the value of the last sub-expression. If there are no sub-expressions in an `or` expression, it evaluates to `#f`.

```
scm> (or)
#f
scm> (or 5 2 1)  ; 5 is a true value
5
scm> (or #f (- 1 1) 1)  ; 0 is a true value in Scheme
0
scm> (or 4 #t (/ 1 0))  ; short-circuiting behavior of or
4
```

**Important:** Use the provided Python functions `is_scheme_true` and `is_scheme_false` from `scheme_utils.py` to test boolean values.

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 12 > Suite 1 > Case 1
(cases remaining: 9)

scm> (and)
Choose the number of the correct choice:
0) #f
1) SchemeError
2) #t
? 2
-- OK! --

scm> (and 1 #f)
Choose the number of the correct choice:
0) #t
1) #f
2) 1
? 1
-- OK! --

scm> (and (+ 1 1) 1)
? 1
-- OK! --

scm> (and #f 5)
? #f
-- OK! --

scm> (and 4 5 (+ 3 3))
? 6
-- OK! --

scm> (not (and #t #f 42 (/ 1 0)))
? #t
-- OK! --

---------------------------------------------------------------------
Problem 12 > Suite 2 > Case 1
(cases remaining: 5)

scm> (or)
? #f
-- OK! --

scm> (or (+ 1 1))
? 2
-- OK! --

scm> (not (or #f))
? #t
-- OK! --

scm> (define (zero) 0)
? zero
-- OK! --

scm> (or (zero) 3)
? 3
-- Not quite. Try again! --

? 0
-- OK! --

scm> (or 4 #t (/ 1 0))
? 4
-- OK! --
```

### Problem 13 (2 pt)

Fill in the missing parts of `do_cond_form` so that it correctly implements `cond` ([spec](https://cs61a.org/articles/scheme-spec/#cond)), returning the value of the first result sub-expression corresponding to a true predicate, or the result sub-expression corresponding to `else`.

Some special cases:

- When the true predicate does not have a corresponding result sub-expression,  return the predicate value.
- When a result sub-expression of a `cond` case has multiple expressions,  evaluate them all and return the value of the last expression. (*Hint*: Use  `eval_all`.)

Your implementation should match the following examples and the additional tests in `tests.scm`.

```
scm> (cond ((= 4 3) 'nope)
           ((= 4 4) 'hi)
           (else 'wait))
hi
scm> (cond ((= 4 3) 'wat)
           ((= 4 4))
           (else 'hm))
#t
scm> (cond ((= 4 4) 'here (+ 40 2))
           (else 'wat 0))
42
```

The value of a `cond` is `undefined` if there are no true predicates and no `else`. In such a case, `do_cond_form` should return `None`. If there is only an `else`, return its sub-expression. If it doesn't have one, return `#t`.

```
scm> (cond (False 1) (False 2))
scm> (cond (else))
#t
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 13 > Suite 1 > Case 1
(cases remaining: 6)


scm> (cond ((> 2 3) 5)
....       ((> 2 4) 6)
....       ((< 2 5) 7)
....       (else 8))
? 7
-- OK! --

scm> (cond ((> 2 3) 5)
....       ((> 2 4) 6)
....       (else 8))
? 8
-- OK! --

scm> (cond ((= 1 1))
....       ((= 4 4) 'huh)
....       (else 'no))
? #t
-- OK! --
```

### Problem 14 (2 pt)

The `let` special form ([spec](https://cs61a.org/articles/scheme-spec/#let)) binds symbols to values locally, giving them their initial values. For example:

```
scm> (define x 5)
x
scm> (define y 'bye)
y
scm> (let ((x 42)
           (y (* x 10)))  ; this x refers to the global value of x, not 42
       (list x y))
(42 50)
scm> (list x y)
(5 bye)
```

Implement `make_let_frame` in `scheme_forms.py`, which returns a child frame of `env` that binds the symbol in each element of `bindings` to the value of its corresponding expression. The `bindings` Scheme list contains pairs that each contain a symbol and a corresponding expression.

You may find the following functions and methods useful:

- `validate_form`: this function can be used to validate the structure of each  binding. It takes in a Scheme list `expr` of expressions and a `min` and `max`  length. If `expr` is not a list with length between `min` and `max` inclusive,  it raises an error. If no `max` is passed in, the default is infinity.
- `validate_formals`: this function validates that its argument is a  Scheme list of symbols for which each symbol is distinct.

Remember to refer to the [spec](https://cs61a.org/articles/scheme-spec/#let) if you don't understand any of the test cases!

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
Problem 14 > Suite 1 > Case 1
(cases remaining: 9)


scm> (define x 1)
? x
-- OK! --

scm> (let ((x 5))
....    (+ x 3))
? 8
-- OK! --

scm> x
? 1
-- OK! --

---------------------------------------------------------------------
Problem 14 > Suite 1 > Case 2
(cases remaining: 8)


scm> (let ((a 1) (b a)) b)
Choose the number of the correct choice:
0) y
1) 1
2) SchemeError
3) x
? 1
-- Not quite. Try again! --

? 2
-- OK! --

---------------------------------------------------------------------
Problem 14 > Suite 1 > Case 3
(cases remaining: 7)


scm> (let ((x 5))
....    (let ((x 2)
....          (y x))
....        (+ y (* x 2))))
? 9
-- OK! --

---------------------------------------------------------------------
Problem 14 > Suite 1 > Case 4
(cases remaining: 6)


scm> (let ((a 2) (a 3)) (+ a a)) ; how should we catch something like this?
? 6
-- Not quite. Try again! --

? SchemeError
-- OK! --

scm> (let ((y 2 3)) (+ y y)) ; should this be an allowable form?
? SchemeError
-- OK! --
```

### Additional Scheme Tests (1 pt)

Your final task in Part III of this project is to make sure that your scheme interpreter passes the additional suite of tests we have provided.

To run these tests (worth 1 point), run the command:

```
  python3 ok -q tests.scm
```

If you have passed all of the required cases, you should see 1/1 points received for `tests.scm` when you run `python ok --score`. If you are failing tests due to output from `print` statements you've added in your code for debugging, make sure to remove those as well for the tests to pass.

> One you have completed Part III, make sure you submit using OK to receive full credit for the checkpoint.
>
> ```
> python3 ok --submit
> ```
>
> If you'd like to check your score so far, use the following command:
>
> ```
> python3 ok --score
> ```
>
> **The best way to see what tests you've passed for the checkpoint is to use the score command in ok.**

Congratulations! Your Scheme interpreter implementation is now complete!

## Part IV: Write Some Scheme

Not only is your Scheme interpreter itself a tree-recursive program, but it is flexible enough to evaluate *other* recursive programs. Implement the following procedures in the `questions.scm` file.

See the [built-in procedure reference](https://cs61a.org/articles/scheme-builtins/) for descriptions of the behavior of all built-in Scheme procedure.

As you use your interpreter, you may discover additional bugs in your interpreter implementation. Therefore, you may find it useful to test your code for these questions in the staff interpreter or the [web editor](https://code.cs61a.org/scheme) and then try it in your own interpreter once you are confident your Scheme code is working. You can also use the web editor to visualize the scheme code you've written and help you debug.

### Scheme Editor

As you're writing your code, you can debug using the Scheme Editor. In your `scheme` folder you will find a new editor. To run this editor, run `python3 editor`. This should pop up a window in your browser; if it does not, please navigate to [localhost:31415](localhost:31415) and you should see it.

Make sure to run `python3 ok` in a separate tab or window so that the editor keeps running.

[Pair programming?](https://cs61a.org/articles/pair-programming) Remember to alternate between driver and navigator roles. The driver controls the keyboard; the navigator watches, asks questions, and suggests ideas.

### Problem 15 (2 pt)

Implement the `enumerate` procedure, which takes in a list of values and returns a list of two-element lists, where the first element is the index of the value, and the second element is the value itself.

```
scm> (enumerate '(3 4 5 6))
((0 3) (1 4) (2 5) (3 6))
scm> (enumerate '())
()
```

Use Ok to test your code:

```
python3 ok -q 15
```

### Problem 16 (2 pt)

Implement the `merge` procedure, which takes in a comparator function `inorder?` and two lists that are sorted, and combines the two lists into a single sorted list. A comparator defines an ordering by comparing two values and returning a true value if and only if the two values are ordered. Here, sorted means sorted according to the comparator. For example:

```
scm> (merge < '(1 4 6) '(2 5 8))
(1 2 4 5 6 8)
scm> (merge > '(6 4 1) '(8 5 2))
(8 6 5 4 2 1)
```

In case of a tie, you can choose to break the tie arbitrarily.

Use Ok to test your code:

```
python3 ok -q 16
```

## Extra Credit

### Problem EC 1 (2 pt)

Complete the function `optimize_tail_calls` in `scheme_eval_apply.py`. It returns an alternative to `scheme_eval` that is properly tail recursive. That is, the interpreter will allow an unbounded number of active tail calls in constant space. It has a third argument `tail` that indicates whether the expression to be evaluated is in a tail context.

The `Unevaluated` class represents an expression that needs to be evaluated in an environment. When `optimized_eval` receives a non-atomic expression in a tail context, it returns an `Unevaluated` instance. Otherwise, it should repeatedly call `original_scheme_eval` until the result is a value, rather than an `Unevaluated`.

**A successful implementation will require changes to several other functions, including some functions that we provided for you.** All expressions throughout your interpreter that are in a tail context should be evaluated by calling `scheme_eval` with `True` as the third argument (now called `tail`). Your goal is to determine which expressions are in a tail context throughout your code and change calls to `scheme_eval` as needed.

Once you finish, uncomment the following line in `scheme_eval_apply.py` to use your implementation:

```
scheme_eval = optimize_tail_calls(scheme_eval)
```

Use Ok to test your code:

```
python3 ok -q EC
```

## Optional Problems

### Optional Problem 1 (0 pt) (Not finished)

In Scheme, source code is data. Every non-atomic expression is written as a Scheme list, so we can write procedures that manipulate other programs just as we write procedures that manipulate lists.

Rewriting programs can be useful: we can write an interpreter that only handles a small core of the language, and then write a procedure that converts other special forms into the core language before a program is passed to the interpreter.

For example, the `let` special form is equivalent to a call expression that begins with a `lambda` expression. Both create a new frame extending the current environment and evaluate a body within that new environment.

```
(let ((a 1) (b 2)) (+ a b))
;; Is equivalent to:
((lambda (a b) (+ a b)) 1 2)
```

These expressions can be represented by the following diagrams:

| Let                                                  | Lambda                                                     |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| ![let](https://cs61a.org/proj/scheme/images/let.png) | ![lambda](https://cs61a.org/proj/scheme/images/lambda.png) |

Use this rule to implement a procedure called `let-to-lambda` that rewrites all `let` special forms into `lambda` expressions. If we quote a `let` expression and pass it into this procedure, an equivalent `lambda` expression should be returned:

```
scm> (let-to-lambda '(let ((a 1) (b 2)) (+ a b)))
((lambda (a b) (+ a b)) 1 2)
scm> (let-to-lambda '(let ((a 1)) (let ((b a)) b)))
((lambda (a) ((lambda (b) b) a)) 1)
scm> (let-to-lambda 1)
1
scm> (let-to-lambda 'a)
a
```

In order to handle all programs, `let-to-lambda` must be aware of Scheme syntax. Since Scheme expressions are recursively nested, `let-to-lambda` must also be recursive. In fact, the structure of `let-to-lambda` is somewhat similar to that of `scheme_eval`--but in Scheme!  As a reminder, atoms include numbers, booleans, nil, and symbols. You do not need to consider code that contains quasiquotation for this problem.

```
(define (let-to-lambda expr)
  (cond ((atom?   expr) <rewrite atoms>)
        ((quoted? expr) <rewrite quoted expressions>)
        ((lambda? expr) <rewrite lambda expressions>)
        ((define? expr) <rewrite define expressions>)
        ((let?    expr) <rewrite let expressions>)
        (else           <rewrite other expressions>)))
```

*Hint*: Consider how you can use `map` to convert `let` forms in every element of a list to the equivalent `lambda` form.

```
scm> (zip '((1 2) (3 4) (5 6)))
((1 3 5) (2 4 6))
scm> (zip '((1 2)))
((1) (2))
scm> (zip '())
(() ())
```

*Hint 2*: In this problem, it may be helpful to build a scheme list that evaluates to a special form (for instance, a `lambda` expression). As a related example, the following code builds a scheme list that evaluates to the expression `(define (f x) (+ x 1))`:

```
(let ((name-and-params '(f x))
      (body '(+ x 1)))
  (cons 'define
        (cons name-and-params (cons body nil))))
```

Test your implementation by running

Use Ok to test your code:

```
python3 ok -q optional_1
```

> We used `let` while defining `let-to-lambda`. What if we want to run `let-to-lambda` on an interpreter that does not recognize `let`? We can pass `let-to-lambda` to itself to rewrite itself into an *equivalent program without* `let`:
>
> ```
> ;; The let-to-lambda procedure
> (define (let-to-lambda expr)
>   ...)
> 
> ;; A list representing the let-to-lambda procedure
> (define let-to-lambda-code
>   '(define (let-to-lambda expr)
>      ...))
> 
> ;; A let-to-lambda procedure that does not use 'let'!
> (define let-to-lambda-without-let
>   (let-to-lambda let-to-lambda-code))
> ```

### Optional Problem 2 (0 pt)

Macros allow the language itself to be extended by the user. Simple macros can be provided with the `define-macro` special form. This must be used like a procedure definition, and it creates a procedure just like `define`. However, this procedure has a special evaluation rule: it is applied to its arguments without first evaluating them. Then the result of this application is evaluated.

This final evaluation step takes place in the caller's frame, as if the return value from the macro was literally pasted into the code in place of the macro.

Here is a simple example:

```
scm> (define (map f lst) (if (null? lst) nil (cons (f (car lst)) (map f (cdr lst)))))
scm> (define-macro (for formal iterable body)
....     (list 'map (list 'lambda (list formal) body) iterable))
scm> (for i '(1 2 3)
....     (print (* i i)))
1
4
9
(None None None)
```

The code above defines a macro `for` that acts as a `map` except that it doesn't need a lambda around the body.

In order to implement `define-macro`, complete the implementation for `do_define_macro`, which should create a `MacroProcedure` and bind it to the given name as in `do_define_form`. Then, update `scheme_eval` so that calls to macro procedures are evaluated correctly.

Use Ok to test your code:

```
python3 ok -q optional_2
```

### Conclusion

**Congratulations!** You have just implemented an interpreter for an entire language! If you enjoyed this project and want to extend it further, you may be interested in looking at more advanced features, like [let* and letrec](http://schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.2.2), [unquote splicing](http://schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.2.6), [error tracing](https://en.wikipedia.org/wiki/Stack_trace), and [continuations](https://en.wikipedia.org/wiki/Call-with-current-continuation).

Submit to Ok to complete the project.

```
python3 ok --submit
```

If you have a partner, make sure to add them to the submission on okpy.org.