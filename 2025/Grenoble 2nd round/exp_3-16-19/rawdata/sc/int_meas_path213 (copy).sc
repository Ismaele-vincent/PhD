START	standard
CALL	Block_path13_doubleCd.sc
M	S18.auxiliary.Robot Diagonal	um	25999.900000	FALSE
F	D:\data\Cycle 198\exp_3-16-19\rawdata\sc\*.dat
R	room to enter remarks
M	S18.auxiliary.Robot Diagonal	um	26000.000000	FALSE
C	time	60.000000
M	S18.auxiliary.Robot Diagonal	um	48000.000000	FALSE
C	time	60.000000
M	S18.auxiliary.Robot Diagonal	um	70000.000000	FALSE
C	time	60.000000
E
CALL	robot_Zout_doubleCd.sc
END
