import csv
from dataclasses import dataclass


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


@dataclass
class Record:
    id: str
    name: str
    age: str
    city: str
    score: str

    # check if a row has all values with an exception of name
    def is_valid(self):
        fields = [self.id, self.age, self.city, self.score]
        for field in fields:
            if field == "" or field is None:
                return False
        return True


# apply age specific rules
def determine_age(str_age):
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


# main function for data cleaning operations
def clean_data(file):
    reader = csv.DictReader(file)
    for row in reader:
        age = determine_age(row.get("age"))
        person = Record(row.get("id"), row.get("name"), age, row.get("city"), row.get("score"))

        # skip an entire row if it doesn't have any value
        if not any(value and value.strip() for value in row.values()):
            continue

        # skip a row if even one field doesn't have value, except name
        if not person.is_valid():
            continue


def main():
    file_path = "messy_people.csv"
    with open(file_path, "r", newline="") as file:
        clean_data(file)


if __name__ == '__main__':
    main() 