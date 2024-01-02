START	standard
G	GPIB1::8	fn2=SIN	*am2=1.8	fr2=2000	ph2=0	of2=0	mo2=CONT	dy2=0us
G	GPIB1::8	fn1=SIN	*am1=0	fr1=2000	*ph1=0	of1=0	mo1=CONT	dy1=0us
G	GPIB1::8	start2

G	GPIB1::8	stop1
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E

G	GPIB1::8	start1
G	GPIB1::8	*am1=0.6
G	GPIB1::8	*ph1=0
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=60
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=120
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=180
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=240
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=300
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E

G	GPIB1::8	*am1=1.2
G	GPIB1::8	*ph1=0
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=60
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=120
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=180
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=240
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=300
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E

G	GPIB1::8	*am1=1.8
G	GPIB1::8	*ph1=0
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=60
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=120
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=180
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=240
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=300
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E

G	GPIB1::8	*am1=2.4
G	GPIB1::8	*ph1=0
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=60
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=120
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=180
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=240
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E
G	GPIB1::8	*ph1=300
F	D:\data\Cycle 194\exp_CRG-3061\rawdata\sc\*.dat
TOF	6	time=900	period=1000µ	binwidth=50µ	trigdiv=2
E


G	GPIB1::8	stop1
G	GPIB1::8	stop2



END
