# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from dormitory import Dormitory
from populator import Populator
from block import Block
from student import Student

def selfdestruction(dummy, students):
    if len(dummy.roomate_ids) == 0:
        return
    
    ls = dummy.roomate_ids.copy()
    dummy.roomate_ids = []

    for dummy_ids in ls:
        dummy_friend = students.get(dummy_ids)
        if dummy_friend != None and len(dummy_friend.roomate_ids) != 0:
            selfdestruction(dummy_friend, students)
        


# nu = Dormitory()
# populator = Populator("listcsv.csv", nu)
# print(nu)

# print("Number of students:", nu.num_students())

# print(populator.students["202048825"].room)

# populator.to_csv()
students = {}
sst = Student("A", "Alim", "Male", "-", "-", ["B", "C"])
students["A"] = sst
students["B"] = (Student("B", "Alim", "Male", "-", "-", ["D"]))
students["C"] = (Student("C", "Alim", "Male", "-", "-", ["A"]))
students["D"] = (Student("D", "Alim", "Male", "-", "-", ["B"]))
students["M"] = (Student("M", "Alim", "Male", "-", "-", []))
for st in students.values():
	print(st)

selfdestruction(sst, students)


for st in students.values():
	print(st)

# selfdestruction(students["M"], students)

# for st in students.values():
# 	print(st)








