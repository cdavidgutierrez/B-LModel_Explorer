import sys
import os
import shutil
import subprocess

import numpy as np

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 oneBP.py <input_file_path> <SPheno_output_path> <input_card_file_path>")
        return

    input_file_path = sys.argv[1]
    spheno_file_path = sys.argv[2]
    IC_file_path = sys.argv[3]
    temp_output_file_path = os.path.dirname(input_file_path)+'/Temp_Modified_LesHouches.in.BLSM'

    ZpMass_val = 4900
    g1p_val = 0.2
    new_parameters = {'g1pINPUT':str(g1p_val), 'vXinput':str(0.5*ZpMass_val/g1p_val)}

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

        subprocess.run(["python3", "../Utils/paramsExtractor.py", spheno_file_path, IC_file_path])

    finally:
            # Restore the working directory even if an exception occurs
            os.chdir(current_directory)
    
    return 0

if __name__ == "__main__":
    main()
