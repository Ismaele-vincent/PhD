G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*ph1=0	of1=0	mo1=CONT	fr1=4000

G	GPIB1::8	*am1=6.0
G	GPIB1::8	start1
CALL	movePS_90_quick.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=600	period=500µ	binwidth=10µ	trigdiv=2
G	GPIB1::8	stop1
E

