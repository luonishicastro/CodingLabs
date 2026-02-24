def main():
  city_name = input('Type the name of a city: ')
  first_word = city_name.split()[0]
  if first_word.upper() == 'SANTO':
    print('This city begins with Santo.')
  else:
    print('This city does not begins with Santo.')


if __name__ == '__main__':
  main()