
# coding: utf-8

# In[ ]:


def aumentar(val, formato=False):
    res = val + val*0.1
    return res if formato is False else moeda(res)
    
def diminuir(val, formato=False):
    res = val - val*0.1
    return res if formato is False else moeda(res)
    
def dobro(val, formato=False):
    res = val*2
    return res if formato is False else moeda(res)
    
def metade(val, formato=False):
    res = val/2
    return res if formato is False else moeda(res)

def moeda(val):
    res = '{:.2f}'.format(val)
    res = res.replace('.', ',')
    return res
