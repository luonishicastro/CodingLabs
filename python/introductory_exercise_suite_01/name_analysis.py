def main():
  name = input('What is you name? ')
  print('The name in all uppercase letters: {}'.format(name.upper()))
  print('The name in all lowercase letters: {}'.format(name.lower()))
  print('The total number of letters (excluding spaces): {}'.format(len(name.replace(' ', ''))))
  print('The number of letters in the first name: {}'.format(len(name.split()[0])))

if __name__ == '__main__':
  main()