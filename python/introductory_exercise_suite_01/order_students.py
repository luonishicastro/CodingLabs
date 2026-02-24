import random

def main():
  student1 = input('Name of the first student: ')
  student2 = input('Name of the second student: ')
  student3 = input('Name of the third student: ')
  student4 = input('Name of the fourth student: ')
  students_list = [student1, student2, student3, student4]
  random.shuffle(students_list)
  return students_list

if __name__ == '__main__':
  main()