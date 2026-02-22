import random

def main():
  student1 = input('Name of the first student: ')
  student2 = input('Name of the second student: ')
  student3 = input('Name of the thrird student: ')
  student4 = input('Name of the fourth student: ')
  sorteded = random.randint(1,4)

  if sorteded == 1:
    print(f'Choosen Student: {student1}')
  elif sorteded == 2:
    print(f'Choosen Student: {student2}')
  elif sorteded == 3:
    print(f'Choosen Student: {student3}')
  elif sorteded == 4:
    print(f'Choosen Student: {student4}')

if __name__ == '__main__':
  main()