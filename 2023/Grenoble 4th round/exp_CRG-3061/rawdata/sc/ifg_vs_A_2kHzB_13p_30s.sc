G	GPIB1::8	stop2
G	GPIB1::8	stop1
G	GPIB1::8	fn1=SIN	*ph1=0	of1=0	mo1=CONT	fr1=2000
G	GPIB1::8	fn2=SIN	*ph2=0	of2=0	mo2=CONT	fr2=2000

G	GPIB1::8	*am1=0.0
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	start1
G	GPIB1::8	*am1=1
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=2
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=3
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=4
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=4.65
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=5
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=5.35
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=5.7
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=6
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=7
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=8
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=9
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	*am1=10
CALL	ifg_-2to2_30s.sc
G	GPIB1::8	stop2
G	GPIB1::8	stop1
