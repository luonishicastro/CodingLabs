def main():
  firstTerm = int(input("Type the first term: "))
  difference = int(input("Common Difference: "))
  print(firstTerm, end=' ')
  for i in range(2,11):
    print(firstTerm+(i-1)*difference, end=' ')

if __name__ == '__main__':
  main()