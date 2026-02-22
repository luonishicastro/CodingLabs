def main():
  price = float(input('Price of the product: $'))
  price_discount = price * 0.05
  print('The product price with discount will be ${:.2f}'.format(price-price_discount))


if __name__ == '__main__':
  main()