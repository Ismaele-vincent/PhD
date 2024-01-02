G	GPIB1::8	fn1=SIN	*am1=4.7	*fr1=10000	*ph1=0	of1=0	bt1=3
G	GPIB1::8	mo1=CONT
G	GPIB1::8	start1
CALL	movePS_90.sc
G	GPIB1::8	mo1=BURS
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
TOF	4	time=600	period=304µ	binwidth=1µ	delay=5µ
G	GPIB1::8	stop1
E