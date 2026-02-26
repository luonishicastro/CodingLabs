import random

def main():
  num = random.randint(1,5)
  guess = int(input('Guess a number between 1 and 5: '))
  if num == guess:
    print(f'You win, the number is {num}')
  else:
    print(f'You lost, the sorted number is {num}')

if __name__ == '__main__':
  main()