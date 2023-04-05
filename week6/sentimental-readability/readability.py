from cs50 import get_string


def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = (letters / words) * 100
    S = (sentences / words) * 100
    
    # Coleman-Liau index
    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


# Count Letters
def count_letters(text):
    count = 0
    for i in range(len(text)):
        if (not text[i] in ["!", ",", "'", "?", ".", " "]):
            count += 1
    return count


# Count Words
def count_words(text):
    count = 0
    for i in range(len(text)):
        if (text[i] in [" "]):
            count += 1
    return count + 1


# Count Sentences
def count_sentences(text):
    count = 0
    for i in range(len(text)):
        if (text[i] in ["!", "?", "."]):
            count += 1
    return count


main()