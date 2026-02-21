def main():
  value = float(input('Enter a value in meters to be converted: '))
  print('Equivalent in centimeters: {:.2f}'.format(value * 100))
  print('Equivalent in milimeters: {:.2f}'.format(value * 1000))

if __name__ == '__main__':
  main()