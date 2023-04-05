def main():
    # Prompt for input
    number = input("Number: ")

    # Print AMEX, MASTERCARD, VISA, or INVALID
    if checksum(number) == False:
        print("INVALID")
    elif checkamex(number) == True:
        print("AMEX")
    elif checkmaster(number) == True:
        print("MASTERCARD")
    elif checkvisa(number) == True:
        print("VISA")
    else:
        print("INVALID")


# Check AMEX
def checkamex(number):
    # Check for card length and starting digits
    if len(number) == 15 and number[:2] in ["34", "37"]:
        return True
    else:
        return False


# Check MASTERCARD
def checkmaster(number):
    # Check for card length and starting digits
    if len(number) == 16 and number[:2] in ["51", "52", "53", "54", "55"]:
        return True
    else:
        return False


# Check VISA
def checkvisa(number):
    # Check for card length and starting digits
    if len(number) in [13, 16] and number[0] == "4":
        return True
    else:
        return False


# Calculate checksum
def checksum(number):
    mult = 0
    not_mult = 0

    mult_list = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

    for i in range(len(number)):
        n = int(number[len(number) - 1 - i])
        if i % 2 == 0:
            not_mult += n
        else:
            mult += mult_list[n]

    total = not_mult + mult
    return (total % 10 == 0)


main()