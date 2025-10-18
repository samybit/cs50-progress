from cs50 import get_string

# Prompt user for credit card number
num = get_string("Number: ")

# Luhn’s Algorithm
sum_ = 0
reverse_digits = num[::-1]

for i, d in enumerate(reverse_digits):
    n = int(d)
    if i % 2 == 1:
        n *= 2
        if n > 9:
            n -= 9
    sum_ += n

# Check if valid
if sum_ % 10 != 0:
    print("INVALID")
else:
    first_two = int(num[:2])
    first_one = int(num[0])
    length = len(num)

    if length == 15 and first_two in [34, 37]:
        print("AMEX")
    elif length == 16 and 51 <= first_two <= 55:
        print("MASTERCARD")
    elif first_one == 4 and length in [13, 16]:
        print("VISA")
    else:
        print("INVALID")
