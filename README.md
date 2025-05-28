# Programming Problems Lists
This repository refers to programming exercise lists in various high-level languages, as well as structured query language. These exercises are applicable both for daily practice to improve programming proficiency and for real and useful applications that can be used as functions or services.



import pandas as pd

arquivo_csv = '\\projetos\\CRRC039_61186680_61186680_20250419_I00001.csv'

pd_arquivo = pd.read_csv(arquivo_csv, chunksize=500000)

chunks_reduzidos = []

for i in pd_arquivo:
	chunk_reduzido = i.iloc[:, :4]
	chunks_reduzidos.append(chunk_reduzido)

df_final = pd.concat(chunks_reduzidos, ignore_index=True)


# Iterating list using enumerate to get both index and element
for i, chunk in enumerate(df_final):
	nome_arquivo = f"\\projetos\arquivos\\CRRC0013_ISPBParticipante_20250528_{i+1}.csv"
	chunk.to_csv(nome_arquivo, index=False)

# print("\\projetos\\CRRC039_61186680_61186680_20250419_I00001.csv")
