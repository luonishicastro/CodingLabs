def main():
  num1 = int(input('Type the first number: '))
  num2 = int(input('Type the second number: '))
  num3 = int(input('Type the third number: '))
  if num1 >= num2 and num1 >= num3:
    biggest = num1
    if num2 <= num3:
      lower = num2
    else:
      lower = num3
  elif num2 >= num1 and num2 >= num3:
    biggest = num2
    if num1 <= num3:
      lower = num1
    else:
      lower = num3
  elif num3 >= num1 and num3 >= num2:
    biggest = num3
    if num1 <= num2:
      lower = num1
    else:
      lower = num2

  print(f'Biggest number: {biggest}')
  print(f'Lower number: {lower}')

if __name__ == '__main__':
  main()