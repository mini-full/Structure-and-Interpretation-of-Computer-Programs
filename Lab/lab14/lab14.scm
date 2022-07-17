(define (split-at lst n)
  (define (split lst-so-far rest i)
    (cond 
      ((null? rest)
       (cons lst-so-far nil))
      ((= i 0)
       (cons lst-so-far rest))
      ((null? lst-so-far)
       (split (list (car rest)) (cdr rest) (- i 1)))
      (else
       (split (append lst-so-far (list (car rest)))
              (cdr rest)
              (- i 1)))))
  (split '() lst n))

(define (compose-all funcs)
  (if (null? funcs)
      (lambda (x) x)
      (lambda (x)
        ((compose-all (cdr funcs)) ((car funcs) x)))))

(define (compose-all funcs)
  (lambda (x)
    (if (null? funcs)
        x
        ((compose-all (cdr funcs)) ((car funcs) x)))))
