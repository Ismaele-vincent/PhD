START	standard		
CALL	Move_newPS1_ph0_12.sc
CALL	ifg2_newPS_2p10s_AP.sc
MS	S18.axis2.phaseshifter 2	1	deg	FIT	O	COS-180
CALL	ifg1_newPS_2p10s_AP.sc
MS	S18.axis2.phaseshifter 1	1	deg	FIT	O	COS-270
END
