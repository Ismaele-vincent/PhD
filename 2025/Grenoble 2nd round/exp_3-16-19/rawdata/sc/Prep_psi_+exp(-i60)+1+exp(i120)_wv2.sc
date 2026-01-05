START	standard		
CALL	robot_Zout_doubleCd.sc
CALL	Move_PS12_parallel.sc
CALL	ifg1_newPS_2p5s_wv2.sc
MS	S18.axis2.phaseshifter 1	1	deg	FIT	AUX	COS-180
CALL	ifg2_newPS_2p10s_wv2.sc
MS	S18.axis2.phaseshifter 2	1	deg	FIT	O	COS-60
CALL	ifg1_newPS_2p5s_wv2.sc
MS	S18.axis2.phaseshifter 1	1	deg	FIT	AUX	COS-60
END
