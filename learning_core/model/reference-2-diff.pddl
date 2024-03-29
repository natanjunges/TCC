
(:action goto-tir-pre
	:parameters (?oi2 - oi2 ?w - w)
	:precondition (and (set ?oi2) (set ?w))
	:effect (and
		(not (set ?oi2))
		(not (set ?w))
	)
)

(:action goto-tir
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?w - w ?i - i)
	:precondition (and (not (set ?oi2)) (not (set ?w)))
	:effect (and
		(set ?oi1)
		(sent-to-human ?i)
	)
)

(:action goto-rirc1-pre
	:parameters (?w1 - w1 ?w2 - w2)
	:precondition (and (set ?w1) (set ?w2))
	:effect (and
		(not (set ?w1))
		(not (set ?w2))
	)
)

(:action goto-rirc1
	:parameters (?oi - oi ?w1 - w1 ?w2 - w2 ?i - i ?iq - iq)
	:precondition (and (sent-to-human ?i) (not (set ?w1)) (not (set ?w2)))
	:effect (and
		(not (sent-to-human ?i))
		(set ?oi)
		(sent-to-robot ?iq)
	)
)

(:action goto-rirc2-pre
	:parameters (?w - w)
	:precondition (and (set ?w))
	:effect (and
		(not (set ?w))
	)
)

(:action goto-rirc2
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?w - w ?iq - iq)
	:precondition (and (sent-to-robot ?iq) (not (set ?w)) (set ?oi1))
	:effect (and
		(not (sent-to-robot ?iq))
		(set ?oi2)
	)
)

(:action goto-cir
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?b - b)
	:precondition (and (set ?oi1) (set ?oi2))
	:effect (and
		(sent-to-human ?b)
	)
)

(:action goto-cir-post
	:parameters (?b - b)
	:precondition (and (sent-to-human ?b))
	:effect (and
		(not (sent-to-human ?b))
	)
)

(:action goto-ric1
	:parameters (?w - w ?s - s ?sq - sq)
	:precondition (and )
	:effect (and
		(set ?w)
		(sent-to-human ?sq)
	)
)

(:action goto-ric2-pre
	:parameters (?w1 - w1)
	:precondition (and (set ?w1))
	:effect (and
		(not (set ?w1))
	)
)

(:action goto-ric2
	:parameters (?oi - oi ?w1 - w1 ?w2 - w2 ?sq - sq)
	:precondition (and (sent-to-human ?sq) (set ?oi) (not (set ?w1)))
	:effect (and
		(not (sent-to-human ?sq))
		(set ?w2)
	)
)

(:action goto-ci1
	:parameters (?oi - oi ?w2 - w2 ?b - b)
	:precondition (and (set ?oi) (set ?w2))
	:effect (and
		(sent-to-robot ?b)
	)
)

(:action goto-ci1-post
	:parameters (?b - b)
	:precondition (and (sent-to-robot ?b))
	:effect (and
		(not (sent-to-robot ?b))
	)
)

(:action goto-ci2-pre
	:parameters (?oi2 - oi2)
	:precondition (and (set ?oi2))
	:effect (and
		(not (set ?oi2))
	)
)

(:action goto-ci2
	:parameters (?oi1 - oi1 ?oi2 - oi2 ?w - w)
	:precondition (and (set ?oi1) (not (set ?oi2)) (set ?w))
	:effect (and
		(not (set ?oi1))
		(not (set ?w))
	)
))