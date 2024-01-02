G	GPIB1::8	stop2
G	GPIB1::8	stop1
G	GPIB1::8	fn1=SIN	*ph1=0	of1=0	mo1=CONT	fr1=3000
G	GPIB1::8	fn2=SIN	*ph2=0	of2=0	mo2=CONT	fr2=3000

G	GPIB1::8	*am2=0.0
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	start2
G	GPIB1::8	*am2=1
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=2
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=3
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=4
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=4.65
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=5
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=5.35
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=5.7
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=6
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=7
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=8
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=9
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am2=10
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	stop2
G	GPIB1::8	stop1
