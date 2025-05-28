# Programming Problems Lists
This repository refers to programming exercise lists in various high-level languages, as well as structured query language. These exercises are applicable both for daily practice to improve programming proficiency and for real and useful applications that can be used as functions or services.


import pandas as pd

arquivo_csv = '\\projetos\\CRRC039_61186680_61186680_20250419_I00001.csv'

pd_arquivo = pd.read_csv(arquivo_csv, chunksize=500000)

# Iterating list using enumerate to get both index and element
for i, chunk in enumerate(pd_arquivo):
    chunk = chunk.iloc[:, :4]
    nome_arquivo = f"\\projetos\\arquivos\\CRRC0013_ISPBParticipante_20250528_{i+1}.csv"
    chunk.to_csv(nome_arquivo, index=False)



01;36866441000118;31924660000192;61186680000174;008;2023-07-27;2023-07-27;2033-07-27;2023052203014535807;;S;A;00000000000028366537;
