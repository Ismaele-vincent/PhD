G	GPIB1::8	stop1
G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=2000	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0.0	*fr2=3000	ph2=0	of2=0	mo2=CONT	dy2=0us

T	COM3	1	23.7
G	GPIB1::8	*am1=0.0
G	GPIB1::8	*am2=0.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=0.3
G	GPIB1::8	*am2=0.6
G	GPIB1::8	start1
G	GPIB1::8	start2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=0.6
G	GPIB1::8	*am2=1.2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=0.9
G	GPIB1::8	*am2=1.8
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.2
G	GPIB1::8	*am2=2.4
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.5
G	GPIB1::8	*am2=3.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.8
G	GPIB1::8	*am2=3.6
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.1
G	GPIB1::8	*am2=4.2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.4
G	GPIB1::8	*am2=4.8
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.7
G	GPIB1::8	*am2=5.4
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.0
G	GPIB1::8	*am2=6.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.3
G	GPIB1::8	*am2=6.6
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.6
G	GPIB1::8	*am2=7.2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.9
G	GPIB1::8	*am2=7.8
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.2
G	GPIB1::8	*am2=8.4
CALL	ifgPS1_2p_22pt.sc

CALL	nullsetzer.sc