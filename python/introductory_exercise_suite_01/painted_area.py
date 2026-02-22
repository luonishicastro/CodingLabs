def main():
  width = float(input('Enter width in meters: '))
  height = float(input('Enter height in meters: '))
  area = width * height
  return 'Amount of paint will be', area/2


if __name__ == '__main__':
  main()