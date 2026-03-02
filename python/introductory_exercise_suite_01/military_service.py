import datetime

def main():
  yearb = int(input('Year of your birth: '))
  now = datetime.datetime.now()
  age = now.year - yearb
  
  if age == 18:
    print('It is time to enlist.')
  elif age > 18:
    print(f'Enlisting period has already passed by {age-18} years.')
  else:
    print(f'Still {18-age} years left to enlist.')

if __name__ == '__main__':
  main()