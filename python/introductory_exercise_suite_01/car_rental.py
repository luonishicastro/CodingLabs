def main():
  kilometers = int(input('Number of kilometers driven: '))
  days = int(input('Number of days driving: '))
  price_to_pay = 60*days + 0.15*kilometers
  print('Total price to pay will be: ${:.2f}'.format(price_to_pay))


if __name__ == '__main__':
  main()