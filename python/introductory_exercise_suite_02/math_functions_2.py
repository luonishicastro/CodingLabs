import sympy as sp
from IPython.display import display

def main():
  x = sp.symbols('x')
  sinc = sp.Piecewise(
    (1, x == 0),
    (sp.sin(x)/x, True)
  )
  display(sp.Eq(sp.Function("sinc")(x), sinc))


if __name__ == '__main__':
  main()