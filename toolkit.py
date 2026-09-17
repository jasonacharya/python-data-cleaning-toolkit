import csv, time
from functools import wraps
from dataclasses import dataclass
from collections.abc import Iterator



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
    age: int
    city: str
    score: str

    # check if a row has all values with an exception of name
    def is_valid(self):
        fields = [self.id, self.age, self.city, self.score]
        for field in fields:
            if field == "" or field is None:
                return False
        return True


# logtime decorator
def log_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        print(f"Elapsed time is: {elapsed_time} seconds")
        return result
    
    return wrapper


@dataclass
class Dataset:
    filepath: str
    records: list[Record]

    # generator function for data cleaning operations
    def clean_data(self: Dataset) -> Iterator[Record]:
        with open(self.filepath, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # skip an entire row if it doesn't have any value
                if not any(value and value.strip() for value in row.values()):
                    continue
    
                age = determine_age(row.get("age"))
                person = Record(row.get("id"), row.get("name"), age, row.get("city"), row.get("score"))
    
                # skip a row if even one field doesn't have value, except name
                if not person.is_valid():
                    continue

                yield person


    # consumer function to handle duplicate ids
    def handle_id(self: Dataset) -> list[Record]:
        duplicate_id ={}

        for current_record in self.clean_data():
            if current_record.id in duplicate_id:
                duplicate_id[current_record.id].append(current_record)
            else:
                duplicate_id[current_record.id] = [current_record]

        final_records = []
        for key, value in duplicate_id.items():
            num_of_val = len(value)

            if num_of_val > 1:
                first_record = value[0]

                if all(record == first_record for record in value):
                    final_records.append(first_record)
                # otherwise conflicting ID -> append nothing
            else: 
                final_records.append(value[0])
        self.records = final_records
        return self.records


    # def average_score(self) -> float:
    #     score_data = self.records
    #     hold_records = []

    #     for record in score_data:
    #         hold_records.append(float(record.score))

    #     num_record = len(hold_records)
    #     average = sum(hold_records)/num_record
    #     return average

    @log_time
    def average_score(self: Dataset) -> float | None:
        total_score = 0
        count = 0
        score_data = self.records

        for record in score_data:
            total_score += float(record.score)
            count += 1
        if count == 0:
            return None

        average = total_score/count
        return average

    @log_time
    def oldest_person(self: Dataset) -> Record | None:
        if self.records == []:
            return None

        oldest = self.records[0]
        for record in self.records:
            if record.age > oldest.age:
                oldest = record
        return oldest

    @log_time
    def youngest_person(self: Dataset) -> Record | None:
        if self.records == []:
            return None

        youngest = self.records[0]
        for record in self.records:
            if record.age < youngest.age:
                youngest = record
        return youngest
    
    @log_time
    def people_per_city(self: Dataset) -> dict[str, int]:
        count_city = {}
        for record in self.records:
            if record.city not in count_city:
                count_city[record.city] = 1
            else:
                count_city[record.city] += 1
        return count_city


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


def main() -> None:
    file_path = "messy_people.csv"
    record_list = []

    dataset = Dataset(file_path, record_list)
    dataset.handle_id()
    final_records = dataset.records

    average = dataset.average_score()
    oldest = dataset.oldest_person()
    youngest = dataset.youngest_person()
    p_per_city = dataset.people_per_city()
    print(f"Average Score: {average:.5f}")
    print(f"Oldest age: {oldest}")
    print(f"Youngest age: {youngest}")
    print(f"People per city: {p_per_city}")
    print(dataset.average_score.__name__)
    print(dataset.oldest_person.__name__)
    print(dataset.youngest_person.__name__)
    print(dataset.people_per_city.__name__)

    # for record in final_records:
    #     print(record)

    print("Final Count: ", len(final_records))

if __name__ == '__main__':
    main() 