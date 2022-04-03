(define (domain pfl)
(:requirements :strips)
(:types object message - object variable - object)
(:predicates
	(sent-to-human ?m1 - message)
	(sent-to-robot ?m1 - message)
	(set ?v1 - variable)
)

(:action goto-tr-pre
	:parameters (?oi2 - variable ?w - variable)
	:precondition (and (set ?oi2) (set ?w))
	:effect (and
		(not (set ?oi2))
		(not (set ?w))
	)
)

(:action goto-tr
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?i - message)
	:precondition (and (not (set ?oi2)) (not (set ?w)))
	:effect (and
		(set ?oi1)
		(sent-to-human ?i)
	)
)

(:action goto-rrc1-pre
	:parameters (?w1 - variable ?w2 - variable)
	:precondition (and (set ?w1) (set ?w2))
	:effect (and
		(not (set ?w1))
		(not (set ?w2))
	)
)

(:action goto-rrc1
	:parameters (?oi - variable ?w1 - variable ?w2 - variable ?i - message ?iq - message)
	:precondition (and (sent-to-human ?i) (not (set ?w1)) (not (set ?w2)))
	:effect (and
		(not (sent-to-human ?i))
		(set ?oi)
		(sent-to-robot ?iq)
	)
)

(:action goto-rrc2-pre
	:parameters (?w - variable)
	:precondition (and (set ?w))
	:effect (and
		(not (set ?w))
	)
)

(:action goto-rrc2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?iq - message)
	:precondition (and (sent-to-robot ?iq) (not (set ?w)) (set ?oi1))
	:effect (and
		(not (sent-to-robot ?iq))
		(set ?oi2)
	)
)

(:action goto-cr
	:parameters (?oi1 - variable ?oi2 - variable ?b - message)
	:precondition (and (set ?oi1) (set ?oi2))
	:effect (and
		(sent-to-human ?b)
	)
)

(:action goto-cr-post
	:parameters (?b - message)
	:precondition (and (sent-to-human ?b))
	:effect (and
		(not (sent-to-human ?b))
	)
)

(:action goto-tw-pre
	:parameters (?w2 - variable)
	:precondition (and (set ?w2))
	:effect (and
		(not (set ?w2))
	)
)

(:action goto-tw
	:parameters (?w1 - variable ?w2 - variable ?s - message)
	:precondition (and (not (set ?w2)))
	:effect (and
		(set ?w1)
		(sent-to-robot ?s)
	)
)

(:action goto-rwc1
	:parameters (?w - variable ?s - message ?sq - message)
	:precondition (and (sent-to-robot ?s))
	:effect (and
		(not (sent-to-robot ?s))
		(set ?w)
		(sent-to-human ?sq)
	)
)

(:action goto-rwc2
	:parameters (?w1 - variable ?w2 - variable ?sq - message)
	:precondition (and (sent-to-human ?sq) (set ?w1))
	:effect (and
		(not (sent-to-human ?sq))
		(set ?w2)
	)
)

(:action goto-cw1
	:parameters (?w1 - variable ?w2 - variable ?b - message)
	:precondition (and (set ?w1) (set ?w2))
	:effect (and
		(sent-to-robot ?b)
	)
)

(:action goto-cw1-post
	:parameters (?b - message)
	:precondition (and (sent-to-robot ?b))
	:effect (and
		(not (sent-to-robot ?b))
	)
)

(:action goto-cw2-pre
	:parameters (?oi2 - variable)
	:precondition (and (set ?oi2))
	:effect (and
		(not (set ?oi2))
	)
)

(:action goto-cw2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable)
	:precondition (and (set ?oi1) (not (set ?oi2)) (set ?w))
	:effect (and
		(not (set ?oi1))
		(not (set ?w))
	)
))
