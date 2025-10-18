from cs50 import get_int

# Prompt user for height
while True:
    hight = get_int("Height: ")
    if 1 <= hight <= 8:
        break

# Build the pyramids
for i in range(1, hight + 1):
    print(" " * (hight - i) + "#" * i + "  " + "#" * i)
