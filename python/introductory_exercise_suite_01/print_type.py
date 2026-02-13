def main():
  var = input('Type anything: ')
  return type(var), var.isnumeric(), var.isalnum()

if __name__ == '__main__':
  main()