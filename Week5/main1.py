
num = input("Please enter a number: ")

while not num.isdigit():
    print("Please enter a number, try again")
    num = input("Please enter a number: ")

num = int(num)

if num % 2 == 0:
    if num % 3 == 0:
        print(num, "is even and devisible by 3")
    else:
        print(num, "is even and not devisible by 3")
else:
    if num % 3 == 0:
        print(num, "is not even and devisible by 3")
    else:
        print(num, "is not even and not devisible by 3")
