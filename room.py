from student import Student
from typing import List
class Room:

    def __init__(self, number: int, capacity: int = 3) -> None:
        self.number = number
        self.students: List[Student] = []
        self.capacity = capacity
        self.gender: str = None

    def __str__(self) -> str:
        return f"Room {self.number} {self.gender}: {self.students}"

    def __repr__(self) -> str:
        return f"Room {self.number} {self.gender}: {self.students}"

    def addStudent(self, newStudent: Student):
        print(f"Successfully added student {newStudent.id} into room {self.number}")
        if self.gender is None:
            self.gender = newStudent.gender
        
        newStudent.room = self
        self.students.append(newStudent)


        self.capacity -= 1


