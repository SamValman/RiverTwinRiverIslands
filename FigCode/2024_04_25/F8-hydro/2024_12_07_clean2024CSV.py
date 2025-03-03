# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:13:13 2024

@author: lgxsv2
"""

import pandas as pd

# fps
input_file = r"D:\GeomorphologyPaper\Analysis\Figures\2024_04_25\F8-hydro\guageCSVs\15400000_Cotas_2024_unformatted.csv"  
output_file = r"D:\GeomorphologyPaper\Analysis\Figures\2024_04_25\F8-hydro\guageCSVs\15400000_cotas_2024_formatted.csv"

# Define headers
desired_headers = [
    "EstacaoCodigo", "NivelConsistencia", "Data", "MediaDiaria", "TipoMedicaoCotas",
    "Maxima", "Minima", "Media", "DiaMaxima", "DiaMinima", "MaximaStatus",
    "MinimaStatus", "MediaStatus", "MediaAnual", "MediaAnualStatus",
] + [f"Cota{i:02}" for i in range(1, 32)] + [f"Cota{i:02}Status" for i in range(1, 32)]

# Use the correct delimiter
df = pd.read_csv(input_file, delimiter=';', dtype=str)

# Drop  "hora" column
df.drop(columns=['hora'], inplace=True)

# Update  headers
df.columns = desired_headers

# Save 
df.to_csv(output_file, index=False, sep=',')  # Use ',' for the standard CSV delimiter
print(f"Data has been cleaned and saved to {output_file}.")
