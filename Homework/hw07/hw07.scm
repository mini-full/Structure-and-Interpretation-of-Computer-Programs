(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cddr s)))

(define (ordered? s)
  (cond 
    ((null? (cdr s))           #t)
    ((> (car s) (car (cdr s))) #f)
    (else                      (ordered? (cdr s)))))

(define (square x) (* x x))

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
