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

    for dummy_id in ls:
        dummy_friend = students.get(dummy_id)
        if dummy_friend != None and len(dummy_friend.roomate_ids) != 0 and dummy_friend.roomate_ids.count(dummy.id) > 0:
            selfdestruction(dummy_friend, students)



nu = Dormitory()
populator = Populator("listcsv.csv", nu)


populator.students["A"] = Student("A", "Alim", "Male", "-", "-", ["B", "A"])
populator.students["B"] = Student("B", "Alim", "Male", "-", "-", ["A", "B"])
populator.students["C"] = Student("C", "Alim", "Male", "-", "-", ["B", "D"])
populator.students["D"] = Student("D", "Alim", "Male", "-", "-", ["M"])
populator.students["M"] = Student("M", "Alim", "Male", "-", "-", ["D"])
for st in populator.students.values():
	print(st)

populator.pair()
print()

for st in populator.students.values():
	print(st, st.roomates)


# selfdestruction(students["M"], students)

# for st in students.values():
# 	print(st)








