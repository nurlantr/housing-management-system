# from sqlalchemy import Column, Integer, String, ForeignKey, Table
# from sqlalchemy.orm import relationship
# from database import Base
# import pandas as pd
# from database import SessionLocal
# from associations import roommates_association_table

# class Dormitory(Base):
#     __tablename__ = "dormitories"

#     id = Column(Integer, primary_key=True, index=True)
#     blocks = relationship("Block", back_populates="dormitory")

#     def __init__(self, blocks: dict[int, 'Block'] = None, excluded_rooms_file: str | None = None) -> None:
#         self.rooms = {}
#         self.blocks = blocks if blocks is not None else {}

#         self.excluded_rooms = set()
#         if excluded_rooms_file is not None:
#             df = pd.read_excel(excluded_rooms_file)
#             self.excluded_rooms = set(df.iloc[:, 0].astype(str) + '.' + df.iloc[:, 1].astype(str))

#         for block in self.blocks.values():
#             self.rooms[block.number] = {}
#             for room in block.room_list:
#                 if f"{block.number}.{room}" in self.excluded_rooms:
#                     continue
#                 self.rooms[block.number][room] = Room(room, block.number, block.room_capacity)

#     def __str__(self):
#         result = "Dormitory:\n"
#         indent = "    "
#         for block in self.rooms:
#             result += f"Block {block}:\n"
#             for room in self.rooms[block].values():
#                 result += indent + f"{room}\n"
#         return result

# class Block(Base):
#     __tablename__ = "blocks"

#     id = Column(Integer, primary_key=True, index=True)
#     number = Column(Integer, unique=True)
#     room_list = Column(String)  # this will store room numbers as comma-separated values
#     room_capacity = Column(Integer)
#     dormitory_id = Column(Integer, ForeignKey("dormitories.id"))
#     dormitory = relationship("Dormitory", back_populates="blocks")
#     rooms = relationship("Room", back_populates="block")

#     def __init__(self, number: int, room_list: list[int], room_capacity: int):
#         self.number = number
#         self.room_list = ",".join(map(str, sorted(room_list)))
#         self.room_capacity = room_capacity

# class Room(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True, index=True)
#     number = Column(Integer)
#     block_number = Column(Integer, ForeignKey("blocks.id"))
#     capacity = Column(Integer, default=2)
#     gender = Column(String, nullable=True)
#     block = relationship("Block", back_populates="rooms")
#     students = relationship("Student", back_populates="room")

#     def __init__(self, number: int, block_number: int, capacity: int = 2):
#         self.number = number
#         self.block_number = block_number
#         self.capacity = capacity
#         self.students = []
#         self.gender = None

#     def __str__(self) -> str:
#         return f"Room {self.block_number}.{self.number} {self.gender}: {self.students}"

#     def __repr__(self) -> str:
#         return f"Room {self.block_number}.{self.number} {self.gender}: {self.students}"

#     def addStudent(self, new_student: 'Student'):
#         with SessionLocal() as session:
#             if self.capacity == 0:
#                 raise ValueError(f"Room {self.block_number}.{self.number} is full")
#             if new_student in self.students:
#                 raise ValueError(f"Student {new_student.id} is already in room {self.block_number}.{self.number}")
#             if self.gender is not None and self.gender != new_student.gender:
#                 raise ValueError(f"Student {new_student.id} has gender {new_student.gender} and it doesn't match Room {self.block_number}.{self.number} gender {self.gender}")

#             if self.gender is None:
#                 self.gender = new_student.gender

#             for habitat in self.students:
#                 habitat.roommates.append(new_student)
#                 new_student.roommates.append(habitat)

#             new_student.room = self
#             self.students.append(new_student)
#             self.capacity -= 1

#             session.add(new_student)
#             session.commit()

#             print(f"{self.block_number}.{self.number}:\n    Added Student {new_student.id}")

#     def deleteStudent(self, delete_student: 'Student'):
#         with SessionLocal() as session:
#             delete_student.room = None

#             try:
#                 self.students.remove(delete_student)
#             except ValueError:
#                 raise ValueError(f"Student {delete_student.id} is not in room {self.block_number}.{self.number}")

