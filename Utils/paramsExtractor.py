from paramsFunctions import *
from paramsFinder import *

import sys
import os

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 paramsExtractor.py <LesHouches_file_path> <input_card_file_path>")
        return
    
    LH_file_path = sys.argv[1]
    IC_file_path = sys.argv[2]

    # Check if the folder exists
    if not os.path.exists(LH_file_path):
        print(f"The file '{LH_file_path}' does not exist.")
        return
    
    text_file = open(LH_file_path, "r")
    data = text_file.read()
    text_file.close()

    THETA_BL = blMixAngle(data) #1e-3 |T_bl|<=10^-3
    bosonMasses = massBlock(data)

    gamma_inv, gamma_xx = decayBlock(data)

    fermion_charges = {'u':(1/2, 2/3, 1/3), 'd':(-1/2, -1/3, 1/3), 'e':(-1/2, -1, -1)} #'f':(T3, Q, Y')
    couplings = couplingsBlock(data)

    model_params = [bosonMasses[0]/1000] #in TeV
    fermions = list(fermion_charges.keys())
    u_charges = fermion_charges[fermions[0]]
    d_charges = fermion_charges[fermions[1]]
    e_charges = fermion_charges[fermions[2]]

    for i in range(3):
        model_params.append(g_f_L(*u_charges, couplings['gBL'], THETA_BL, Nc=3))
        model_params.append(g_f_R(*u_charges, couplings['gBL'], THETA_BL, Nc=3))
        model_params.append(g_f_L(*d_charges, couplings['gBL'], THETA_BL, Nc=3))
        model_params.append(g_f_R(*d_charges, couplings['gBL'], THETA_BL, Nc=3))

    for i in range(3):
        model_params.append(g_f_L(*e_charges, couplings['gBL'], THETA_BL))
        model_params.append(g_f_R(*e_charges, couplings['gBL'], THETA_BL))

    model_params.append(gamma_inv)
    model_params.append(Gamma_WW(bosonMasses[1], bosonMasses[3], bosonMasses[0], THETA_BL))
    lamb = Lamd(bosonMasses[0], bosonMasses[2])
    model_params.append(Gamma_Zh(couplings['gBL'], lamb, bosonMasses[4], THETA_BL, bosonMasses[0]))
    model_params.append(gamma_xx)

    rouded_params = [round(param, 4) for param in model_params]
    str_params = [str(param) for param in rouded_params]
    BP_string = '  '.join(str_params)

    output_file_path = os.path.join(IC_file_path, "icard_B-L.dat")
    with open(output_file_path, "a") as file:
        file.write(BP_string+'\n')

    print(f"icard file has been written to '{output_file_path}'")

if __name__ == "__main__":
    main()
