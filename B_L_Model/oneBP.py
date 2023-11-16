import sys
import os
import shutil
import subprocess

import numpy as np

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 oneBP.py <SPheno_output_path> <input_card_file_path>")
        return

    spheno_file_path = sys.argv[1]
    IC_file_path = sys.argv[2]

    subprocess.run(["python3", "/home/david/Desktop/ZpExplorer/paramsExtractor.py", spheno_file_path, IC_file_path])

if __name__ == "__main__":
    main()