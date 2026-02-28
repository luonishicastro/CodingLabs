def main():
  year = int(input("Type any year: "))
  if year%4 == 0 and year%100 != 0 or year%400 == 0:
    print("It is a leap year!")
  else:
    print("It's not a leap year.")


if __name__ == '__main__':
  main()