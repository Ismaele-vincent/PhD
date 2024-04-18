CALL	rocking.sc
CALL	ifgPS1_3p_quick.sc

G	GPIB1::8	stop1
G	GPIB1::8	fn2=SIN	*fr2=3000	ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	start2

G	GPIB1::8	am2=10.0
T	COM3	1	21.8
CALL	ifgPS1_3p_quick.sc
CALL	rocking.sc
CALL	ifgPS1_3p_quick.sc
CALL	ifgPS1_3p_quick.sc

CALL	nullsetzer.sc