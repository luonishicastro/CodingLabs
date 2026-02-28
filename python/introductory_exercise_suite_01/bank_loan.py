def main():
  totalValue = float(input('Total Value of a House: $'))
  BuyingSalary = float(input('Buying Salary: $'))
  installments = float(input('How many year will it be payed: '))

  installmentAmout = totalValue/(installments*12)

  if installmentAmout>(0.3*BuyingSalary):
    print('Denied!')
  else:
    print('Aporoved! Installment of ${:.2f} to be payed during {} year.'.format(installmentAmout, installments))

if __name__ == '__main__':
  main()