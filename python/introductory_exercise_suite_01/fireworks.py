import os
from time import sleep

def main():
  cont = 10
  while cont > 0:
    os.system('cls')
    print(cont)
    sleep(1)
    cont = cont - 1
  print('BOOOM')

if __name__ == '__main__':
  main()