from cs50 import get_string

# Prompt user for input
text = get_string("Text: ")

# Count letters, words, and sentences
letters = sum(1 for c in text if c.isalpha())
words = len(text.split())
sentences = sum(1 for c in text if c in ['.', '!', '?'])

# Calculate averages per 100 words
L = (letters / words) * 100
S = (sentences / words) * 100

# Coleman-Liau index
index = round(0.0588 * L - 0.296 * S - 15.8)

# Output grade level
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
