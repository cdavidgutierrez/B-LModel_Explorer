import sys
import os
import shutil
import subprocess

import numpy as np

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 paramsSpace.py <input_file_path> <SPheno_output_path> <input_card_file_path>")
        return
    
    input_file_path = sys.argv[1]
    spheno_file_path = sys.argv[2]
    IC_file_path = sys.argv[3]
    temp_output_file_path = os.path.dirname(input_file_path)+'/Temp_Modified_LesHouches.in.BLSM'

    # Check if the folder exists
    if not os.path.exists(input_file_path):
        print(f"The folder '{input_file_path}' does not exist.")
        return
    
    ZpMass_spec = np.linspace(1500, 7200, 25)
    g1p_spec = np.linspace(0.2, 1.0, 25)
    params_combinations = np.array(np.meshgrid(ZpMass_spec, g1p_spec)).T.reshape(-1,2)
    allowed_params = [(g, 0.5*mass/g) for mass, g in params_combinations if mass/g>=7100]

    for params in allowed_params:
        str_param_array = [str(value) for value in params]
        new_parameters = dict(zip(['g1pINPUT', 'vXinput'], str_param_array))

        # Modify parameter values and write to the temporary output file
        with open(input_file_path, 'r') as input_file, open(temp_output_file_path, 'w') as temp_output_file:
            for line in input_file:
                for parameter_name, new_value in new_parameters.items():
                    if parameter_name in line:
                        parts = line.split()
                        parts[1] = new_value
                        line = " ".join(parts) + "\n"
                        break
                temp_output_file.write(line)

        shutil.move(temp_output_file_path, input_file_path)
        current_directory = os.getcwd()

        try:
            # Change the working directory
            os.chdir("/home/david/Documents/BSM-Submodules/SPheno")

            # Execute SPhenoBLSM
            subprocess.run(["bin/SPhenoBLSM", "LesHouches.in.BLSM"])

            # Execute paramsExtractor.py
            subprocess.run(["python3", "/home/david/Desktop/ZpExplorer/paramsExtractor.py", spheno_file_path, IC_file_path])

        finally:
            # Restore the working directory even if an exception occurs
            os.chdir(current_directory)

    return allowed_params

if __name__ == "__main__":
    main()
