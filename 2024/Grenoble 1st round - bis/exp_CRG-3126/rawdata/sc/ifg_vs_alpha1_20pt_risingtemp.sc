G	GPIB1::8	stop1
G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=3000	ph1=0	of1=0	mo1=CONT	dy1=0us

T	COM3	1	23.7
G	GPIB1::8	*am1=0.0
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=0.4
G	GPIB1::8	start1
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=0.8
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.2
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=1.6
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.4
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.8
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.2
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=3.6
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.4
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.8
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=5.2
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=5.6
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.4
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.8
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=7.2
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=7.6
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

CALL	nullsetzer.sc