G	GPIB1::8	fn1=SIN	*am1=4.12	*fr1=2000	*ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=4.127	*fr2=3000	*ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start1
G	GPIB1::8	start2
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1500	period=200�	binwidth=4�	delay=95�	trigdiv=2
G	GPIB1::8	stop1
G	GPIB1::8	stop2
E