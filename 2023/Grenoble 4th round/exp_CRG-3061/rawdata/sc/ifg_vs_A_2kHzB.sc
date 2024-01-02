G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*ph1=0	of1=0	mo1=CONT	fr1=2000
G	GPIB1::8	fn2=SIN	*ph2=0	of2=0	mo2=CONT	fr2=2000

G	GPIB1::8	start2
G	GPIB1::8	*am1=0.0
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=0.556
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=1.113
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=1.668
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=2.224
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=2.781
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=3.337
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=3.892
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=4.45
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=5.005
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=5.561
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=6.118
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=6.674
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=7.229
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=7.786
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=8.342
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=8.898
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=9.455
CALL	ifg_-2to2_15s.sc
G	GPIB1::8	*am1=10.0
CALL	ifg_-2to2_15s.sc

