def main():
  highestWeight = 0
  lowestWeight = 999
  
  for p in range(1,6):
    weight = float(input('Type the weight of the Person {}: '.format(p)))
    if weight >= highestWeight:
      highestWeight = weight
    if weight <= lowestWeight:
      lowestWeight = weight
      
  print('Highest Weight: {:.2f}Kg'.format(highestWeight))
  print('Lowest Weight: {:.2f}Kg'.format(lowestWeight))

if __name__ == '__main__':
  main()