#             self.capacity += 1

#             for habitat in self.students:
#                 if delete_student in habitat.roommates:
#                     habitat.roommates.remove(delete_student)
#                 if habitat in delete_student.roommates:
#                     delete_student.roommates.remove(habitat)

#             if len(self.students) == 0:
#                 self.gender = None

#             session.delete(delete_student)
#             session.commit()

# class Student(Base):
#     __tablename__ = "students"

#     id = Column(Integer, primary_key=True, index=True)
#     gender = Column(String)
#     degree = Column(String, nullable=True)
#     year = Column(String, nullable=True)
#     intended_roommate_ids = Column(String, nullable=True)
#     room_id = Column(Integer, ForeignKey("rooms.id"))
#     room = relationship("Room", back_populates="students")
#     roommates = relationship("Student",
#                              secondary=roommates_association_table,
#                              primaryjoin="Student.id==roommates_association_table.c.student_id",
#                              secondaryjoin="Student.id==roommates_association_table.c.roommate_id",
#                              backref="roommates_back")

#     def __init__(self, id: int, gender: str, degree: str | None = None, year: str | None = None, intended_roommate_ids: list[int] | None = None):
#         self.id = id
#         self.gender = gender
#         self.degree = degree
#         self.year = year
#         self.intended_roommate_ids = [] if intended_roommate_ids is None else ",".join(map(str, intended_roommate_ids))
#         self.roommates = []
#         self.room = None

#     def __str__(self) -> str:
#         return f"Student {self.id} {self.gender} {[roomate.id for roomate in self.roommates]}"

#     def __repr__(self) -> str:
#         return f"Student {self.id} {self.gender} {[roomate.id for roomate in self.roommates]}"

#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, Student):
#             return self.id == other.id
#         else:
#             return False

#     def __hash__(self) -> int:
#         return hash(self.id)

#2
# from sqlalchemy import Column, Integer, String, ForeignKey, Table
# from sqlalchemy.orm import relationship
# from database import Base
# import pandas as pd
# from database import SessionLocal

# roommates_association_table = Table(
#     'roommates_association',
#     Base.metadata,
#     Column('student_id', Integer, ForeignKey('students.id')),
#     Column('roommate_id', Integer, ForeignKey('students.id'))
# )

# class Dormitory(Base):
#     __tablename__ = "dormitories"

#     id = Column(Integer, primary_key=True, index=True)
#     blocks = relationship("Block", back_populates="dormitory")

# class Block(Base):
#     __tablename__ = "blocks"

#     id = Column(Integer, primary_key=True, index=True)
#     number = Column(Integer, unique=True)
#     room_list = Column(String)  # this will store room numbers as comma-separated values
#     room_capacity = Column(Integer)
#     dormitory_id = Column(Integer, ForeignKey("dormitories.id"))
#     dormitory = relationship("Dormitory", back_populates="blocks")
#     rooms = relationship("Room", back_populates="block")

# class Room(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True, index=True)
#     number = Column(Integer)
#     block_number = Column(Integer, ForeignKey("blocks.id"))
#     capacity = Column(Integer, default=2)
#     gender = Column(String, nullable=True)
#     block = relationship("Block", back_populates="rooms")
#     students = relationship("Student", back_populates="room")

# class Student(Base):
#     __tablename__ = "students"

#     id = Column(Integer, primary_key=True, index=True)
#     gender = Column(String)
#     degree = Column(String, nullable=True)
#     year = Column(String, nullable=True)
#     intended_roommate_ids = Column(String, nullable=True)
#     room_id = Column(Integer, ForeignKey("rooms.id"))
#     room = relationship("Room", back_populates="students")
#     roommates = relationship("Student",
#                              secondary=roommates_association_table,
#                              primaryjoin="Student.id==roommates_association_table.c.student_id",
#                              secondaryjoin="Student.id==roommates_association_table.c.roommate_id",
#                              back_populates="roommates_back")

import pandas as pd

