import csv
from dataclasses import dataclass

@dataclass
class Record:
    id: str
    name: str
    age: str
    city: str
    score: str

    def is_valid(self):
        fields = [self.id, self.name, self.age, self.city, self.score]
        for field in fields:
            if field == "" or field is None:
                return False
        return True


def main():
    file_path = "messy_people.csv"
    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            person = Record(row.get("id"), row.get("name"), row.get("age"), row.get("city"), row.get("score"))

            # test if the instances were created
            print(repr(person))
            print(f"Id: {person.id} is {person.is_valid()}")


if __name__ == '__main__':
    main()