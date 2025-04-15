if __name__ == '__main__':
    print("Hello, World!")

'''
Quando você roda um arquivo Python diretamente (por exemplo: python meu_script.py), o Python define uma variável especial
chamada __name__ com o valor '__main__'.
Se esse mesmo arquivo for importado como módulo dentro de outro script (import meu_script), o valor de __name__ será o nome
do módulo ('meu_script'), e não '__main__'.
'''
