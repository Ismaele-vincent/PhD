START	standard		
CALL	robot_Zout_singleCd.sc
MS	S18.auxiliary.Robot rot big	1	deg	absolute	30.00000
MS	S18.auxiliary.Robot Diagonal	1	um	absolute	28000.00000
CALL	robot_Zin_singleCd.sc
M	S18.auxiliary.Robot Diagonal	um	27999.900000	FALSE
F	D:\data\Cycle 198\exp_3-16-19\rawdata\sc\*.dat
R	room to enter remarks
M	S18.auxiliary.Robot Diagonal	um	28000.000000	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	30820.512821	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	33641.025642	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	36461.538463	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	39282.051284	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	42102.564105	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	44923.076926	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	47743.589747	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	50564.102568	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	53384.615389	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	56205.128210	FALSE
C	time	2.000000
E
END
