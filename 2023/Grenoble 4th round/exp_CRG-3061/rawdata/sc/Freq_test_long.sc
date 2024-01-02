G	GPIB1::8	stop2
G	GPIB1::8	fn1=SIN	*ph1=0	of1=0	mo1=CONT

G	GPIB1::8	*fr1=10000	*am1=2.1
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=200µ	binwidth=8µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=15000	*am1=2.0
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=133.333µ	binwidth=5.333µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=20000	*am1=1.6
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=100µ	binwidth=4µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=25000	*am1=1.0
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=80µ	binwidth=3.2µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=30000	*am1=0.8
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=66.666µ	binwidth=2.666µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=35000	*am1=1.55
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=57.143µ	binwidth=2.286µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=36000	*am1=1.75
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=55.556µ	binwidth=2.222µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=37000	*am1=2
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=54.054µ	binwidth=2.162µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=38000	*am1=2.25
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=52.632µ	binwidth=2.105µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=39000	*am1=2.5
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=51.282µ	binwidth=2.051µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=40000	*am1=2.8
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=50µ	binwidth=2µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=41000	*am1=3.05
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=48.78µ	binwidth=1.951µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=42000	*am1=3.4
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=47.619µ	binwidth=1.905µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=43000	*am1=3.6
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=46.512µ	binwidth=1.860µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=44000	*am1=3.95
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=45.455µ	binwidth=1.818µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=45000	*am1=4.25
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=44.444µ	binwidth=1.778µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=50000	*am1=6
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=40µ	binwidth=1.6µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=55000	*am1=7.8
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=36.364µ	binwidth=1.455µ	trigdiv=2
G	GPIB1::8	stop1
E

G	GPIB1::8	*fr1=60000	*am1=9.8
G	GPIB1::8	start1
CALL	movePS_90_long.sc
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=1800	period=33.333µ	binwidth=1.333µ	trigdiv=2
G	GPIB1::8	stop1
E