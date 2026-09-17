from dataclasses import dataclass

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