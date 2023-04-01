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


populator.students["A"] = Student("A", "Alim", "Male", "-", "-", ['D'])
populator.students["B"] = Student("B", "Bota", "Male", "-", "-", ['M','C'])
populator.students["C"] = Student("C", "Batyr", "Male", "-", "-", ['M','B'])
populator.students["D"] = Student("D", "Dosbol", "Male", "-", "-", ['A'])
populator.students["M"] = Student("M", "Naga", "Male", "-", "-", ['B','C'])
for st in populator.students.values():
	print(st)

populator.pair()
print()

for st in populator.students.values():
	print(st, st.roomates)
    


populator.populate(["A", "D", "B","C", "M"], ["D11007", "D11111", "D11110"])
print(populator.dorm)
for st in populator.students.values():
     print(st.room)



# selfdestruction(students["M"], students)

# for st in students.values():
# 	print(st)








