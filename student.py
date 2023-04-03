from typing import List
class Student:
    def __init__(self, id: str, name: str, gender: str, degree: int, year: str, roomate_ids: List[str]):
        self.id = id
        self.name = name
        self.gender = gender
        self.degree = degree
        self.year = year
        self.roomate_ids = roomate_ids
        self.roomates: List[Student] = []
        self.room: Room = None

    def __str__(self):
        return  f"{self.id} {self.name} " + self.gender + " " + str(self.roomate_ids)

    def __repr__(self):
        return f" {self.id} {self.name} " + self.gender + " " + str(self.roomate_ids)

    
    def __eq__(self, other: 'Student') -> bool:
        if isinstance(other, Student):
            return self.id == other.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)
        