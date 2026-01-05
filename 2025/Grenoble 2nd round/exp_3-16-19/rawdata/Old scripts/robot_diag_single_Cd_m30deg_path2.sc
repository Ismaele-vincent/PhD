START	standard		
CALL	robot_Zout_singleCd.sc
MS	S18.auxiliary.Robot rot big	1	deg	absolute	-30.00000
MS	S18.auxiliary.Robot Diagonal	1	um	absolute	-30000.00000
CALL	robot_Zin_singleCd.sc
M	S18.auxiliary.Robot Diagonal	um	-30000.100000	FALSE
F	D:\data\Cycle 198\exp_3-16-19\rawdata\sc\*.dat
R	room to enter remarks
M	S18.auxiliary.Robot Diagonal	um	-30000.000000	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-27179.487179	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-24358.974358	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-21538.461537	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-18717.948716	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-15897.435895	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-13076.923074	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-10256.410253	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-7435.897432	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-4615.384611	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	-1794.871790	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	1025.641031	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	3846.153852	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	6666.666673	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	9487.179494	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	12307.692315	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	15128.205136	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	17948.717957	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	20769.230778	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	23589.743599	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	26410.256420	FALSE
C	time	2.000000
M	S18.auxiliary.Robot Diagonal	um	29230.769241	FALSE
C	time	2.000000
E
END
