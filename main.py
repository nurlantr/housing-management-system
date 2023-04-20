# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from models import Dormitory, Student
from populator import Populator


nu = Dormitory()
populator = Populator("test1.csv", nu)

# populator.students["A"] = Student("A", "Alim", "Female", "-", "-", ['D'])
# populator.students["B"] = Student("B", "Bota", "Male", "-", "-", ['M'])
# populator.students["C"] = Student("C", "Batyr", "Male", "-", "-", ['M','B'])
# populator.students["D"] = Student("D", "Dosbol", "Female", "-", "-", ['A'])
# populator.students["M"] = Student("M", "Naga", "Male", "-", "-", ['C'])
for st in populator.students.values():
	print(st)

populator.pair()
print()

for st in populator.students.values():
	print(st, 'Roomates:', st.roomates)

# rooms_list = ["D11007", "D11111", "D11110"]
# populator.populate(["A", "D", "B","C", "M"], rooms_list)
populator.populate([student.id for student in populator.students.values()], [room.number for room in nu.rooms.values()])
# populator.populate(['201780219','201826542','202105768'], [room.number for room in nu.rooms.values()])

# for room_num in rooms_list:
#       print(nu.rooms[room_num])

print(nu)

for st in populator.students.values():
	print(st, 'Roomates:', st.roomates)
    
populator.to_csv("test_output.csv")



