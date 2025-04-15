'''
Given an integer, n , perform the following conditional actions:
If n is odd, print Weird
If n is even and in the inclusive range of  to , print Not Weird
If n is even and in the inclusive range of  to , print Weird
If n is even and greater than , print Not Weird

'''
if __name__ == '__main__':
    n = input("Digite um numero: ")
    if not n % 2 == 0:
        print('Weird')