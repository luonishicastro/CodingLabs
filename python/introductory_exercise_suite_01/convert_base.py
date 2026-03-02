def main():
  num = int(input('Type any integer number: '))
  base = input('What will it be converted to? 1 - binary; 2 - octal; 3 - hexadecimal\n')
  if base == '1':
    print(f'In Binary: {bin(num)[2:]}')
  elif base == '2':
    print(f'In Octal: {oct(num)[2:]}')
  elif base == '3':
    print(f'In Hexadecimal: {hex(num)[2:].upper()}')
  else:
    print('Invalid enter.')

if __name__ == '__main__':
  main()