def main():
  summ = 0
  for i in range(1,501):
    if (i%3==0) and (i%2!=0):
      summ = summ + i
  return summ

if __name__ == '__main__':
  main()