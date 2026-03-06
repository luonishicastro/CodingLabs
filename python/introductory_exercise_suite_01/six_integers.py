def main():
  print('Type six numbers.')
  summ = 0
  for i in range(1,7):
    num = int(input())
    if num%2 == 0:
      summ = summ + num
  print(f'Sum of all even numbers is {summ}')

if __name__ == '__main__':
  main()