def main():
  name = input('Write your full name:')
  print(f'First name: {name.split()[0]}')
  print(f'Last name: {name.split()[-1]}')


if __name__ == '__main__':
  main()