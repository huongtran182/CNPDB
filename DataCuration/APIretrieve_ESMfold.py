# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 15:41:50 2025

"""

import requests
import pandas as pd

sequence_list_path = "ESMfold\sequence_IDs.csv"
sequence_list = pd.read_csv(sequence_list_path)

url = "https://api.esmatlas.com/foldSequence/v1/pdb/" # API endpoint
output_dir = "CNPDB\Assets\3D Structure ESMFold 1_1000"

for x in range(0,len(sequence_list)):
    accession = sequence_list['cNPDB ID'].iloc[x]
    sequence = sequence_list['Sequence'].iloc[x]

    response = requests.post(url, data=sequence)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the result as a PDB file
        with open(f"{output_dir}//3D Meta cNP{str(accession)}.pdb", "wb") as f:
            f.write(response.content)
        print("PDB structure saved as prediction.pdb")
    else:
        print(f"Error {response.status_code}: {response.text}")
