import csv
from dataclasses import dataclass
from record import Record
from collections.abc import Iterator
from clean_age import determine_age
from utils import log_time

@dataclass
class Dataset:
    filepath: str
    records: list[Record]
    reasons: dict[str, int]


    # generator function for data cleaning operations
    def clean_data(self: Dataset) -> Iterator[Record]:
        with open(self.filepath, "r", newline="") as file:

            self.rows_loaded = 0
            self.rows_dropped = 0
            self.reasons = {
                "blank_row": 0,
                "invalid_required_data": 0,
                "exact_duplicate": 0,
                "conflicting_id": 0,
            }

            reader = csv.DictReader(file)

            for row in reader:
                self.rows_loaded += 1
                # skip an entire row if it doesn't have any value
                if not any(value and value.strip() for value in row.values()):
                    self.rows_dropped += 1
                    self.reasons["blank_row"] += 1
                    continue
    
                age = determine_age(row.get("age"))
                person = Record(row.get("id"), row.get("name"), age, row.get("city"), row.get("score"))
    
                # skip a row if even one field doesn't have value, except name
                if not person.is_valid():
                    self.rows_dropped += 1
                    self.reasons["invalid_required_data"] += 1
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
                    self.rows_dropped += len(value) - 1
                    self.reasons["exact_duplicate"] += len(value) - 1 
                else:
                    self.rows_dropped += len(value)
                    self.reasons["conflicting_id"] += len(value)
                # otherwise conflicting ID -> append nothing

            else: 
                final_records.append(value[0])

        self.records = final_records
        return self.records


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


    def summary_report(self):
        average = self.average_score()
        oldest = self.oldest_person()
        youngest = self.youngest_person()
        city_counts = self.people_per_city()

        summary = {
            "rows_loaded": self.rows_loaded,
            "rows_dropped": self.rows_dropped,
            "reasons": self.reasons,
            "key_stats": {
                "average_score": average,
                "oldest_person": oldest,
                "youngest_person": youngest,
                "people_per_city": city_counts,
            }
        }
        return summary
    
    def save_report(self, summary):
        with open("report-summary.txt", "w") as file:
            file.write("================= DATASET SUMMARY REPORT =================\n")
            file.write("----------------------------------------------------------\n")

            file.write(f"Rows loaded: {summary['rows_loaded']}\n")
            file.write(f"Rows dropped: {summary['rows_dropped']}\n")
            file.write(f"Final cleaned records: {len(self.records)}\n")

            file.write("\nReasons dropped (where each row was dropped):\n")
            file.write("---------------------------------------------\n")

            for reason, count in summary["reasons"].items():
                file.write(f"  {reason}: {count}\n")

            file.write("\nKey Statistics:\n")
            file.write("----------------\n")
            file.write(f"  Average score: {summary['key_stats']['average_score']}\n")
            file.write(f"  Oldest person: {summary['key_stats']['oldest_person']}\n")
            file.write(f"  Youngest person: {summary['key_stats']['youngest_person']}\n")

            file.write("\nPeople per city:\n")
            file.write("----------------\n")
            for city, count in summary["key_stats"]["people_per_city"].items():
                file.write(f"  {city}: {count}\n")
            file.write("\n====================== END OF SUMMARY ======================\n")