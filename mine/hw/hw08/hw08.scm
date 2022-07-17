(define (my-filter func lst)
  (if (null? lst)
    '()
    (if (func (car lst))
      (cons (car lst) (my-filter func (cdr lst)))
      (my-filter func (cdr lst)))
))

(define (interleave s1 s2)
  (if (null? s1)
    s2
    (cons (car s1) (interleave s2 (cdr s1))))
)

(define (accumulate merger start n term)
  (if (= n 0)
    start
    (accumulate merger (merger start (term n)) (- n 1) term)))

(define (no-repeats lst)
  (if (null? lst)
      '()
      (cons (car lst)
            (no-repeats (my-filter
                         (lambda (element) (not (= element (car lst))))
                         lst)))))