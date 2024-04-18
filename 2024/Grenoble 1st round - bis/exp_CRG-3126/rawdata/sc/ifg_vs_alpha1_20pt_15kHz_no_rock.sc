G	GPIB1::8	stop1
G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=15000	ph1=0	of1=0	mo1=CONT	dy1=0us

T	COM3	1	23.7
G	GPIB1::8	*am1=0.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=0.6
G	GPIB1::8	start1

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.2

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.8

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.4

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.0

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.6

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.2

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.8

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=5.4

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.6

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=7.2

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=7.8

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.4

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=9.0

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=9.6

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=10.2

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=10.8

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=11.4

CALL	ifgPS1_2p_22pt.sc

CALL	nullsetzer.sc