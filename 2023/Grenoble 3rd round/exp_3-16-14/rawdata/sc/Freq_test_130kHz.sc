G	GPIB1::8	fn1=SIN	*am1=10	*fr1=130000	*ph1=0	of1=0	bt1=7
G	GPIB1::8	start1
CALL	movePS_90.sc
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
TOF	4	time=600	period=58�	binwidth=1�	delay=5�
G	GPIB1::8	stop1
E