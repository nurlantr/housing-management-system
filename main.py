from models import Dormitory
from populator import Populator
import pandas as pd
import numpy as np
nu = Dormitory()
populator = Populator("", nu)

df = populator.read_excel_dorm('full.xlsx')

print(nu.print_occupied_rooms())


empty_rooms = nu.get_rooms(23, 27, 1)
print(empty_rooms)
print(len(empty_rooms))
# new_df = pd.DataFrame({'Room': empty_rooms})
# print(new_df)
# new_df  = new_df.drop(new_df.index[0:28])
# new_df.to_excel('empty_rooms.xlsx', index = False)




# populator.read_excel_dorm('dorm.xlsx')

# print(nu.print_occupied_rooms())

# students_to_accomodate = populator.read_excel_students('test_input_excel.xlsx')

# print(nu.print_occupied_rooms())


# populator.populate(students_to_accomodate, empty_rooms, randomize = True)

# print(nu.print_occupied_rooms())

# populator.upload_csv('upload', 'our_upload.csv')










