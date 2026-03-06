import random

def main():
  play = int(input("Make your move: \n 1 - Rock \n 2 - Paper \n 3 - Scissor\n"))
  counterMove = random.randint(1,3)
  if play == counterMove:
    print("It's a Draw.")
  elif (play == 1 and counterMove == 3) or (play == 2 and counterMove == 1) or (play == 3 and counterMove == 2):
    print("You Won!")
    if play == 1:
      print("Rock smashes Scissor!")
    elif play == 2:
      print("Paper covers Rock!")
    elif play == 3:
      print("Scissors cuts Paper!")
  elif (play == 1 and counterMove == 2) or (play == 2 and counterMove == 3) or (play == 3 and counterMove == 1):
    print("You Lose!")
    if play == 1:
      print("Paper covers Rock!")
    elif play == 2:
      print("Scissors cuts Paper!")
    elif play == 3:
      print("Rock smashes Scissor!")


if __name__ == '__main__':
  main()