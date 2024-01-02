G	GPIB1::8	fn1=SIN	*am1=2.5	*fr1=80000	*ph1=0	of1=0	mo1=CONT
G	GPIB1::8	start1
CALL	movePS_90.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=600	period=25µ	binwidth=1µ	trigdiv=2
G	GPIB1::8	stop1
