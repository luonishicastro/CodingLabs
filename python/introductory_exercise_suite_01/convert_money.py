def main():
  wallet = float(input('Type how much money you have: R$'))
  dollar = 5.18
  print('You total wallet in US Dollars is equal to: U${:.2f}'.format(wallet / dollar))

if __name__ == '__main__':
  main()