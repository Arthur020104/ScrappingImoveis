#property code example: 0004-0101-0912-0003-9001
# this code is divided into 5 parts, each only four is relevant to the search, so the code is divided into 4 parts
def primeira_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num):
    # Adding numbers to change property code relative to range, 
    numbers_list.extend([mix + i for i in range(range_num)])
    # Formatting the numbers by adding a fixed pattern and converting them to strings
    formatted_numbers.extend([fixed_pattern + str(number) for number in numbers_list])

def segunda_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num):
    # Adding a fixed number (10000) to the mix for each number in the range
    numbers_list.extend([mix + (10000*i) for i in range(range_num)])
    # Formatting the numbers by adding a fixed pattern and converting them to strings
    formatted_numbers.extend([fixed_pattern + str(number) for number in numbers_list])

def terceira_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num):
    # Adding a fixed number (10000000000) to the mix for each number in the range
    numbers_list.extend([mix + (10000000000*i) for i in range(range_num)])
    # Formatting the numbers by adding a fixed pattern and converting them to strings
    formatted_numbers.extend([fixed_pattern + str(number) for number in numbers_list])

def quarta_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num):
    # Adding a fixed number (1000000000000) to the mix for each number in the range
    numbers_list.extend([mix + (1000000000000 * i) for i in range(range_num)])
    # Formatting the numbers by adding a fixed pattern and converting them to strings
    formatted_numbers.extend([fixed_pattern + str(number) for number in numbers_list])
