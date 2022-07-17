# Homework 7: Scheme

### Scheme Editor

As you're writing your code, you can debug using the Scheme Editor. In your `scheme` folder you will find a new editor. To run this editor, run `python3 editor`. This should pop up a window in your browser; if it does not, please navigate to [localhost:31415](localhost:31415) and you should see it.

Make sure to run `python3 ok` in a separate tab or window so that the editor keeps running.

If you find that your code works in the online editor but not in your own interpreter, it's possible you have a bug in code from an earlier part that you'll have to track down. Every once in a while there's a bug that our tests don't catch, and if you find one you should let us know!

## Required Questions

### Q1: Thane of Cadr

Define the procedures `cadr` and `caddr`, which return the second and third elements of a list, respectively. If you would like a quick refresher on scheme syntax consider looking at Lab 10 Scheme Refresher.

```
(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  'YOUR-CODE-HERE
)

(define (caddr s)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
cadr-caddr > Suite 1 > Case 1
(cases remaining: 3)

scm> (load-all ".")
scm> (cddr '(1 2 3 4))
? 3
-- Not quite. Try again! --

? (3 4)
-- OK! --

---------------------------------------------------------------------
cadr-caddr > Suite 1 > Case 2
(cases remaining: 2)

scm> (load-all ".")
scm> (cadr '(1 2 3 4))
? (2 3 4)
-- Not quite. Try again! --

? 2
-- OK! --

---------------------------------------------------------------------
cadr-caddr > Suite 1 > Case 3
(cases remaining: 1)

scm> (load-all ".")
scm> (caddr '(1 2 3 4))
? 3
-- OK! --
```

#### Answer

```scheme
(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cddr s)))
```

#### Solution

Following the given example of `cddr`, defining `cadr` and `caddr` should be fairly straightforward.

Just for fun, if this were a Python linked list question instead, the solution might look something like this:

```
cadr = lambda l: l.rest.first
caddr = lambda l: l.rest.rest.first
```

### Q2: Ordered

Implement a procedure called `ordered?`, which takes a list of numbers and returns `True` if the numbers are in nondescending order, and `False` otherwise.  Numbers are considered nondescending if each subsequent number is either larger or equal to the previous, that is:

```
1 2 3 3 4
```

Is nondescending, but:

```
1 2 3 3 2
```

Is not.

> *Hint*: The built-in `null?` function returns whether its argument is `nil`.

```
(define (ordered? s)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
ordered? > Suite 1 > Case 1
(cases remaining: 4)

scm> (load-all ".")
scm> (ordered? '(1 2 3 4 5))  ; #t or #f
? #t
-- OK! --

---------------------------------------------------------------------
ordered? > Suite 1 > Case 2
(cases remaining: 3)

scm> (load-all ".")
scm> (ordered? '(1 5 2 4 3))  ; #t or #f
? #f
-- OK! --

---------------------------------------------------------------------
ordered? > Suite 1 > Case 3
(cases remaining: 2)

scm> (load-all ".")
scm> (ordered? '(2 2))  ; #t or #f
? #t
-- OK! --

---------------------------------------------------------------------
ordered? > Suite 1 > Case 4
(cases remaining: 1)

scm> (load-all ".")
scm> (ordered? '(1 2 2 4 3))  ; #t or #f
? #f
-- OK! --
```

#### Answer

```scheme
(define (ordered? s)
  (cond 
    ((null? (cdr s))           #t)
    ((> (car s) (car (cdr s))) #f)
    (else                      (ordered? (cdr s)))))
```

#### Solution

```
(define (ordered? s)
  (if = 
      true
      (and (<= (car s) (car (cdr s))) (ordered? (cdr s)))))
```

We approach this much like a standard Python linked list problem.

- The base case is where `s` has zero or one items. Trivially, this is ordered.
- Otherwise we check if the first element is in order -- that is, if it's  smaller than the second element. If it's not, then the list is out of order.  Otherwise, we check if the rest of `s` is in order.

You should verify for yourself that a Python implementation of this for linked lists is similar.

### Q3: Pow

Implement a procedure `pow` for raising the number `base` to the power of a nonnegative integer `exp` for which the number of operations  grows logarithmically, rather than linearly (the number of recursive  calls should be much smaller than the input `exp`). For example, for `(pow 2 32)` should take 5 recursive calls rather than 32 recursive calls. Similarly, `(pow 2 64)` should take 6 recursive calls.

> *Hint:* Consider the following observations:
>
> 1. x^2y^ = (x^y^)^2^
> 2. x^2y+1^ = x(x^y^)^2^
>
> For example we see that 2^32^ is (2^16^)^2^, 2^16^ is (2^8^)^2^, etc. You may use the built-in predicates `even?` and `odd?`. Scheme doesn't support iteration in the same manner as Python, so consider another way to solve this problem.

```
(define (square x) (* x x))

(define (pow base exp)
  'YOUR-CODE-HERE
)
```

Use Ok to unlock and test your code:

```
---------------------------------------------------------------------
pow > Suite 1 > Case 1
(cases remaining: 4)

scm> (load-all ".")
scm> (pow 2 5)
? 32
-- OK! --

---------------------------------------------------------------------
pow > Suite 1 > Case 2
(cases remaining: 3)

scm> (load-all ".")
scm> (pow 10 3)
? 1000
-- OK! --

---------------------------------------------------------------------
pow > Suite 1 > Case 3
(cases remaining: 2)

scm> (load-all ".")
scm> (pow 3 3)
? 27
-- OK! --

---------------------------------------------------------------------
pow > Suite 1 > Case 4
(cases remaining: 1)

scm> (load-all ".")
scm> (pow 1 100000000000000) ; make sure this doesn't run forever!
? 1
-- OK! --
```

#### Answer

```scheme
(define (pow base exp)
  (cond 
    ((= base 1)
     1)
    ((= exp 1)
     base)
    ((even? exp)
     (square (pow base (/ exp 2))))
    (else
     (* base (square (pow base (/ (- exp 1) 2)))))))
```

#### Solution

```python
(define (square x) (* x x))

(define (pow base exp)
  (cond ((= exp 0) 1)
        ((even? exp) (square (pow base (/ exp 2))))
        (else (* base (pow base (- exp 1)))))
)
```

The `else` clause shows the basic recursive version of `pow` that we've seen before in class.

We save time in computation by avoiding an extra n/2 multiplications of the base. Instead, we just square the result of `base^(exp/2)`.