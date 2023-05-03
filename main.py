from models import Dormitory
from populator import Populator
import pandas as pd
import numpy as np
nu = Dormitory()
populator = Populator("", nu)

populator.read_excel_dorm('dorm.xlsx')

print(nu.print_occupied_rooms())

students_to_accomodate = populator.read_excel_students('test_input_excel.xlsx')

print(nu.print_occupied_rooms())


empty_rooms = nu.get_empty_rooms(23, 24)
populator.populate(students_to_accomodate, empty_rooms, randomize = True)

print(nu.print_occupied_rooms())

populator.upload_csv('upload', 'our_upload.csv')










