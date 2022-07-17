# Homework 8: Scheme

## Instructions

**Readings:** You might find the following references  useful:

- [Scheme Specification](https://cs61a.org/articles/scheme-spec/)
- [Scheme Built-in Procedure Reference](https://cs61a.org/articles/scheme-builtins/)

You may find it useful to try [code.cs61a.org/scheme](https://code.cs61a.org/scheme) when working through problems, as it can draw environment and box-and-pointer diagrams and it lets you walk your code step-by-step (similar to Python Tutor). Don't forget to submit your code through Ok though!

### Scheme Editor

As you're writing your code, you can debug using the Scheme Editor. In your `scheme` folder you will find a new editor. To run this editor, run `python3 editor`. This should pop up a window in your browser; if it does not, please navigate to [localhost:31415](localhost:31415) and you should see it.

Make sure to run `python3 ok` in a separate tab or window so that the editor keeps running.

If you find that your code works in the online editor but not in your own interpreter, it's possible you have a bug in code from an earlier  part that you'll have to track down. Every once in a while there's a bug that our tests don't catch, and if you find one you should let us know!

## Required Questions

### Q1: My Filter

Write a procedure `my-filter`, which takes a predicate `func` and a list `lst`, and returns a new list containing only elements of the list that satisfy the predicate. The output should contain the elements in the same order that they appeared in the original list.

**Note:** Make sure that you are not just calling the built-in `filter` function in Scheme - we are asking you to re-implement this!

```
(define (my-filter func lst)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
my-filter > Suite 1 > Case 1
(cases remaining: 6)

scm> (load-all ".")
scm> (my-filter even? '(1 2 3 4))
? (2 4)
-- OK! --

---------------------------------------------------------------------
my-filter > Suite 1 > Case 2
(cases remaining: 5)

scm> (load-all ".")
scm> (my-filter odd? '(1 3 5))
? (1 3 5)
-- OK! --

---------------------------------------------------------------------
my-filter > Suite 1 > Case 3
(cases remaining: 4)

scm> (load-all ".")
scm> (my-filter odd? '(2 4 6 1))
? (1)
-- OK! --

---------------------------------------------------------------------
my-filter > Suite 1 > Case 4
(cases remaining: 3)

scm> (load-all ".")
scm> (my-filter even? '(3))
? ()
-- OK! --

---------------------------------------------------------------------
my-filter > Suite 1 > Case 5
(cases remaining: 2)

scm> (load-all ".")
scm> (my-filter odd? nil)
? (nil)
-- Not quite. Try again! --

? ()
-- OK! --

---------------------------------------------------------------------
my-filter > Suite 2 > Case 1
(cases remaining: 1)

scm> (define filter nil)
scm> (load-all ".")
scm> (my-filter even? '(1 2 3 4)) ; checks you dont use builtin filter
? (2 4)
-- OK! --
```

#### Answer

```scheme
(define (my-filter func lst)
  (if (null? lst)
      '()
      (if (func (car lst))
          (cons (car lst) (my-filter func (cdr lst)))
          (my-filter func (cdr lst)))))
```

#### Solution

```scheme
(define (my-filter func lst)
  (cond ((null? lst) '())
        ((func (car lst)) (cons (car lst) (my-filter func (cdr lst))))
        (else (my-filter func (cdr lst))))
)
```

### Q2: Interleave

Implement the function `interleave`, which takes a two lists `s1` and `s2` as arguments. `interleave` should return a new list that interleaves the elements of the two lists. (In other words, the resulting list should contain elements alternating between `s1` and `s2`.)

If one of the input lists to `interleave` is shorter than the other, then `interleave` should alternate elements from both lists until one list has no more elements, and then the remaining elements from the longer list should be added to the end of the new list.

```
(define (interleave s1 s2)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
interleave > Suite 1 > Case 1
(cases remaining: 6)

scm> (load-all ".")
scm> (interleave (list 1 3 5) (list 2 4))
? (1 2 3 4 5)
-- OK! --

---------------------------------------------------------------------
interleave > Suite 1 > Case 2
(cases remaining: 5)

scm> (load-all ".")
scm> (interleave (list 2 4) (list 1 3 5))
? (2 1 4 3 5)
-- OK! --

---------------------------------------------------------------------
interleave > Suite 1 > Case 3
(cases remaining: 4)

scm> (load-all ".")
scm> (interleave (list 1 2) (list 1 2))
? (1 1 2 2)
-- OK! --

---------------------------------------------------------------------
interleave > Suite 1 > Case 4
(cases remaining: 3)

scm> (load-all ".")
scm> (interleave '(1 2 3 4 5 6) '(7 8))
? (1 7 2 8 3 4 5 6)
-- OK! --

---------------------------------------------------------------------
interleave > Suite 2 > Case 1
(cases remaining: 2)

scm> (load-all ".")
scm> (interleave (list 1 3 5) (list 2 4 6))
? (1 2 3 4 5 6)
-- OK! --

---------------------------------------------------------------------
interleave > Suite 2 > Case 2
(cases remaining: 1)

scm> (load-all ".")
scm> (interleave (list 1 3 5) nil)
? (1 3 5)
-- OK! --

scm> (interleave nil (list 1 3 5))
? (1 3 5)
-- OK! --

scm> (interleave nil nil)
? ()
-- OK! --
```

#### Answer

```scheme
(define (interleave s1 s2)
  (cond 
    ((null? s1)
     s2)
    ((null? s2)
     s1)
    (else
     (append (list (car s1) (car s2))
             (interleave (cdr s1) (cdr s2))))))
```

#### Solution

```scheme
(define (interleave s1 s2)
  (if (or (null? s1) (null? s2))
      (append s1 s2)
      (cons (car s1)
            (cons (car s2)
                  (interleave (cdr s1) (cdr s2)))))
)
```

### Q3: Accumulate

Fill in the definition for the procedure `accumulate`, which merges the first `n` natural numbers (ie. 1 to n, inclusive) according to the following parameters:

1. `merger`: a function of two arguments
2. `start`: a number with which we start merging with
3. `n`: the number of natural numbers to merge
4. `term`: a function of one argument that computes the *n*th term of  a sequence

For example, we can find the product of all the numbers from 1 to 5 by using the multiplication operator as the `merger`, and starting our product at 1:

```
scm> (define (identity x) x)
scm> (accumulate * 1 5 identity)  ; 1 * 1 * 2 * 3 * 4 * 5
120
```

We can also find the sum of the squares of the same numbers by using the addition operator as the `merger` and `square` as the `term`:

```
scm> (define (square x) (* x x))
scm> (accumulate + 0 5 square)  ; 0 + 1^2 + 2^2 + 3^2 + 4^2 + 5^2
55
scm> (accumulate + 5 5 square)  ; 5 + 1^2 + 2^2 + 3^2 + 4^2 + 5^2
60
```

You may assume that the `merger` will always be commutative: i.e. the order of arguments do not matter.

> **Hint:** You may find it useful to refer to the recursive implementation of `accumulate` we implemented in Python in [HW 2](https://cs61a.org/hw/hw02).

```
(define (accumulate merger start n term)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
accumulate > Suite 1 > Case 1
(cases remaining: 2)

scm> (load-all ".")
scm> (define (identity x) x)
scm> (accumulate * 1 5 identity)
? 120
-- OK! --

---------------------------------------------------------------------
accumulate > Suite 2 > Case 1
(cases remaining: 1)

scm> (load-all ".")
scm> (define (square x) (* x x))
? square
-- OK! --

scm> (accumulate + 0 5 square)
? 55
-- OK! --

scm> (accumulate + 5 5 square)
? 60
-- OK! --
```

#### Answer

```scheme
(define (accumulate merger start n term)
  (if (= n 0)
      start
      (accumulate merger
                  (merger start (term n))
                  (- n 1)
                  term)))
```

### Q4: No Repeats

Implement `no-repeats`, which takes a list of numbers `lst` as input and returns a list that has all of the unique elements of `lst` in the order that they first appear, but no repeats. For example, `(no-repeats (list 5 4 5 4 2 2))` evaluates to `(5 4 2)`.

> **Hint:** How can you make the first time you see an element in the input list be the first and only time you see the element in the resulting list you return?

> **Hint:** You may find it helpful to use the `my-filter` procedure with a helper `lambda` function to use as a filter. To test if two numbers are equal, use the `=` procedure. To test if two numbers are not equal, use the `not` procedure in combination with `=.`

```
(define (no-repeats lst)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
no-repeats > Suite 1 > Case 1
(cases remaining: 7)

scm> (load-all ".")
scm> (no-repeats '(5 4 3 2 1))
? (5 4 3 2 1)
-- OK! --

---------------------------------------------------------------------
no-repeats > Suite 1 > Case 2
(cases remaining: 6)

scm> (load-all ".")
scm> (no-repeats '(5 4 3 2 1 1))
? (5 4 3 2 1)
-- OK! --

---------------------------------------------------------------------
no-repeats > Suite 1 > Case 3
(cases remaining: 5)

scm> (load-all ".")
scm> (no-repeats '(5 5 4 3 2 1))
? (5 4 3 2 1)
-- OK! --

---------------------------------------------------------------------
no-repeats > Suite 1 > Case 4
(cases remaining: 4)

scm> (load-all ".")
scm> (no-repeats '(12))
? (12)
-- OK! --

---------------------------------------------------------------------
no-repeats > Suite 1 > Case 5
(cases remaining: 3)

scm> (load-all ".")
scm> (no-repeats '(1 1 1 1 1 1))
? (1)
-- OK! --

---------------------------------------------------------------------
no-repeats > Suite 2 > Case 1
(cases remaining: 2)

scm> (load-all ".")
scm> (no-repeats (list 5 4 2))
? (5 4 2)
-- OK! --

---------------------------------------------------------------------
no-repeats > Suite 2 > Case 2
(cases remaining: 1)

scm> (load-all ".")
scm> (no-repeats (list 5 4 5 4 2 2))
? (5 4 2)
-- OK! --

scm> (no-repeats (list 5 5 5 5 5))
? (5)
-- OK! --

scm> (no-repeats ())
? ()
-- OK! --
```

#### Answer

```scheme
(define (no-repeats lst)
  (if (null? lst)
      '()
      (cons (car lst)
            (no-repeats (my-filter
                         (lambda (element) (not (= element (car lst))))
                         lst)))))
```

#### Solution

```scheme
(define (no-repeats lst)
  (if (null? lst) lst
    (cons (car lst)
      (no-repeats (filter (lambda (x) (not (= (car lst) x))) (cdr lst)))))
)
```

