START	standard
;CALL	rocking.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS0
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS30
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS60
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS90
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS120
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS150
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
CALL	ifg_10s_3p.sc
MS	S18.axis2.phase shifter	1	deg	FIT	H	COS180
CALL	betaS1pi8.sc
MS	S18.auxiliary.LinearBlue	1	mm	FIT	O	COS0
CALL	DC2Y.sc

CALL	setDCpi2.sc
CALL	setDC2pos.sc
END
