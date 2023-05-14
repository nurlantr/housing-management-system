from typing import Dict, List
class Dormitory:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        # self.num_blocks = 2
        for block_idx in range(23, 28): #range(1, self.num_blocks + 1):
            for i in range(2, 13):
                if block_idx == 23 and i == 2: continue
                if block_idx == 24 and i == 2: continue
                for j in range(1, 29):
                    self.rooms[f"{block_idx}.{i*100 + j}"] = Room(f"{block_idx}.{i*100 + j}")

    def __str__(self):
        result = "Dormitory:\n"
        for i in self.rooms.values():
            result += f"{i}\n"

        return result

    def num_students(self):
        res = 0
        for room in self.rooms.values():
                res += len(room.students)

        return res
    def print_occupied_rooms(self):
        result = "Dormitory:\n"
        for room in self.rooms.values():
            if len(room.students) != 0:
                result += f"{room}\n"

        return result

    def get_rooms(self, begin, end, size = 0):
        rooms = []
        for room in self.rooms.values():
            if int(room.number[0:2]) in range(begin, end + 1):
                if len(room.students) == size:
                    rooms.append(room.number)
        
        return rooms

class Student:
    def __init__(self, id: str, gender: str, degree: str | None = None, year: str | None = None, intended_roomate_ids: List[str] | None = None):
        self.id = id
        self.gender = gender
        self.degree = degree
        self.year = year
        self.intended_roomate_ids = [] if intended_roomate_ids is None else intended_roomate_ids
        self.roomates: List[Student] = []
        self.room: Room | None = None

    def __str__(self):
        return  f"{self.id} " + self.gender + " " + str(self.intended_roomate_ids)

    def __repr__(self):
        return f" {self.id} " + self.gender + " " + str(self.intended_roomate_ids)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Student):
            return self.id == other.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)

class Room:
    def __init__(self, number: str, capacity: int = 2) -> None:
        self.number = number
        self.students: List[Student] = []
        self.capacity = capacity
        self.gender: str | None = None

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
    
    def deleteStudent(self, student: Student):
        student.room = None
        self.students.remove(student)
        self.capacity += 1
        
        student.roomates = []

        if len(self.students) == 0:
            self.gender = None
        