from student import Student
from random import randint
class Populator:
    def __init__(self, file, dorm):
        self.dorm = dorm
        self.students = {}
        self.read(file)
        self.pair()
        self.populate()

    def read(self, file):
        with open(file) as f:
            line = f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().split(',')
                line = [st.strip() for st in line]
                if len(line) == 7:
                    self.students[line[0]] = Student(line[0], line[1], line[2], line[3], line[4], [line[5], line[6]])
                elif len(line) == 6:
                    self.students[line[0]] = Student(line[0], line[1], line[2], line[3], line[4], [line[5]])
                else:
                    self.students[line[0]] = Student(line[0], line[1], line[2], line[3], line[4], [])

    def pair(self):
        for student in self.students.values():
            if len(student.roomate_ids) == 1:
                intended_roomate = self.students.get(student.roomate_ids[0])
                if intended_roomate == None:
                    self.selfdestruction(student)
                    continue
                roomate_is_free = len(intended_roomate.students)
                if len(intended_roomate.roomate_ids) == 1:
                    different_id = (intended_roomate.id != student.id)
                    id_match = (intended_roomate.roomate_ids[0] == student.id)
                    gender_match = (intended_roomate.gender == student.gender)
                    
                    if different_id and id_match and gender_match:
                        student.students.append(intended_roomate)
                        intended_roomate.append(student)

                else:
                    self.selfdestruction(student)






    def selfdestruction(self, dummy):
        if len(dummy.roomate_ids) == 0:
            return
        
        ls = dummy.roomate_ids.copy()
        dummy.roomate_ids = []

        for dummy_ids in ls:
            dummy_friend = self.students.get(dummy_ids)
            if dummy_friend != None and len(dummy_friend.roomate_ids) != 0:
                selfdestruction(dummy_friend)

    def pair1(self):
        for student in self.students.values():
            intended_roomate = self.students.get(student.roomate_id)
            roomate_isnt_assigned = (student.roomate == None)
            has_roomate_id = (student.roomate_id != None)
            id_exists = (intended_roomate != None)

            if has_roomate_id and roomate_isnt_assigned and id_exists:
                intended_roomate_is_free = (intended_roomate.roomate == None)
                id_match = (intended_roomate.roomate_id != None and intended_roomate.roomate_id == student.id)
                gender_match = (intended_roomate.gender == student.gender)

                if intended_roomate_is_free and id_match and gender_match:
                    student.roomate = intended_roomate
                    intended_roomate.roomate = student
            
            if student.roomate == None:
                student.roomate_id = None

    def populate(self):
        used_rooms = set()
        pending_rooms = []
        for student in self.students.values():
            if student.room == None:
                if student.roomate != None:
                    self.assign(student, used_rooms)
                else:
                    if (len(pending_rooms) != 0  and pending_rooms[0].gender == student.gender) or (len(pending_rooms) == 2 and pending_rooms[1].gender == student.gender):
                        if pending_rooms[0].gender == student.gender:
                            room = pending_rooms[0]
                            del pending_rooms[0]
                        else:
                            room = pending_rooms[1]
                            del pending_rooms[1]

                        room.students[0].roomate = student
                        student.roomate = room.students[0]
                        room.students.append(student)
                        room.students[0].room = room.students[1].room = room
                        room.students[0].roomate_id, room.students[1].roomate_id = room.students[1].id, room.students[0].id
                    else:
                        pending_rooms.append(self.assign(student, used_rooms))


    def assign(self, student, used_rooms):
        while True:
            block_num = randint(1, self.dorm.num_blocks)
            room_num = 100 * randint(2, 12) + randint(1, 28)
            
            if (block_num, room_num) not in used_rooms:
                room = self.dorm.blocks[block_num].rooms[room_num]
                student.room = room
                room.students.append(student)
                room.gender = student.gender

                if student.roomate != None:
                    student.roomate.room = room
                    room.students.append(student.roomate)
                
                used_rooms.add((block_num, room_num))
                return room

    def to_csv(self):
        f = open("output.csv", "w")
        f.write("id,name,block,room,place\n")
        for block in self.dorm.blocks.values():
            for room in block.rooms.values():
                for i in range(len(room.students)):
                    s = room.students[i]
                    f.write(f"{s.id},{s.name},{s.room.block},{s.room.room_number},{i+1}\n")