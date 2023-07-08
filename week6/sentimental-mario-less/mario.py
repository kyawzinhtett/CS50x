import cs50


def main():
    height = get_height()
    # Pyramid Rows
    for i in range(height):
        # Left-align Spaces
        print(" " * (height - (i + 1)), end="")
        # Pyramid Columns
        for k in range(i + 1):
            print("#", end="")
        print()


# Get Height From User
def get_height():
    while True:
        n = cs50.get_int("Height: ")
        if n > 0 and n < 9:
            return n


main()