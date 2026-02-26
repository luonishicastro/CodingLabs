import random

def main():
  distance = float(input('What is the total distance in kilometers: '))
  if distance <= 200:
    price = 0.5*distance
  else:
    price = 0.45*distance
  print('The total ticket price is: ${:.2f}'.format(price))

if __name__ == '__main__':
  main()