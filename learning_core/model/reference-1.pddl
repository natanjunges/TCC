(define (domain pfl)
(:requirements :strips)
(:types object message - object i - message s - message b - message iq - message sq - message variable - object oi1 - variable oi2 - variable oi - variable w1 - variable w2 - variable w - variable)
(:predicates
	(sent-to-human ?m1 - message)
	(sent-to-robot ?m1 - message)
	(set ?v1 - variable)
)

(:action goto-tr-pre
	:parameters (?oi2 - oi2 ?w - w)
	:precondition (and (set ?oi2) (set ?w))
	:effect (and
		(not (set ?oi2))
		(not (set ?w))
	)
)

(:action goto-tr
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?w - w ?i - i)
	:precondition (and (not (set ?oi2)) (not (set ?w)))
	:effect (and
		(set ?oi1)
		(sent-to-human ?i)
	)
)

(:action goto-rrc1-pre
	:parameters (?w1 - w1 ?w2 - w2)
	:precondition (and (set ?w1) (set ?w2))
	:effect (and
		(not (set ?w1))
		(not (set ?w2))
	)
)

(:action goto-rrc1
	:parameters (?oi - oi ?w1 - w1 ?w2 - w2 ?i - i ?iq - iq)
	:precondition (and (sent-to-human ?i) (not (set ?w1)) (not (set ?w2)))
	:effect (and
		(not (sent-to-human ?i))
		(set ?oi)
		(sent-to-robot ?iq)
	)
)

(:action goto-rrc2-pre
	:parameters (?w - w)
	:precondition (and (set ?w))
	:effect (and
		(not (set ?w))
	)
)

(:action goto-rrc2
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?w - w ?iq - iq)
	:precondition (and (sent-to-robot ?iq) (not (set ?w)) (set ?oi1))
	:effect (and
		(not (sent-to-robot ?iq))
		(set ?oi2)
	)
)

(:action goto-cr
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?b - b)
	:precondition (and (set ?oi1) (set ?oi2))
	:effect (and
		(sent-to-human ?b)
	)
)

(:action goto-cr-post
	:parameters (?b - b)
	:precondition (and (sent-to-human ?b))
	:effect (and
		(not (sent-to-human ?b))
	)
)

(:action goto-tw-pre
	:parameters (?w2 - w2)
	:precondition (and (set ?w2))
	:effect (and
		(not (set ?w2))
	)
)

(:action goto-tw
	:parameters (?w1 - w1 ?w2 - w2 ?s - s)
	:precondition (and (not (set ?w2)))
	:effect (and
		(set ?w1)
		(sent-to-robot ?s)
	)
)

(:action goto-rwc1
	:parameters (?w - w ?s - s ?sq - sq)
	:precondition (and (sent-to-robot ?s))
	:effect (and
		(not (sent-to-robot ?s))
		(set ?w)
		(sent-to-human ?sq)
	)
)

(:action goto-rwc2
	:parameters (?w1 - w1 ?w2 - w2 ?sq - sq)
	:precondition (and (sent-to-human ?sq) (set ?w1))
	:effect (and
		(not (sent-to-human ?sq))
		(set ?w2)
	)
)

(:action goto-cw1
	:parameters (?w1 - w1 ?w2 - w2 ?b - b)
	:precondition (and (set ?w1) (set ?w2))
	:effect (and
		(sent-to-robot ?b)
	)
)

(:action goto-cw1-post
	:parameters (?b - b)
	:precondition (and (sent-to-robot ?b))
	:effect (and
		(not (sent-to-robot ?b))
	)
)

(:action goto-cw2-pre
	:parameters (?oi2 - oi2)
	:precondition (and (set ?oi2))
	:effect (and
		(not (set ?oi2))
	)
)

(:action goto-cw2
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?w - w)
	:precondition (and (set ?oi1) (not (set ?oi2)) (set ?w))
	:effect (and
		(not (set ?oi1))
		(not (set ?w))
	)
))