(define (cddr s) (cdr (cdr s)))

(define (cadr s)
    (car (cdr s))
)

(define (caddr s)
    (car (cddr s))
)

(define (ordered? s)
    (cond ((or (null? s) (null? (cdr s))) #t)
        ((< (cadr s) (car s)) #f)
        (else (ordered? (cdr s))))
)

(define (square x) (* x x))

(define (pow base exp)
    
    (define (power base exp)
            (cond ((even? exp) (square (pow base (quotient exp 2))))
                ((= exp 1) base)
                (else (* base (pow base (- exp 1)))))
            )
    (if (= base 1) 1 (power base exp))
)
