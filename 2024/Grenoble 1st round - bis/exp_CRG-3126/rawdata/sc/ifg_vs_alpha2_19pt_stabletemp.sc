G	GPIB1::8	stop1
G	GPIB1::8	stop2
G	GPIB1::8	fn2=SIN	*am2=0.0	*fr2=3000	ph2=0	of2=0	mo2=CONT	dy2=0us

T	COM3	1	23.7
;CALL	rockingR.sc

CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=0.5
G	GPIB1::8	start2
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=1.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=1.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=2.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=2.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=3.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=3.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=4.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=4.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=5.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=5.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=6.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=6.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=7.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=7.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=8.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=8.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=9.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=9.5
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am2=10.0
T	COM3	1	23.7	-0.025*am2^2
CALL	ifgPS1_2p_22pt.sc

CALL	nullsetzer.sc