START	standard
G	GPIB1::8	fn1=SIN	*am1=0	*fr1=0	*ph1=0	of1=0	mo1=CONT	dy2=0us
G	GPIB1::8	fn2=SIN	*am2=1.0	*fr2=10000	*ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start2
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
R	room to enter remarks
M	S18.axis2.phaseshifter 1	deg	-2.000000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-1.800000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-1.600000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-1.400000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-1.200000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-1.000000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-0.800000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-0.600000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-0.400000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	-0.200000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	0.000000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	0.200000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	0.400000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	0.600000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	0.800000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	1.000000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	1.200000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	1.400000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	1.600000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	1.800000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
M	S18.axis2.phaseshifter 1	deg	2.000000	FALSE
TOF	5	time=20	period=200�	binwidth=4�	delay=95�
G	GPIB1::8	stop2
E
END