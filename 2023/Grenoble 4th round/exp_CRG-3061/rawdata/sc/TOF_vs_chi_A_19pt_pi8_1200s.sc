START	standard
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=0	*ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0.0	*fr2=0	*ph2=0	of2=0	mo2=CONT	dy2=0us
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.500000
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.333333
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.166666
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.999999
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.833332
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.666665
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.499998
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.333331
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.166664
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.000003
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.166670
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.333337
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.500004
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.666671
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.833338
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.000005
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.166672
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.333339
CALL	TOF_A_pi8_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.500006
CALL	TOF_A_pi8_1200s.sc
E
END