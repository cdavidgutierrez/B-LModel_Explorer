import numpy as np

_ALPHAem = (1.279320e2)**(-1)
_GF = 1.1663788e-5
_MZ = 91.18870
_THETAW = np.arcsin(np.sqrt(0.23121))

def gp_axial(T3, thetap):
    return -T3*np.sin(thetap)

def gp_vector(T3, Q, Y, g1p, g, thetap, thetaW = _THETAW):
    return -T3*np.sin(thetap)+2*Q*np.sin(thetaW)**2*np.sin(thetap)+2*Y*g1p/g*np.cos(thetaW)*np.cos(thetap)

def g_f_L(T3, Q, Yp, g1p, thetap, thetaW = _THETAW, Nc = 1):
    coef1 = (2*np.sqrt(_ALPHAem*np.pi))/(np.cos(thetaW)*np.sin(thetaW))

    #return coef1*(-T3 + Q*np.sin(thetaW)**2)*np.sin(thetap) + Yp*g1p*np.cos(thetap)
    return g1p*Yp

def g_f_R(T3, Q, Yp, g1p, thetap, thetaW = _THETAW, Nc = 1):
    #return np.sqrt(_ALPHAem*np.pi)*Q*np.tan(thetaW)*np.sin(thetap) + 0.5*Yp*g1p*np.cos(thetap)
    return g1p*Yp

def Lamd(MZp, Mh):
    r_ZZp = _MZ/MZp
    r_hZp = Mh/MZp

    return 1+r_ZZp**2+r_hZp**2-2*r_ZZp-2*r_hZp-2*r_ZZp*r_hZp

def Gamma_Zh(g1p, L, v, thetap, MZp, MZ = _MZ):
    #coef = (g**2*MZ**2)/(192*np.pi*MW**2)*MZp*np.sqrt(L)
    coef = np.sqrt(2)/(48*np.pi)*_GF*MZ**2*MZp*np.sqrt(L)*np.sin(thetap)
    f1 = L+12*(MZ/MZp)**2
    f2 = (4*MZ**2/v**2-g1p**2)*np.sin(2*thetap)+(4*MZ*g1p/v)*np.cos(2*thetap)

    return coef*f1*f2

def Gamma_WW(MZ, MW, MZp, thetap, thetaW = _THETAW):
    #coef = g**2/(192*np.pi)*np.cos(thetaW)**2*np.sin(thetap)*MZp*(MZp/MZ)**4
    coef = _ALPHAem/(48*np.tan(thetaW)**2)*np.sin(thetap)*MZp*(MZp/MZ)**4
    f1 = (1-4*MW**2/MZp**2)**(3/2)
    f2 = 1+20*MW**2/MZp**2+12*MW**4/MZp**4

    return coef*f1*f2