def main():
  line1 = int(input('First segment length: '))
  line2 = int(input('Second segment length: '))
  line3 = int(input('Third segment length: '))
  flagTriangle = 0
  if (abs(line2-line3))<line1 and line1<(line2+line3):
    flagTriangle = 1
  elif (abs(line1-line3))<line2 and line2<(line1+line3):
    flagTriangle = 1
  elif (abs(line1-line2))<line3 and line3<(line1+line2):
    flagTriangle = 1

  if flagTriangle == 1:
    print('Sides {} {} {} constitutes a Triangle.'.format(line1, line2, line3))
  else:
    print('Sides {} {} {} do not constitutes a Triangle.'.format(line1, line2, line3))

if __name__ == '__main__':
  main()