import csv

file_path = "messy_people.csv"

with open(file_path, "r", newline="") as file:
    reader = csv.DictReader(file)

    row_list = []
    for row in reader:
        row_list.append(row)
    # print(row_list)
    print(len(row_list))
    print(row_list[:3])
            