START	standard
;R	RF GF 1+2      
CALL	RobotZ.sc
CALL	nullsetzer.sc
CALL	setDC_pi_half.sc

CALL	setRF1_pi_contin_bothGF.sc
CALL	rocking.sc
CALL	setRF1_weak_contin_bothGF.sc
CALL	setRF2_weak_contin_bothGF.sc
CALL	movePS_140.sc
CALL	setRF1_weak_bothGF.sc
CALL	setRF2_weak_bothGF.sc
;********Start
F	D:\data\Cycle 190\exp_CRG-2887\rawdata\sc\TOF\RF1_weak\*.tof
TOF	4	time=7200	period=304�	binwidth=1�	delay=95�
E
CALL	setRF1_pi_contin_bothGF.sc
CALL	rocking.sc
CALL	setRF1_weak_contin_bothGF.sc
CALL	setRF2_weak_contin_bothGF.sc
CALL	movePS_145.sc
CALL	setRF1_weak_bothGF.sc
CALL	setRF2_weak_bothGF.sc
;********Start
F	D:\data\Cycle 190\exp_CRG-2887\rawdata\sc\TOF\RF1_weak\*.tof
TOF	4	time=7200	period=304�	binwidth=1�	delay=95�
E
CALL	setRF1_pi_contin_bothGF.sc
CALL	rocking.sc
CALL	setRF1_weak_contin_bothGF.sc
CALL	setRF2_weak_contin_bothGF.sc
CALL	movePS_160.sc
CALL	setRF1_weak_bothGF.sc
CALL	setRF2_weak_bothGF.sc
;********Start
F	D:\data\Cycle 190\exp_CRG-2887\rawdata\sc\TOF\RF1and2_weak\*.tof
TOF	4	time=7200	period=304�	binwidth=1�	delay=95�
E
CALL	setRF1_pi_contin_bothGF.sc
CALL	rocking.sc
CALL	setRF1_weak_contin_bothGF.sc
CALL	setRF2_weak_contin_bothGF.sc
CALL	movePS_175.sc
CALL	setRF1_weak_bothGF.sc
CALL	setRF2_weak_bothGF.sc
;********Start
F	D:\data\Cycle 190\exp_CRG-2887\rawdata\sc\TOF\RF1and2_weak\*.tof
TOF	4	time=7200	period=304�	binwidth=1�	delay=95�
E
CALL	setRF1_pi_contin_bothGF.sc
CALL	rocking.sc
CALL	setRF1_weak_contin_bothGF.sc
CALL	setRF2_weak_contin_bothGF.sc
CALL	movePS_175.sc
CALL	setRF1_weak_bothGF.sc
CALL	setRF2_weak_bothGF.sc
;********Start
F	D:\data\Cycle 190\exp_CRG-2887\rawdata\sc\TOF\RF1and2_weak\*.tof
TOF	4	time=7200	period=304�	binwidth=1�	delay=95�
E
CALL	setRF1_weak_contin_bothGF.sc
CALL	setRF2_weak_contin_bothGF.sc
CALL	movePS_175.sc

END
