(define (over-or-under num1 num2)
  (if (< num1 num2)
      -1
      (if (= num1 num2)
          0
          1)))

(define (over-or-under num1 num2)
  (cond 
    ((< num1 num2) -1)
    ((= num1 num2) 0)
    (else          1)))

(define (make-adder num) (lambda (x) (+ x num)))

(define (composed f g) (lambda (x) (f (g x))))

(define lst
        (let ((t (list 1))
              (l (list 3 4)))
          (list t 2 l 5)))

(define lst
        (let ((t (cons 1 nil))
              (l (cons 3 (cons 4 nil))))
          (cons t (cons 2 (cons l (cons 5 nil))))))

(define (remove item lst)
  (filter (lambda (x) (not (equal? x item))) lst))
