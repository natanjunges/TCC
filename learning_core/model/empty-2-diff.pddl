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
	:precondition (and )
	:effect (and 
	)
)

(:action goto-tir
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?i - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rirc1-pre
	:parameters (?w1 - variable ?w2 - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rirc1
	:parameters (?oi - variable ?w1 - variable ?w2 - variable ?i - message ?iq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rirc2-pre
	:parameters (?w - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rirc2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?iq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cir
	:parameters (?oi1 - variable ?oi2 - variable ?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cir-post
	:parameters (?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ric1
	:parameters (?w - variable ?s - message ?sq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ric2-pre
	:parameters (?w1 - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ric2
	:parameters (?oi - variable ?w1 - variable ?w2 - variable ?sq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ci1
	:parameters (?oi - variable ?w2 - variable ?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ci1-post
	:parameters (?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ci2-pre
	:parameters (?oi2 - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-ci2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable)
	:precondition (and )
	:effect (and 
	)
))