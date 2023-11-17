import sys
import os

import numpy as np

from SM_couplings import *

def main():

    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 SSM_space.py <input_card_file_path>")
        return
    
    IC_file_path = sys.argv[1]
    fermion_charges = {'u':(1/2, 2/3), 'd':(-1/2, -1/3), 'e':(-1/2, -1)} #'f':(T3, Q, Y')
    fermions = list(fermion_charges.keys())
    u_charges = fermion_charges[fermions[0]]
    d_charges = fermion_charges[fermions[1]]
    e_charges = fermion_charges[fermions[2]]

    ZpMass_spec = np.linspace(2.0, 6.0, 500) #en TeV

    for mass in ZpMass_spec:
        model_params = [mass]

        for i in range(3):
            #print('Calculando g para {}'.format(fermions[0]+str(i+1)+'L'))
            model_params.append(g_f_L(*u_charges))
            model_params.append(g_f_R(*u_charges))
            model_params.append(g_f_L(*d_charges))
            model_params.append(g_f_R(*d_charges))

        for i in range(3):
            model_params.append(g_f_L(*e_charges))
            model_params.append(g_f_R(*e_charges))

        model_params.append(Gamma_inv(mass))

        #Γww = ΓZh = Γxx = 0
        model_params.append(0)
        model_params.append(0)
        model_params.append(0)

        rouded_params = [round(param, 6) for param in model_params]
        str_params = [str(param) for param in rouded_params]
        BP_string = '  '.join(str_params)

        # Create a file
        output_file_path = os.path.join(IC_file_path, "icard_B-L.dat")
        with open(output_file_path, "a") as file:
            file.write(BP_string+'\n')

    print(f"icard file has been written to '{output_file_path}'")

    return 0

if __name__ == "__main__":
    main()
