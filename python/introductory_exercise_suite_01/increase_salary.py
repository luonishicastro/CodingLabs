def main():
  salary = float(input('Enter your salary: $'))
  if salary > 1250:
    increase = salary*0.1
  else:
    increase = salary*0.15
  
  print('New salary: ${}'.format(salary+increase))

if __name__ == '__main__':
  main()