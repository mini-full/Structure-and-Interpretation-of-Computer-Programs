(define (split-at lst n)
    (define (split lstsofar rest i)
        (cond
            ((null? rest) (cons lstsofar nil))
            ((= i 0) (cons lstsofar rest))
            ((null? lstsofar) (split (list (car rest)) (cdr rest) (- i 1)))
            (else (split (append lstsofar (list (car rest))) (cdr rest) (- i 1)))))
    (split '() lst n)
)

(define (compose-all funcs)
    (lambda (x)
        (if (null? funcs)
            x
            ((compose-all (cdr funcs)) ((car funcs) x))))
)
