import sympy as sp
from IPython.display import display

def main():
  x1, x2, x3, n = sp.symbols('x1 x2 x3 n')
  mean = (x1 + x2 + x3) / 3
  display(sp.Eq(sp.Symbol("mean"), mean))


if __name__ == '__main__':
  main()