class Dormitory:
    class Block:
        def __init__(self, number: int, room_list: list[int], room_capacity: int):
            self.number = number
            self.room_list = sorted(room_list)
            self.room_capacity = room_capacity
        
    def __init__(self, blocks: dict[int, Block], excluded_rooms_file: str | None = None) -> None:
        self.rooms: dict[int, dict[int, Room]] = {} 
        self.blocks = blocks
        
        self.excluded_rooms = set()
        if excluded_rooms_file is not None:
            df = pd.read_excel(excluded_rooms_file) # header: Block, Room
            self.excluded_rooms = set(df.iloc[:,0].astype(str) + '.' + df.iloc[:,1].astype(str)) #23.909 ex.

        for block in self.blocks.values():
            self.rooms[block.number] = {}  # для каждого №блока создаем пустую мапу (dict[int, Room])
            for room in block.room_list: # итерация по списку комнат в текущем блоке
                if f"{block.number}.{room}" in self.excluded_rooms:
                    continue
                self.rooms[block.number][room] = Room(room, block.number, block.room_capacity)
                # создание объекта Room для каждой комнаты, и сохранение его в словаре.

    def __str__(self):
        result = "Dormitory:\n"
        indent = "    "
        for block in self.rooms:
            result += f"Block {block}:\n"
            for room in self.rooms[block].values():
                result += indent + f"{room}\n"
        
        return result

class Room:
    def __init__(self, number: int, block_number: int, capacity: int = 2):
        self.number = number
        self.block_number = block_number
        self.capacity = capacity
        self.students: list[Student] = []  # пустой список оккупантов комнаты
        self.gender: str | None = None    

    def __str__(self) -> str:
        return f"Room {self.block_number}.{self.number} {self.gender}: {self.students}"
    
    def __repr__(self) -> str:
        return f"Room {self.block_number}.{self.number} {self.gender}: {self.students}"
    
    def addStudent(self, new_student: 'Student'): #ожидается объект этого класса,но сам класс может быть определен позже в коде, "forward declaration".
        if self.capacity == 0:
            raise ValueError(f"Room {self.block_number}.{self.number} is full")
        if new_student in self.students:
            # raise ValueError(f"Student {new_student.id} is already in room {self.block_number}.{self.number}")
            print(f"Student {new_student.id} is already in room {self.block_number}.{self.number}")
            return
        if self.gender is not None and self.gender != new_student.gender:
            raise ValueError(f"Student {new_student.id} has gender {new_student.gender} and it doesn't match Room {self.block_number}.{self.number} gender {self.gender}")
        
        if self.gender is None:
            self.gender = new_student.gender
        
        for habitat in self.students:
            habitat.roommates.append(new_student)
            new_student.roommates.append(habitat)
    
        new_student.room = self  # означает, что студент теперь проживает в этой комнате
        self.students.append(new_student) #Новый студент добавляется в список self.students, который содержит всех студентов этой комнаты
        self.capacity -= 1

        print(f"{self.block_number}.{self.number}:\n    Added Student {new_student.id}")

    def deleteStudent(self, delete_student: 'Student'):
        delete_student.room = None  # студент больше не проживает в этой комнате
        
        try:
            self.students.remove(delete_student)
        except ValueError:
            raise ValueError(f"Student {delete_student.id} is not in room {self.block_number}.{self.number}")
        
        self.capacity += 1

        for habitat in self.students:
            if delete_student in habitat.roommates:
                habitat.roommates.remove(delete_student)
            if habitat in delete_student.roommates:
                delete_student.roommates.remove(habitat)

        if len(self.students) == 0:
            self.gender = None

class Student:
    def __init__(self, id: int, gender: str, degree: str | None = None, year: str | None = None, intended_roommate_ids: list[int] | None = None):
        self.id = id
        self.gender = gender
        self.degree = degree
        self.year = year
        self.intended_roommate_ids = [] if intended_roommate_ids is None else intended_roommate_ids
        self.roommates: list[Student] = []
        self.room: Room | None = None
    
    def __str__(self) -> str:
        return f"Student {self.id} {self.gender} {[roomate.id for roomate in self.roommates]}"
    
    def __repr__(self) -> str:
        return f"Student {self.id} {self.gender} {[roomate.id for roomate in self.roommates]}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Student):
            return self.id == other.id
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self.id)
    