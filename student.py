class Student:

    def __init__(self, id, name, gender, degree, year, roomate_ids):
        self.id = id
        self.name = name
        self.gender = gender
        self.degree = degree
        self.year = year
        self.roomate_ids = roomate_ids
        self.roomates = []
        self.room = None

    def __str__(self):
        return f"{self.id} {self.name} " + self.gender + " " + str(self.roomate_ids)

    def __repr__(self):
        return f"{self.id} {self.name} " + self.gender + " " + str(self.roomate_ids)

    #commment
