START	standard
G	GPIB1::8	fn2=SIN	*am2=1.715	fr2=2000	ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start2
G	GPIB1::8	fn1=SIN	*am1=1.143	fr1=2000	*ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	stop1

G	GPIB1::8	*ph1=0
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1200	period=1000µ	binwidth=50µ	trigdiv=2
E

G	GPIB1::8	stop1
G	GPIB1::8	stop2



END
