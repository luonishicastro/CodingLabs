def main():
  sex = ""
  options = ["M", "F"]
  while (sex not in options):
    sex = input("Person's Gender: ").upper()
    if sex not in options:
      print("Invalid Option! Try again.")
    else:
      if sex == "F":
        print("Female.")
      elif sex == 'M':
        print("Male.")

if __name__ == '__main__':
  main()