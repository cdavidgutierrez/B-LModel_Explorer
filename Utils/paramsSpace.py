import sys
import os
import shutil
import subprocess

import numpy as np

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 paramsSpace.py <input_file_path>")
        return
    
    input_file_path = sys.argv[1]
    temp_output_file_path = os.path.dirname(input_file_path)+'/Temp_Modified_LesHouches.in.BLSM'


    # Check if the folder exists
    if not os.path.exists(input_file_path):
        print(f"The folder '{input_file_path}' does not exist.")
        return
    
    keys = ["Lambda1INPUT", "Lambda2INPUT", "Lambda3INPUT", "g1pINPUT", "g1p1INPUT", "g11pINPUT", "vXinput"]
    
    Lambda1 = np.linspace(-2.0e-1, 2.0e-1, 10)
    Lambda2 = np.linspace(-1.0e-4, 1.0e-4, 10)
    Lambda3 = np.linspace(-0.2e-1, 0.2e-1, 10)
    g1p = np.linspace(1e-3, 0.999, 10)
    g1p1 = np.array([0.0])
    g11p = np.array([0.0])
    vX = np.linspace(1.0e3, 8.0e3, 10)

    params_combinations = np.array(np.meshgrid(Lambda1, Lambda2, Lambda3, g1p, g1p1, g11p, vX )).T.reshape(-1,7)

    for param_array in params_combinations:
        # Define the parameter names and new values
        str_param_array = [str(value) for value in param_array]
        new_parameters = dict(zip(keys, str_param_array))

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
            subprocess.run(["python3", "paramsExtractor.py", input_file_path, "input_card_file_path"])

        finally:
            # Restore the working directory even if an exception occurs
            os.chdir(current_directory)

if __name__ == "__main__":
    main()
