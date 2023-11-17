import numpy as np

_ALPHAem = (1.279320e2)**(-1)
_s2_W = 0.23121
_c2_W = 1-_s2_W

def g_f_L(T3, Q):
    return 2*np.sqrt(_ALPHAem*np.pi)/np.sqrt(_s2_W*_c2_W)*(T3-Q*_s2_W)

def g_f_R(T3, Q):
    return -2*np.sqrt(_ALPHAem*np.pi)/np.sqrt(_s2_W*_c2_W)*Q*_s2_W

def Gamma_inv(MZp):
    return _ALPHAem*MZp/(8*_s2_W*_c2_W)
