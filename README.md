# Programming Problems Lists
This repository refers to programming exercise lists in various high-level languages, as well as structured query language. These exercises are applicable both for daily practice to improve programming proficiency and for real and useful applications that can be used as functions or services.





import pandas as pd

arquivo_csv = '\\projetos\\CRRC039_61186680_61186680_20250419_I00001.csv'

pd_arquivo = pd.read_csv(arquivo_csv, sep=';', header=None, chunksize=500000)

# Iterating list using enumerate to get both index and element
for i, chunk in enumerate(pd_arquivo):
    chunk = chunk.iloc[:, :4]
    nome_arquivo = f"\\projetos\\arquivos\\CRRC0013_ISPBParticipante_20250528_{i+1}.csv"
    chunk.to_csv(nome_arquivo, index=False, sep=';')


File "c:\Users\lucas.onishi\Desktop\Scripts\partition_data.py", line 8, in <module>
    for i, chunk in enumerate(pd_arquivo):
                    ~~~~~~~~~^^^^^^^^^^^^
  File "C:\Users\lucas.onishi\AppData\Roaming\Python\Python313\site-packages\pandas\io\parsers\readers.py", line 1843, in __next__
    return self.get_chunk()
           ~~~~~~~~~~~~~~^^
  File "C:\Users\lucas.onishi\AppData\Roaming\Python\Python313\site-packages\pandas\io\parsers\readers.py", line 1985, in get_chunk
    return self.read(nrows=size)
           ~~~~~~~~~^^^^^^^^^^^^
  File "C:\Users\lucas.onishi\AppData\Roaming\Python\Python313\site-packages\pandas\io\parsers\readers.py", line 1923, in read
    ) = self._engine.read(  # type: ignore[attr-defined]
        ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        nrows
        ^^^^^
    )
    ^
  File "C:\Users\lucas.onishi\AppData\Roaming\Python\Python313\site-packages\pandas\io\parsers\c_parser_wrapper.py", line 234, in read
    chunks = self._reader.read_low_memory(nrows)
  File "parsers.pyx", line 850, in pandas._libs.parsers.TextReader.read_low_memory
  File "parsers.pyx", line 905, in pandas._libs.parsers.TextReader._read_rows
  File "parsers.pyx", line 874, in pandas._libs.parsers.TextReader._tokenize_rows
  File "parsers.pyx", line 891, in pandas._libs.parsers.TextReader._check_tokenize_status
  File "parsers.pyx", line 2061, in pandas._libs.parsers.raise_parser_error
pandas.errors.ParserError: Error tokenizing data. C error: Expected 4 fields in line 2, saw 14

