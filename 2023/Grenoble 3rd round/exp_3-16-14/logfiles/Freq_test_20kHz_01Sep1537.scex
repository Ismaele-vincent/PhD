G	GPIB1::8	fn1=SIN	*am1=3.1	*fr1=20000	*ph1=0	of1=0	bt1=3
G	GPIB1::8	mo1=CONT
G	GPIB1::8	start1
CALL	movePS_90.sc
G	GPIB1::8	stop1
G	GPIB1::8	mo1=BURS
G	GPIB1::8	start1
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
TOF	4	time=600	period=154µ	binwidth=1µ	delay=5µ
G	GPIB1::8	stop1
E