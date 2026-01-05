START	standard		
CALL	robot_Zout_doubleCd.sc
MS	S18.auxiliary.Robot rot big	1	deg	absolute	120.00000
MS	S18.auxiliary.Robot Diagonal	1	um	absolute	10000.00000
CALL	robot_Zin_doubleCd.sc
M	S18.auxiliary.Robot Diagonal	um	9999.900000	FALSE
F	D:\data\Cycle 198\exp_3-16-19\rawdata\sc\*.dat
R	room to enter remarks
M	S18.auxiliary.Robot Diagonal	um	10000.000000	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	13684.210526	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	17368.421052	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	21052.631578	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	24736.842104	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	28421.052630	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	32105.263156	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	35789.473682	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	39473.684208	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	43157.894734	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	46842.105260	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	50526.315786	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	54210.526312	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	57894.736838	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	61578.947364	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	65263.157890	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	68947.368416	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	72631.578942	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	76315.789468	FALSE
C	time	5.000000
M	S18.auxiliary.Robot Diagonal	um	79999.999994	FALSE
C	time	5.000000
E
END
