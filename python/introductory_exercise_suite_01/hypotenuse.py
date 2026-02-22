import math

def main():
  op_side = int(input('Opposite Side of a right Triangle: '))
  ad_side = int(input('Adjacent Side of a right Triangle: '))
  hyp = math.sqrt(op_side * op_side + ad_side*ad_side)
  print('The hypotenuse of a right triangle with opposite side of {} and adjacent side of {} will be {}.'.format(op_side, ad_side, hyp))


if __name__ == '__main__':
  main()