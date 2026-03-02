def main():
  num1 = int(input('Enter the first number: '))
  num2 = int(input('Enter the second number: '))
  if num1 > num2:
    print('The first value is greater')
  elif num1 < num2:
    print('The second value is greater')
  else:
    print('There is no greater value, both are equal.')

if __name__ == '__main__':
  main()