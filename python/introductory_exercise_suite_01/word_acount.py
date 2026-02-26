def main():
  phrase = input('Write any phrase: ').upper()
  aquant = phrase.count('A')
  apost = phrase.find('A')+1
  alast = phrase.rfind('A')+1
  print(f'Quantity of A: {aquant}')
  print(f'First A position: {apost}')
  print(f'Last A position: {alast}')

if __name__ == '__main__':
  main()