import re
import numpy as np

def massBlock(string_data):
    Zp_mass_ptr1 = r'Block MASS  # Mass spectrum([\s#a-zA-Z0-9.+_\-]+)Block SCALARMIX'
    mass_block = re.findall(Zp_mass_ptr1, string_data)[0]

    Zp_mass = float(re.findall(r'31\s+([0-9E.+\-]+)', mass_block)[0])
    Z_mass = float(re.findall(r'23\s+([0-9E.+\-]+)', mass_block)[0])
    h_mass = float(re.findall(r'25\s+([0-9E.+\-]+)', mass_block)[0])
    W_mass = float(re.findall(r'24\s+([0-9E.+\-]+)', mass_block)[0])

    v_value_ptr1 = r'Block HMIX Q=\s+[0-9.E+\-\s]+# \(Renormalization Scale\)\n([\s#a-zA-Z0-9.+_\-]+)Block ANGLES Q'
    v_block = re.findall(v_value_ptr1, string_data)[0]

    v_value = float(re.findall(r'[0-9]+\s+([0-9E.+\-]+)', v_block)[0])

    return Zp_mass, Z_mass, h_mass, W_mass, v_value

def blMixAngle(string_data):
    angles_ptr1 = r'Block ANGLES Q=\s+[0-9.E+\-\s]+# \(Renormalization Scale\)\n([\s#a-zA-Z0-9.+_\-]+)Block YX Q'
    angles_block = re.findall(angles_ptr1, string_data)[0]

    angle_value = float(re.findall(r'[0-9]+\s+([0-9E.+\-]+)', angles_block)[0])

    return angle_value

def couplingsBlock(string_data):
    coupling_cts_ptr = r'Block GAUGE Q=  [0-9.E+\-]+  # \(Renormalization Scale\)([\s#a-zA-Z0-9.+_\-]+)Block BL' #Corregir 1.60000000E\+02
    coupling_cts_str = re.findall(coupling_cts_ptr, string_data)[0]
    coupling_list = np.array([re.findall('\s+'+str(id)+r'\s+([0-9E.+\-]+)\s+#\s([A-Za-z0-9]+)\n', coupling_cts_str) for id in [1,11,2,3,4,10]])
    couplings = dict(zip(coupling_list.T[1][0], [float(g) for g in coupling_list.T[0][0]]))

    return couplings

def decayBlock(string_data):
    Zp_Tdecay_ptr = r'DECAY\s+31\s+([0-9\.E+]+)'
    Zp_Tdecay = float(re.findall(Zp_Tdecay_ptr, string_data)[0])

    Zp_BR_pattern = r'\d+\.\d+E[+-]\d+\s+\d+\s+[-\d]+\s+[-\d]+\s+#\s+BR\(VZp\s*->\s*.*\)'
    Zp_BR = re.findall(Zp_BR_pattern, string_data)

    Gamma_inv = 0
    Gamma_xx = 0

    for n in range(1,4):
        for line in Zp_BR:
            if re.search(r'#\s+BR\(VZp\s*->\s*Fv_'+str(n)+'.*\)', line):
                Gamma_inv += float(re.findall(r'([\w.+\-]+)\s', line)[0])

    for n in range(4,7):
        for line in Zp_BR:
            if re.search(r'#\s+BR\(VZp\s*->\s*Fv_'+str(n)+'.*\)', line):
                Gamma_xx += float(re.findall(r'([\w.+\-]+)\s', line)[0])

    Gamma_inv = Zp_Tdecay*Gamma_inv/1000 #En TeV
    Gamma_xx = Zp_Tdecay*Gamma_xx*0 #Para tomar el valor de SPheno, no multiplicar por 0

    return Gamma_inv, Gamma_xx