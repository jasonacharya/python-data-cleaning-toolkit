map_singles = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "onehundred": 100,
}

map_tens = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}


# function to apply age specific rules
def determine_age(str_age: str) -> int | str:
    try:
        age = int(str_age)
        if age < 1 or age > 100:
            return ""
        else: 
            return age
    except ValueError:
        age = (str_age.lower()).replace(" ", "")
        new_age = age.replace("-", "")

        if map_singles.get(new_age):
            return map_singles.get(new_age)
        
        elif map_tens.get(new_age):
            return map_tens.get(new_age)
        
        else:
            for key in map_tens:
                check = new_age.startswith(key) # returns True

                if check: # if True:
                    strip_first = new_age.removeprefix(key)

                    if map_singles.get(strip_first):
                        second_digit = map_singles.get(strip_first)
                        first_digit = map_tens.get(key)
                        return first_digit + second_digit
            return ""