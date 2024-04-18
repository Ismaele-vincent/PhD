G	GPIB1::8	fn1=SIN	*am1=1.4	*fr1=2000	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0	*fr2=0	ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start1
F	D:\data\Cycle 195\exp_CRG-3125\rawdata\sc\*.dat
TOF	6	time=600	period=1000µ	binwidth=25µ	trigdiv=2
G	GPIB1::8	stop1
E