(define (over-or-under num1 num2) 
    (cond ((= num1 num2) 0)
        ((< num1 num2) -1)
        (else 1))
)

(define (make-adder num) 
    (define (adder inc)
        (+ inc num)
    )
    adder)

(define (composed f g) 
    (define (combined x)
        (f (g x))
    )
    combined
)

(define lst
        (let ((t (cons 1 nil))
              (l (cons 3 (cons 4 nil))))
          (cons t (cons 2 (cons l (cons 5 nil))))))

(define (remove item lst)
    (filter (lambda (x) (not (equal? x item))) lst)
)
