from string import ascii_letters, ascii_lowercase, ascii_uppercase

# print(ascii_letters)
# print(ascii_lowercase)
# print(ascii_uppercase)

from yacut.models import generate_short

for _ in range(10):
    print(generate_short())
