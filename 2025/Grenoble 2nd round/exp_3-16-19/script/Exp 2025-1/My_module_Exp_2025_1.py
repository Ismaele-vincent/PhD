import numpy as np

"""
Weak values for mixed states
"""
def w1(a_1, a_2, a_3, chi_1, chi_1_0, chi_2, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23):
    Dchi_12=chi_1_0+chi_1-(chi_2_0+chi_2)
    Dchi_13=chi_1_0+chi_1-(chi_3_0+chi_3)
    Dchi_23=chi_2_0+chi_2-(chi_3_0+chi_3)
    A=a_1**2+C_12*a_1*a_2*np.exp(-1j*Dchi_12)+C_13*a_1*a_3*np.exp(-1j*Dchi_13)
    B=1+2*C_12*a_1*a_2*np.cos(Dchi_12)+2*C_13*a_1*a_3*np.cos(Dchi_13)+2*C_23*a_2*a_3*np.cos(Dchi_23)
    return A/B

def w2(a_1, a_2, a_3,chi_1, chi_1_0, chi_2, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23):
    Dchi_12=chi_1_0+chi_1-(chi_2_0+chi_2)
    Dchi_13=chi_1_0+chi_1-(chi_3_0+chi_3)
    Dchi_23=chi_2_0+chi_2-(chi_3_0+chi_3)
    A=C_12*a_1*a_2*np.exp(1j*Dchi_12)+a_2**2+C_23*a_2*a_3*np.exp(-1j*Dchi_23)
    B=1+2*C_12*a_1*a_2*np.cos(Dchi_12)+2*C_13*a_1*a_3*np.cos(Dchi_13)+2*C_23*a_2*a_3*np.cos(Dchi_23)
    return A/B

def w3(a_1, a_2, a_3, chi_1, chi_1_0, chi_2, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23):
    Dchi_12=chi_1_0+chi_1-(chi_2_0+chi_2)
    Dchi_13=chi_1_0+chi_1-(chi_3_0+chi_3)
    Dchi_23=chi_2_0+chi_2-(chi_3_0+chi_3)
    A=C_12*a_1*a_3*np.exp(1j*Dchi_13)+C_23*a_2*a_3*np.exp(1j*Dchi_23)+a_3**2
    B=1+2*C_12*a_1*a_2*np.cos(Dchi_12)+2*C_13*a_1*a_3*np.cos(Dchi_13)+2*C_23*a_2*a_3*np.cos(Dchi_23)
    return A/B

"""
Contrast
"""
def contrast(name):
    group_p1p1p1_20_Oct = ["ifg_wv1_psi_+1+1+1_No_fit_20Oct1759"]
    group_p1p1p1_22_Oct_morning = ["ifg_wv1_psi_+1+1+1_no_fit_22Oct1050", "ifg_wv2_psi_+1+1+1_no_fit_22Oct1130", "ifg_wv3_psi_+1+1+1_no_fit_22Oct1212"]
    group_p1p1p1_22_Oct_evening = ["ifg_wv1_psi_+1+1+1_no_fit_22Oct2358", "ifg_wv2_psi_+1+1+1_no_fit_23Oct0034", "ifg_wv3_psi_+1+1+1_no_fit_23Oct0111"]
    group_p1p1p1_24_Oct = ["ifg_wv1_psi_+1+1+1_no_fit_24Oct2318", "ifg_wv2_psi_+1+1+1_no_fit_24Oct2354", "ifg_wv3_psi_+1+1+1_no_fit_25Oct0031"]
    group_p1m1m1_22_Oct = ["ifg_wv1_psi_+1-1-1_no_fit_22Oct1257", "ifg_wv2_psi_+1-1-1_no_fit_22Oct1338", "ifg_wv3_psi_+1-1-1_no_fit_22Oct1426"]
    group_p1m1m1_23_Oct = ["ifg_wv1_psi_+1-1-1_no_fit_23Oct0152", "ifg_wv2_psi_+1-1-1_no_fit_23Oct0229", "ifg_wv3_psi_+1-1-1_no_fit_23Oct0305"  ]
    group_p1m1m1_25_Oct = ["ifg_wv1_psi_+1-1-1_no_fit_25Oct0112", "ifg_wv2_psi_+1-1-1_no_fit_25Oct0148", "ifg_wv3_psi_+1-1-1_no_fit_25Oct0225"]
    group_p1mPi3p2Pi3_22_Oct = ["ifg_wv1_psi_+1+exp(-i60)+exp(i120)_no_fit_22Oct1732", "ifg_wv2_psi_+1+exp(-i60)+exp(i120)_no_fit_22Oct1812"]
    group_p1mPi3p2Pi3_24_Oct = ["ifg_wv1_psi_+1+exp(-i60)+exp(i120)_no_fit_24Oct2117"]
    
    if name in group_p1p1p1_20_Oct or name=="group_p1p1p1_20_Oct":
        C_12=0.74
        C_13=0.66
        C_23=0.63
    
    if name in group_p1p1p1_22_Oct_morning or name=="group_p1p1p1_22_Oct_morning":
        C_12=0.72
        C_13=0.67 
        C_23=0.58
    
    if name in group_p1p1p1_22_Oct_evening or name=="group_p1p1p1_22_Oct_evening":
        C_12=0.74
        C_13=0.66
        C_23=0.63
    
    if name in group_p1p1p1_24_Oct or name=="group_p1p1p1_24_Oct":
        C_12=0.68 
        C_13=0.56 
        C_23=0.50
    
    if name in group_p1m1m1_22_Oct or name=="group_p1m1m1_22_Oct":
        C_12=0.77
        C_13=0.67 
        C_23=0.65
    
    if name in group_p1m1m1_23_Oct or name=="group_p1m1m1_23_Oct":
        C_12=0.77
        C_13=0.68
        C_23=0.64
        
    if name in group_p1m1m1_25_Oct or name=="group_p1m1m1_25_Oct":
        C_12=0.81 
        C_13=0.63 
        C_23=0.45
        
    if name in group_p1mPi3p2Pi3_22_Oct or name=="group_p1mPi3p2Pi3_22_Oct":
        C_12=0.74
        C_13=0.66
        C_23=0.62    
    
    if name in group_p1mPi3p2Pi3_24_Oct or name=="group_p1mPi3p2Pi3_24_Oct":
        C_12=0.68 
        C_13=0.56 
        C_23=0.54  
    
    return [C_12,C_13,C_23]

