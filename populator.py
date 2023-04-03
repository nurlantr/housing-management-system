from typing import List, Dict
from student import Student
from random import randint
from dormitory import Dormitory
from random import shuffle
import os
import heapq
class Populator:
    def __init__(self, input_name, dorm : Dormitory):
        self.dorm = dorm
        self.students: Dict[str, Student] = {}
        self.read(input_name)

    def read(self, input_name):
        with open(input_name) as f:
            line = f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip(',\n ').split(',')
                self.students[line[0]] = Student(line[0], line[1], line[2], line[3], line[4], line[5:])
                

    def match(self, A: Student, B: Student, roomate_num: int):
        roomate_is_free = (len(B.roomates) == 0)
        roomate_has_roomate_num = (len(B.roomate_ids) == roomate_num)
        
        if roomate_is_free and roomate_has_roomate_num:
            id_match = (B.roomate_ids.count(A.id) == 1) and (A.roomate_ids.count(B.id) == 1)
            gender_match = (B.gender == A.gender)
            
            # ------------------
            # Degree year match!
            # ------------------          

            if id_match and gender_match:
                return True
            else:
                return False

    def pair(self):
        for student in self.students.values():
            if len(student.roomates) != 0: continue
            
            if len(student.roomate_ids) == 1 and (student.roomate_ids[0] in self.students) and (student.id != student.roomate_ids[0]):
                intended_roomate = self.students[student.roomate_ids[0]]

                if self.match(student, intended_roomate, 1):
                    student.roomates.append(intended_roomate)
                    intended_roomate.roomates.append(student)

            elif len(student.roomate_ids) == 2 and (student.roomate_ids[0] in self.students) and (student.roomate_ids[1] in self.students) and len({student.id, student.roomate_ids[0], student.roomate_ids[1]}) == 3:
                intended_roomate1 = self.students[student.roomate_ids[0]]
                intended_roomate2 = self.students[student.roomate_ids[1]]
                if self.match(student, intended_roomate1, 2) and self.match(student,intended_roomate2, 2) and self.match(intended_roomate1, intended_roomate2, 2):
                    student.roomates.extend([intended_roomate1, intended_roomate2])
                    intended_roomate1.roomates.extend([intended_roomate2, student])
                    intended_roomate2.roomates.extend([intended_roomate1, student])
            
            elif (len(student.roomate_ids) == 3 and 
                  (student.roomate_ids[0] in self.students) and 
                  (student.roomate_ids[1] in self.students) and
                  (student.roomate_ids[2] in self.students) and
                  len({student.id, student.roomate_ids[0], student.roomate_ids[1], student.roomate_ids[2]}) == 4
                  ):
                intended_roomate1 = self.students[student.roomate_ids[0]]
                intended_roomate2 = self.students[student.roomate_ids[1]]
                intended_roomate3 = self.students[student.roomate_ids[2]]
                if (self.match(student, intended_roomate1, 3) and 
                    self.match(student,intended_roomate2, 3) and 
                    self.match(student,intended_roomate3, 3) and 
                    self.match(intended_roomate1, intended_roomate2, 3) and
                    self.match(intended_roomate1, intended_roomate3, 3) and
                    self.match(intended_roomate2, intended_roomate3, 3)
                    ):
                    student.roomates.extend([intended_roomate1, intended_roomate2, intended_roomate3])
                    intended_roomate1.roomates.extend([intended_roomate2, intended_roomate3, student])
                    intended_roomate2.roomates.extend([intended_roomate1, intended_roomate3, student])
                    intended_roomate3.roomates.extend([intended_roomate1, intended_roomate2, student])
                    
            if len(student.roomates) == 0:
                self.selfdestruction(student)

    def selfdestruction(self, dummy):
        if len(dummy.roomate_ids) == 0:
            return
        
        ls = dummy.roomate_ids.copy()
        dummy.roomate_ids = []

        for dummy_ids in ls:
            dummy_friend = self.students.get(dummy_ids)
            if dummy_friend != None and len(dummy_friend.roomate_ids) != 0 and dummy_friend.roomate_ids.count(dummy.id) > 0:
                self.selfdestruction(dummy_friend)

    def populate_old(self, students_list: List[int], rooms_list: List[int]):
        students_list.sort(key = lambda id: len(self.students[id].roomates), reverse = True)
        
        shuffle(rooms_list)

        def run(gender: str):
            room_heap = [(-self.dorm.rooms[rooms_list[i]].capacity, self.dorm.rooms[rooms_list[i]].number[0:2], i, self.dorm.rooms[rooms_list[i]]) for i in range(len(rooms_list))]
            heapq.heapify(room_heap)
            
            # Run for guys
            i = 0 # stud_idx
            

            while i < len(students_list) and len(room_heap):
                student = self.students[students_list[i]]
                _, _, idx, room = heapq.heappop(room_heap)

                if(student.gender != gender or 
                    student.room or 
                    len(student.roomates) + 1 > room.capacity):
                    heapq.heappush(room_heap, (-room.capacity, room.number[0:2], idx, room))
                    i += 1
                    continue

                if room.gender and room.gender != gender:
                    continue

                room.addStudent(student)
                
                for roomate in student.roomates:
                    room.addStudent(roomate)

                if room.capacity > 0:
                    heapq.heappush(room_heap, (-room.capacity, room.number[0:2], idx, room))
                
                i += 1
        
        run("Male")
        run("Female")
        print(rooms_list)
        for id in rooms_list:
            room = self.dorm.rooms[id]
            for habitant in room.students:
                st = set(room.students)
                st.discard(habitant)
                habitant.roomates = list(st)

    def populate(self, students_list: List[int], rooms_list: List[int]):
        shuffle(rooms_list)
        
        self.populate_gender([male_id for male_id in students_list if self.students[male_id].gender == 'Male'], rooms_list)
        self.populate_gender([female_id for female_id in students_list if self.students[female_id].gender == 'Female'], rooms_list)

        for room_num in rooms_list:
            room = self.dorm.rooms[room_num]
            for habitant in room.students:
                st = set(room.students)
                st.discard(habitant)
                habitant.roomates = list(st)
        
        not_accommodated = []
        for student_id in students_list:
            student = self.students[student_id]
            if student.room is None:
                not_accommodated.append(student_id)
        print("Were not accommodated:", not_accommodated)

    def populate_gender(self, students_list: List[int], rooms_list: List[int]):
        students_list.sort(key = lambda id: len(self.students[id].roomates), reverse = True)
        
        for student_id in students_list:
            student = self.students[student_id]
            
            if student.room is not None: continue

            group_len = len(student.roomates) + 1

            best_room = None
            for room_num in rooms_list:
                room = self.dorm.rooms[room_num]
                
                if room.gender is not None and room.gender != student.gender: continue

                if room.capacity >= group_len and (best_room is None or room.capacity < best_room.capacity):
                    best_room = room
                
            if best_room is not None:
                best_room.addStudent(student)
            
                for roomate in student.roomates:
                    best_room.addStudent(roomate)

    def to_csv(self, file_name: str):
        output_path = "output"
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        path = os.path.join(output_path, file_name)
        
        f = open(path, "w")
        f.write("id,name,block,room,place\n")
        for room in self.dorm.rooms.values():
            for i in range(len(room.students)):
                s = room.students[i]
                f.write(f"{s.id},{s.name},{room.number[0:2]},{room.number[2:]},{i+1}\n")
        f.close()
    
        

            
                    

                
                


            



        



        

            

            




            

            












