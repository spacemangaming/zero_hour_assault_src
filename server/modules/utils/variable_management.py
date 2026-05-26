# variable conversion functions written by nbm studios. Intended to function the same as with BGT
import base64
import globals as g





def ascii_to_character(code):
    return chr(code)


def character_to_ascii(char):
    return ord(char)


def hex_to_string(hex):
    return string.decode("hex")


def number_to_hex_string(number):
    hex(number)


def string_base64_decode(string):
    try:
        string = string.encode()
    except:
        pass
    return base64.b64decode(string)


def string_base64_encode(string):
    try:
        string = string.encode()
    except:
        pass
    return base64.b64encode(string).decode()

def string_contains(the_string, the_search, occurrence):
    if isinstance(the_string, int):
        the_string = str(the_string)
        
    count = the_string.count(the_search)
    if count < occurrence:
        return -1
    else:
        pos = -1
        for i in range(occurrence):
            pos = the_string.find(the_search, pos + 1)
        return pos

def string_is_alphabetic(the_string):
    return the_string.isalpha()


def string_is_alphanumeric(the_string):
    return the_string.isalnum()

def string_compress(the_string):
    if not the_string:
        return ""

    compressed_string = ""
    count = 1
    prev_char = the_string[0]

    for i in range(1, len(the_string)):
        if the_string[i] == prev_char:
            count += 1
        else:
            compressed_string += prev_char + str(count)
            prev_char = the_string[i]
            count = 1

    compressed_string += prev_char + str(count)
    return compressed_string


def string_decompress(compressed_string):
    if not compressed_string:
        return ""

    decompressed_string = ""
    i = 0

    while i < len(compressed_string):
        char = compressed_string[i]
        count = int(compressed_string[i+1])
        decompressed_string += char * count
        i += 2

    return decompressed_string

def string_is_digits(the_string):
    return the_string.isdigit()


def string_is_lower_case(the_string):
    return the_string.islower()


def string_is_upper_case(the_string):
    return the_string.isupper()


def string_left(the_string, count):
    if count <= 0:
        return ""
    elif count > len(the_string):
        return the_string
    else:
        return the_string[0:count]


def string_len(the_string):
    return len(the_string)
def string_distance(first_string, second_string):
    distances = [[0 for j in range(len(second_string) + 1)] for i in range(len(first_string) + 1)]
    for i in range(len(first_string) + 1):
        distances[i][0] = i
    for j in range(len(second_string) + 1):
        distances[0][j] = j
    for i in range(1, len(first_string) + 1):
        for j in range(1, len(second_string) + 1):
            if first_string[i-1] == second_string[j-1]:
                distances[i][j] = distances[i-1][j-1]
            else:
                distances[i][j] = min(distances[i-1][j], distances[i][j-1], distances[i-1][j-1]) + 1
    return distances[-1][-1]

def string_mid(the_string, start_position, count):
    if count < 1:
        return ""
    elif count > len(the_string):
        return the_string[start_position:]
    elif start_position < 1:
        the_string = the_string[::-1]  # string is reversed
        return the_string[start_position:count]
    elif start_position > len(the_string):
        return ""
    else:
        return the_string[start_position:count]


def string_replace(the_string, the_search, replacement, replace_all):
    return the_string.replace(the_search, replacement, -1 if replace_all else 1)


def string_reverse(the_string):
    return the_string[::-1]


def string_right(the_string, count):
    if count > len(the_string):
        return ""
    else:
        return the_string[count:]


def string_split(the_string, the_delimiter, ahoooo):
    if the_delimiter == "\r\n":
        the_delimiter = "\n"
    return the_string.split(the_delimiter)


def string_to_hex(the_string):
    the_string = the_string.encode()
    return the_string.hex()


def string_to_lower_case(the_string):
    return the_string.lower()


def string_to_number(the_string):
    try:
        return int(the_string)
    except ValueError:
        return float(the_string)


def string_to_upper_case(the_string):
    return the_string.upper()


def string_trim_left(the_string, count):
    if count < 1:
        return the_string
    elif count > len(the_string):
        return ""
    else:
        return the_string[count : len(the_string)]


def string_trim_right(the_string, count):
    if count < 1:
        return the_string
    elif count > len(the_string):
        return ""
    else:
        return the_string[: len(the_string) - count]

