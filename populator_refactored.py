from models_refactored import *
class Populator:
    def __init__(self, dorm: Dormitory):
        self.dorm = dorm
        self.students: dict[int, Student] = {}
    
    def update_dorm(self, dorm_input_file: str):
        df = pd.read_excel(dorm_input_file) # Header: Block, Room, ID, Gender
        if df.shape[1] != 6:
            raise ValueError(f'Number of columns should be 6')
        
        df.columns = ['Block', 'Room', 'Id', 'Gender', 'Degree', 'Year']
        if df.isnull().sum().sum() > 0:
            raise ValueError(f'Following rows contain null values {df[df.isnull().any(axis=1)].index.tolist()}')
        # -------------------------------------
        # More Data Transformations (if needed)
        # -------------------------------------
        df.Block = df.Block.astype(int)
        df.Room = df.Room.astype(int)
        df.Id = df.Id.astype(int)

        for _, row in df.iterrows():
            new_student = Student(row['Id'], row['Gender'], row['Degree'], row['Year'])
            self.students[new_student.id] = new_student
            self.dorm.rooms[row['Block']][row['Room']].addStudent(new_student)
    
    def read_students_to_accommodate(self, students_input_file: str):
        df = pd.read_excel(students_input_file)
        if df.shape[1] != 7:
            raise ValueError(f'Number of columns should be 7')
        df.columns = ['Id', 'Gender', 'Degree', 'Year', 'Roommate1', 'Roommate2', 'Roommate3']
        if df[['Id', 'Gender', 'Degree', 'Year']].isnull().sum().sum() > 0:
            raise ValueError(f'Following rows contain null values {df[df[["Id", "Gender", "Degree", "Year"]].isnull().any(axis=1)].index.tolist()}')
        # -------------------------------------
        # More Data Transformations (if needed)
        # -------------------------------------
        df.Id = df.Id.astype(int)
        df.Roommate1 = df.Roommate1.astype(int)
        df.Roommate2 = df.Roommate2.astype(int)
        df.Roommate3 = df.Roommate3.astype(int)

        student_ids_with_rooms = []
        student_ids_to_accommodate = []
        for _, row in df.iterrows():
            id = row['Id']
            gender = row['Gender']
            degree = row['Degree']
            year = row['Year']
            roommates = []
            for i in range(1, 4):
                if not pd.isna(row[f'Roommate{i}']):
                    roommates.append(row[f'Roommate{i}'])
            
            if id in self.students: # Student already in dorm
                if len(roommates) == 0:
                    raise ValueError(f'Student {id} is already in dorm, did not specify roommates, but applied for accommodation. Contradiction.')
                student_ids_with_rooms.append(id)
                self.students[id].intended_roommate_ids = roommates
            else:
                self.students[id] = Student(id, gender, degree, year, roommates)
                student_ids_to_accommodate.append(id)
        # List of students to accommodate that do not have rooms
    
        return student_ids_with_rooms, student_ids_to_accommodate
                
    
    def pair_roommates(self):
        student_ids_to_destroy: dict[int, str] = {}
        for student in self.students.values():
            if len(student.intended_roommate_ids) == 0: # Student did not apply for roommates matching.
                continue                                # That student either already has a room or applied as random (does not need to be paired)
            
            # Check if all roommates exist in students list
            for roommate_id in student.intended_roommate_ids: 
                if roommate_id not in self.students:
                    student_ids_to_destroy[student.id] = f'Id error! Student {student.id} fault! Roommate {roommate_id} id does not exist or he/she did not apply for accommodation.'
                    break
            
            if student.id in student_ids_to_destroy:
                continue

            # Check if all Ids are unique. Student did not apply for the same roommate twice or no one applied for himself/herself.
            set_of_roommates = set(student.intended_roommate_ids)
            set_of_roommates.add(student.id) # Now it is a set of all students that applied for each other
            if len(set_of_roommates) != len(student.intended_roommate_ids) + 1:
                student_ids_to_destroy[student.id] = f'Ids uniqueness error! Student {student.id} fault! Roommate Ids are not unique or student applied for himself/herself.'

            if student.id in student_ids_to_destroy:
                continue
            
            # Now that we know all roommates exist and are unique, we need to check if each roommate applied for the other.
            # In case of 2, If A applied for B, then B must have applied for A. In case of 3, If A applied for B and C, then B must have applied for A, C and C must have applied for A, B.
            # double check this
            for roommate_id in student.intended_roommate_ids:
                set_of_intended_roommates = set(self.students[roommate_id].intended_roommate_ids)
                set_of_intended_roommates.add(roommate_id)
                if set_of_intended_roommates != set_of_roommates:
                    student_ids_to_destroy[student.id] = f'Id match error. Student {student.id} or Roommate {roommate_id} did something wrong with Ids.'
                    break
            
            if student.id in student_ids_to_destroy:
                continue

            # Check if he has room already
            
            # Gender matching
            for roommate_id in student.intended_roommate_ids:
                if self.students[roommate_id].gender != student.gender:
                    student_ids_to_destroy[student.id] = f'Gender match error. Student {student.id} or Roommate {roommate_id} have different genders.'
                    break
        
                    
                
                

