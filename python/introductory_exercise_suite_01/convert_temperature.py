def main():
  celsius = float(input('Enter temperature in Celsius: '))
  fahrenheit = (celsius*1.8)+32
  print(f'Correspondent temperature of {celsius} Celsius is {fahrenheit} Fahrenheit.')

if __name__ == '__main__':
  main()