G	GPIB1::8	fn1=SIN	*am1=1.112	*fr1=3000	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0	*fr2=0	ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start1
F	D:\data\Cycle 195\exp_CRG-3126\rawdata\sc\*.dat
TOF	6	time=1200	period=1000�	binwidth=25�	trigdiv=3
G	GPIB1::8	stop1
E