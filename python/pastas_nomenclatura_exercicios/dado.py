
# coding: utf-8

# In[ ]:

def resumo():
    return 'RESUMO DO VALOR.'


def leiaDinheiro(num):
    n = str(input(num))
    if not n.isalpha():
        return float(n)