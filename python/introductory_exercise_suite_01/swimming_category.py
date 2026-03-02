import datetime

def main():
  yearb = int(input('Enter the year of birth: '))
  now = datetime.datetime.now()
  age = now.year - yearb
  print('Category: ')
  if age <= 9:
    print('Child')
  elif age <= 14:
    print('Youth')
  elif age <= 19:
    print('Junior')
  elif age <= 20:
    print('Senior')
  else:
    print('Master')

if __name__ == '__main__':
  main()