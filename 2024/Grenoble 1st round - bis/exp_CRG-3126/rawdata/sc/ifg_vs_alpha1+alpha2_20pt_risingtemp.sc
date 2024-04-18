G	GPIB1::8	stop1
G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*am1=0.0	*fr1=2000	ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	fn2=SIN	*am2=0.0	*fr2=3000	ph2=0	of2=0	mo2=CONT	dy2=0us

T	COM3	1	23.7

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=0.5
G	GPIB1::8	start1
G	GPIB1::8	start2
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=1.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=1.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=0.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=1.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=2.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=2.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=1.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=0.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=3.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=2.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=1.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=3.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=2.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=1.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=0.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc
G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=4.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=3.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=2.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=1.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=4.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=3.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc


G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=2.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=1.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=2.0
G	GPIB1::8	*am2=5.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=4.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=2.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=3.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=4.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=3.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=2.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=4.0
G	GPIB1::8	*am2=5.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=4.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=3.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=4.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=3.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=6.0
G	GPIB1::8	*am2=5.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=4.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=4.5
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

G	GPIB1::8	*am1=8.0
G	GPIB1::8	*am2=5.0
CALL	rockingR.sc
CALL	ifgPS1_2p_22pt.sc

CALL	nullsetzer.sc