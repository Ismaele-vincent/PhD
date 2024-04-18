START	standard
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=0	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0.0	*fr2=0	ph2=0	of2=0	mo2=CONT	dy2=0us
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.214287	FALSE
CALL	TOF_alpha2_Bessel_0_2kHz_900s.sc
E
END