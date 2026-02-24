def main():
  name = input('Type your full name: ')
  silva_name = False
  for i in name.split():
    if i.upper() == 'SILVA':
      silva_name = True
  print(f'The name contains Silva: {silva_name}')

if __name__ == '__main__':
  main()