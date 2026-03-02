def main():
  initialPrice = float(input('Product price: $'))
  cond = int(input('Options: \n[1] Cash or check\n'
                        '[2] Immediate payment by card\n'
                            '[3] Up to 2 installments on the card\n'
                                '[4] 3 or more installments on the card\n'
                                    'Condition: '))
  if cond == 1:
    finalPrice = initialPrice-initialPrice*0.1
  elif cond == 2:
    finalPrice = initialPrice-initialPrice*0.05
  elif cond == 4:
    finalPrice = initialPrice + initialPrice*0.2
  else:
    finalPrice = initialPrice
    
  print('Payment Condition: {}\nProduct Price: R${:.2f} \Final Price: R${:.2f}'.format(cond, initialPrice, finalPrice))


if __name__ == '__main__':
  main()