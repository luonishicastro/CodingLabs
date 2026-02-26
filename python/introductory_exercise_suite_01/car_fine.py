import random

def main():
  veloc = float(input('Enter the speed of a car (km/h): '))
  if veloc > 80:
    fine = (veloc-80)*7
    print('The driver has been fined! The fine will be ${:.2f}'.format(fine))

if __name__ == '__main__':
  main()