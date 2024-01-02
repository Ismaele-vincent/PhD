G	GPIB1::8	fn1=SIN	*am1=0	*fr1=0	*ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=2.05	*fr2=10000	*ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start2
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
TOF	6	time=1500	period=200µ	binwidth=4µ	delay=95µ	trigdiv=2
G	GPIB1::8	stop2
E