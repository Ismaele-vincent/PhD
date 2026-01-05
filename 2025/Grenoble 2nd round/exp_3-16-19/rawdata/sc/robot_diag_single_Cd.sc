START	standard		
CALL	robot_Zout_singleCd.sc
MS	S18.auxiliary.Robot rot big	1	deg	absolute	0.00000
MS	S18.auxiliary.Robot Diagonal	1	um	absolute	-55000.00000
CALL	robot_Zin_singleCd.sc
M	S18.auxiliary.Robot Diagonal	um	-55000.100000	FALSE
F	D:\data\Cycle 198\exp_3-16-19\rawdata\sc\*.dat
R	room to enter remarks
M	S18.auxiliary.Robot Diagonal	um	-55000.000000	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	0.000000	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	55000.000000	FALSE
C	time	2.000000
E
END
