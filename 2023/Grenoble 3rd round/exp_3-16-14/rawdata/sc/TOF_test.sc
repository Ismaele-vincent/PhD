G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=10000	*ph1=0	of1=0	bt1=3
G	GPIB1::8	fn2=SIN	*am2=2.0	*fr2=10000	*ph2=0	of2=0	bt2=3
G	GPIB1::8	start1
G	GPIB1::8	start2
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
TOF	4	time=1200	period=301µ	binwidth=3µ	delay=95µ
G	GPIB1::8	stop1
G	GPIB1::8	stop2
E