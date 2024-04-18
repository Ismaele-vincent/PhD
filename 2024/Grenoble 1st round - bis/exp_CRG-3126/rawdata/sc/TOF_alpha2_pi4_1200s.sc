G	GPIB1::8	fn1=SIN	*am1=0	*fr1=0	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0.686	*fr2=3000	ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start2
F	D:\data\Cycle 195\exp_CRG-3126\rawdata\sc\*.dat
TOF	6	time=1200	period=1000µ	binwidth=25µ	trigdiv=3
G	GPIB1::8	stop2
E