# Programming Problems Lists
This repository refers to programming exercise lists in various high-level languages, as well as structured query language. These exercises are applicable both for daily practice to improve programming proficiency and for real and useful applications that can be used as functions or services.


import pandas as pd

arquivo_csv = '\\projetos\\CRRC039_61186680_61186680_20250419_I00001.csv'

pd_arquivo = pd.read_csv(arquivo_csv, sep=';', chunksize=500000)

# Iterating list using enumerate to get both index and element
for i, chunk in enumerate(pd_arquivo):
    chunk = chunk.iloc[:, :4]
    nome_arquivo = f"\\projetos\\arquivos\\CRRC0013_ISPBParticipante_20250528_{i+1}.csv"
    chunk.to_csv(nome_arquivo, index=False, sep=';')


01;41795262000177;22896431000200;61186680000174;062;2025-01-13;2025-01-13;2025-08-15;2025011301764740517;;S;A;20240529114258542;

S;A;20240529114258542;
