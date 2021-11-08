;;; SI413 Lab 03
;;; EVERETT STENBERG 

;;; EXERCISE 1 - min-sin
(define (min-sin x . vars)
  (let ((L (append (list x) vars)))
    (get-index L (get-min(map sin L)))
    )
  )
    

;;; EXERCISE 2 - group 
(define (group k vars)
  (group-helper '() vars k 0)
  )


;;; EXERCISE 3 - power 
(define (power n)
  (lambda (x)
    (expt x n)
    )
  )

;;; EXERCISE 4 - make-cXr
(define (make-cXr x . args)
  (lambda (argument) 
    (map (lambda (function) (function argument)) (build-list (list x args)))
    )
  ) 
 



;;; EXERCISE 5 - make-stack
(define (make-stack)
  (let ((stack '()))
    (lambda (d1)
      (cond [(eqv? d1 'size) (length stack)]
	    [(eqv? d1 'pop) (begin (display (car stack)) (car stack) (set! stack (cdr stack)))]
	    [(eqv? d1 'push) (set! stack (append d2 stack))]
	    ))))
(define (make-set)
  (let ((set '()))
    (lambda (d1 . d2)
      (cond [(eqv? d1 'get) set]
	    [(eqv? d1 'set!) (apply (lambda (x) (append (list x) set)) d2) ]
	    [(eqv? d1 'size) (length set)]
	    [(eqv? d1 'insert!) (set! set (add-all-items d2 set))]
	    ))))
(define (add-all-items L set)
  (if (null? L)
      set 
      (add-all-items (cdr L) (add-to-list (car L) '() set))))
(define (add-to-list item before after)
  (if (null? after)
      (append before (list item) )
      (cond [(> (car after) item) (append before (list item) after)]
	    [else (add-to-list item (append before (list (car after))) (cdr after))]
	    )))
;;; HELPER FUNCTIONS
;;; EXERCISE 1
(define (get-min L)
     (get-min-helper L 100 0 0) ;;; <- works for our purposes here
     )
(define (get-min-helper L min_val i_min i_cur)
  (if (null? L )
      i_min
      (if (< (car L) min_val)
   (get-min-helper (cdr L) (car L) i_cur (+ i_cur 1))
   (get-min-helper (cdr L) min_val i_min (+ i_cur 1))
   )))
; indexing starts at 0
(define (get-index L i)
  (get-index-helper L i 0)
  )
(define (get-index-helper L i n)
  (if (= n i)
      (car L)
      (get-index-helper (cdr L) i (+ n 1))
      ))


;;;EXERCISE 2 
(define (group-helper L_building L_taking k generation)
  (if (<= (length L_taking) (* generation k))
      L_building
      (cons (add-k '() L_taking k 0 generation) (group-helper L_building L_taking k (+ generation 1)))
      )
  )

(define (add-k L_building L_taking k i gen)
  (if (or (= i k) (<= (length L_taking) (+ i (* gen k))))
      L_building
      (cons (get-index L_taking (+ i (* gen k))) (add-k L_building L_taking k (+ i 1) gen))
  )
  )
;;; EXERCISE 4  
(define (get-func x)
  (cond [(eqv? x 'a) car]
  	[(eqv? x 'd) cdr]
	)
  )
(define (build-list L)
  (if (null? L)
      '()
      (cons (get-func (car L)) (build-list (cdr L)) )))
