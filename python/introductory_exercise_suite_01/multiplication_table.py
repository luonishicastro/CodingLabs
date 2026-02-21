def main():
  num = int(input('Type any number: '))
  print('Multiplication Table: ')
  for i in range(1,10):
    print(f'{i} x {num} = {num*i}')

if __name__ == '__main__':
  main()