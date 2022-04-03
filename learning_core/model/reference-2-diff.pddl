(define (domain pfl)
(:requirements :strips)
(:types object message - object variable - object)
(:predicates
	(sent-to-human ?m1 - message)
	(sent-to-robot ?m1 - message)
	(set ?v1 - variable)
)

(:action goto-tir-pre
	:parameters (?oi2 - variable ?w - variable)
	:precondition (and (set ?oi2) (set ?w))
	:effect (and
		(not (set ?oi2))
		(not (set ?w))
	)
)

(:action goto-tir
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?i - message)
	:precondition (and (not (set ?oi2)) (not (set ?w)))
	:effect (and
		(set ?oi1)
		(sent-to-human ?i)
	)
)

(:action goto-rirc1-pre
	:parameters (?w1 - variable ?w2 - variable)
	:precondition (and (set ?w1) (set ?w2))
	:effect (and
		(not (set ?w1))
		(not (set ?w2))
	)
)

(:action goto-rirc1
	:parameters (?oi - variable ?w1 - variable ?w2 - variable ?i - message ?iq - message)
	:precondition (and (sent-to-human ?i) (not (set ?w1)) (not (set ?w2)))
	:effect (and
		(not (sent-to-human ?i))
		(set ?oi)
		(sent-to-robot ?iq)
	)
)

(:action goto-rirc2-pre
	:parameters (?w - variable)
	:precondition (and (set ?w))
	:effect (and
		(not (set ?w))
	)
)

(:action goto-rirc2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?iq - message)
	:precondition (and (sent-to-robot ?iq) (not (set ?w)) (set ?oi1))
	:effect (and
		(not (sent-to-robot ?iq))
		(set ?oi2)
	)
)

(:action goto-cir
	:parameters (?oi1 - variable ?oi2 - variable ?b - message)
	:precondition (and (set ?oi1) (set ?oi2))
	:effect (and
		(sent-to-human ?b)
	)
)

(:action goto-cir-post
	:parameters (?b - message)
	:precondition (and (sent-to-human ?b))
	:effect (and
		(not (sent-to-human ?b))
	)
)

(:action goto-ric1
	:parameters (?w - variable ?s - message ?sq - message)
	:precondition (and )
	:effect (and
		(set ?w)
		(sent-to-human ?sq)
	)
)

(:action goto-ric2-pre
	:parameters (?w1 - variable)
	:precondition (and (set ?w1))
	:effect (and
		(not (set ?w1))
	)
)

(:action goto-ric2
	:parameters (?oi - variable ?w1 - variable ?w2 - variable ?sq - message)
	:precondition (and (sent-to-human ?sq) (set ?oi) (not (set ?w1)))
	:effect (and
		(not (sent-to-human ?sq))
		(set ?w2)
	)
)

(:action goto-ci1
	:parameters (?oi - variable ?w2 - variable ?b - message)
	:precondition (and (set ?oi) (set ?w2))
	:effect (and
		(sent-to-robot ?b)
	)
)

(:action goto-ci1-post
	:parameters (?b - message)
	:precondition (and (sent-to-robot ?b))
	:effect (and
		(not (sent-to-robot ?b))
	)
)

(:action goto-ci2-pre
	:parameters (?oi2 - variable)
	:precondition (and (set ?oi2))
	:effect (and
		(not (set ?oi2))
	)
)

(:action goto-ci2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable)
	:precondition (and (set ?oi1) (not (set ?oi2)) (set ?w))
	:effect (and
		(not (set ?oi1))
		(not (set ?w))
	)
))
