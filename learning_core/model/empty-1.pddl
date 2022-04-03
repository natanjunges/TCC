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
	:precondition (and )
	:effect (and 
	)
)

(:action goto-tr
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?i - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rrc1-pre
	:parameters (?w1 - variable ?w2 - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rrc1
	:parameters (?oi - variable ?w1 - variable ?w2 - variable ?i - message ?iq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rrc2-pre
	:parameters (?w - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rrc2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable ?iq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cr
	:parameters (?oi1 - variable ?oi2 - variable ?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cr-post
	:parameters (?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-tw-pre
	:parameters (?w2 - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-tw
	:parameters (?w1 - variable ?w2 - variable ?s - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rwc1
	:parameters (?w - variable ?s - message ?sq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-rwc2
	:parameters (?w1 - variable ?w2 - variable ?sq - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cw1
	:parameters (?w1 - variable ?w2 - variable ?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cw1-post
	:parameters (?b - message)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cw2-pre
	:parameters (?oi2 - variable)
	:precondition (and )
	:effect (and 
	)
)

(:action goto-cw2
	:parameters (?oi1 - variable ?oi2 - variable ?w - variable)
	:precondition (and )
	:effect (and 
	)
))