G	GPIB1::8	fn1=SIN	*am1=0.74	*fr1=10000	*ph1=0	of1=0	bt1=4	dy1=29.43us
G	GPIB1::8	fn2=SIN	*am2=0.61	*fr2=15000	*ph2=0	of2=0	bt2=6 	dy2=0us
G	GPIB1::8	start1
G	GPIB1::8	start2
F	D:\data\Cycle 192ter\exp_3-16-14\rawdata\sc\*.dat
TOF	4	time=1500	period=434�	binwidth=3�	delay=95�
G	GPIB1::8	stop1
G	GPIB1::8	stop2
E