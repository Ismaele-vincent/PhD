G	GPIB1::8	stop1
G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*am2=0.0	*fr2=2000	ph2=0	of2=0	mo2=CONT	dy2=0us

T	COM3	1	23.7
G	GPIB1::8	*am2=0.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=1.0
G	GPIB1::8	start2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=2.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=3.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=4.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=5.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=6.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=7.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=8.0
CALL	ifgPS1_2p_22pt.sc

CALL	nullsetzer.sc