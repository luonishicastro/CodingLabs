
# coding: utf-8

from lib import leiaNum

def linha(tam=42):
    return '-' * tam

def cabecalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())
    
def menu(lista):
    cabecalho('MENU PRINCIPAL')
    c=1
    for item in lista:
        print(f'\033[33m{c} - \033[34m {item}\033[m')
        c+=1
    print(linha())
    opc = leiaNum.leiaInt('\033[32mSua Opção: \033[m')
    return opc