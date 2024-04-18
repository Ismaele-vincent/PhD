START	standard
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=0	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0.0	*fr2=0	ph2=0	of2=0	mo2=CONT	dy2=0us
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.500000	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.357143	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.214286	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-1.071429	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.928572	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.785715	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.642858	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.500001	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.357144	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.214287	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	-0.071430	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.071427	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.214284	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.357141	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.499998	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.642855	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.785712	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	0.928569	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.071426	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.214283	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.357140	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
MS	S18.axis2.phaseshifter 1	1	deg	absolute	1.499997	FALSE
CALL	TOF_alpha1_Bessel_0_2kHz_1200s.sc
E
END
