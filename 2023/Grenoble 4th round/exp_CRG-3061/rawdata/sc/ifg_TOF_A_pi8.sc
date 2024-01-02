START	standard
G	GPIB1::8	fn1=SIN	*am1=4.12	*fr1=2000	*ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0	*fr2=0	*ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start1
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
R	room to enter remarks
M	S18.axis2.phaseshifter 1	deg	0.000000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	0.200000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	0.400000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	0.600000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	0.800000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	1.000000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	1.200000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	1.400000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	1.600000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	1.800000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	2.000000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	2.200000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	2.400000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	2.600000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	2.800000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	3.000000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	3.200000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	3.400000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	3.600000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	3.800000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
M	S18.axis2.phaseshifter 1	deg	4.000000	FALSE
TOF	7	time=20	period=1000µ	binwidth=50µ
G	GPIB1::8	stop1
E
END