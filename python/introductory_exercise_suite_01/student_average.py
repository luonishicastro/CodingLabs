def main():
  grade1 = float(input('Enter the first grade: '))
  grade2 = float(input('Enter the second grade: '))
  average = (grade1 + grade2) / 2

  if average < 5:
    print('FAILED')
  elif average >= 5 and average <= 6.9:
    print('RECOVERY')
  else:
    print('PASSED')

if __name__ == '__main__':
  main()