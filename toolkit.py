'''
Level 1 — A Record class (OOP begins)
Concept: classes, __init__, methods, @dataclass.
================================================
Instead of loose dictionaries, make a Record class — one object per person. First write it as a normal
class with __init__. Then rewrite it as a @dataclass and notice how much shorter it is. Give it a
method like is_valid() that returns True if the row has all its fields filled in.
Guidance: we tell you to make a Record class and a validity method. You decide what "valid" means and how the
method checks it. That decision is yours — that's the first bit of logic you derive.
'''

import csv

class Record:
    def __init__(self, id, name, age, city, score):
        self.id = id
        self.name = name
        self.age = age
        self.city = city
        self.score = score

    # testing code: if an object was created or not?
    def __repr__(self):
        return f"{type(self).__name__}(Id: {self.id}, Name: {self.name}, Age: {self.age}, City: {self.city}, Score: {self.score})"

    def is_valid(self):
        if self.id != "" and self.name != "" and self.age != "" and self.city != "" and self.score != "":
            return True
        return False


def main():
    file_path = "messy_people.csv"
    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        # row_list = []
        for row in reader:
            person = Record(row.get("id"), row.get("name"), row.get("age"), row.get("city"), row.get("score"))

            # test if the instances were created
            print(repr(person))
            print(f"Id: {person.id} is {person.is_valid()}")


if __name__ == '__main__':
    main()