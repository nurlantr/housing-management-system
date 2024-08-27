# import streamlit as st
# import pandas as pd
# from populator_refactored import Populator
# from models_refactored import Room, Student, Dormitory
# from io import BytesIO
# import psycopg2

# def fetch_current_dormitory(excluded_rooms_file=None):
#     conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
#     cur = conn.cursor()
#     fetch_query = "SELECT block, room, gender, students FROM dormitory"
#     cur.execute(fetch_query)
#     records = cur.fetchall()
#     cur.close()
#     conn.close()

#     blocks = {}
#     for block_num in range(22, 28):
#         rooms = []
#         for record in records:
#             if record[0] == block_num:
#                 rooms.append(record[1])
#         blocks[block_num] = Dormitory.Block(block_num, rooms, 2 if block_num != 22 else 3)

#     dormitory = Dormitory(blocks, excluded_rooms_file)
#     for record in records:
#         block_num, room_num, gender, students = record
#         room = dormitory.rooms[block_num][room_num]
#         if gender:
#             room.gender = gender
#         if students:
#             student_ids = [int(id) for id in students.split(", ")]
#             for student_id in student_ids:
#                 room.students.append(Student(student_id, gender))
#     return dormitory

# def fetch_dormitory_data():
#     conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
#     cur = conn.cursor()
#     fetch_query = "SELECT block, room, gender, students FROM dormitory"
#     cur.execute(fetch_query)
#     records = cur.fetchall()
#     cur.close()
#     conn.close()

#     data = []
#     for record in records:
#         data.append({
#             "Block": record[0],
#             "Room": record[1],
#             "Gender": record[2],
#             "Students": record[3]
#         })

#     df = pd.DataFrame(data)
#     df = df.sort_values(by=["Block", "Room"])
#     df['Number of Students'] = df['Students'].apply(lambda x: len(x.split(', ')) if x else 0)
#     return df

# def build_dormitory():
#     if not st.session_state.build:
#         st.session_state.nu = fetch_current_dormitory(st.session_state.excluded_data)
#         print(st.session_state.nu)
#     st.session_state.build = True

# def init_session_state():
#     st.set_page_config(layout="wide")
#     if 'populate_clicked' not in st.session_state:
#         st.session_state.populate_clicked = False
#     if 'get_rooms_clicked' not in st.session_state:
#         st.session_state.get_rooms_clicked = False
#     if 'get_students_clicked' not in st.session_state:
#         st.session_state.get_students_clicked = False
#     if 'configured_blocks' not in st.session_state:
#         st.session_state.configured_blocks = []
#     if 'generate' not in st.session_state:
#         st.session_state.generate = False
#     if 'build' not in st.session_state:
#         st.session_state.build = False
#     if 'blocks' not in st.session_state:
#         st.session_state.blocks = []
#     if 'page' not in st.session_state:
#         st.session_state.page = "Populator Page"
#     if 'my_slider_value' not in st.session_state:
#         st.session_state.my_slider_value = (22, 27)
#     if "upload_clicked" not in st.session_state:
#         st.session_state.upload_clicked = False
#     if "room_data_uploaded" not in st.session_state:
#         st.session_state.room_data_uploaded = False
#     if "occupants_data_uploaded" not in st.session_state:
#         st.session_state.occupants_data_uploaded = False
#     if 'custom_blocks' not in st.session_state:
#         st.session_state.custom_blocks = None
#     if 'excluded_data' not in st.session_state:
#         st.session_state.excluded_data = None
#     if 'paired_roomates' not in st.session_state:
#         st.session_state.paired_roomates = False
#     if 'settled_roomates' not in st.session_state:
#         st.session_state.settled_roomates = False
#     if 'file_processed' not in st.session_state:
#         st.session_state.file_processed = False
#     if 'nu' not in st.session_state:
#         st.session_state.nu = fetch_current_dormitory()
#     if 'filter_block' not in st.session_state:
#         st.session_state.filter_block = None
#     if 'filter_gender' not in st.session_state:
#         st.session_state.filter_gender = None
#     if 'filter_empty' not in st.session_state:
#         st.session_state.filter_empty = False
#     if 'filter_partially_empty' not in st.session_state:
#         st.session_state.filter_partially_empty = []

# def callbackUpload():
#     st.session_state.upload_clicked = True

# def callback_rdataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.room_data_uploaded = True

# def callback_odataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.occupants_data_uploaded = True

# def apply_filters(df, block, gender, empty, partially_empty):
#     if block:
#         df = df[df['Block'].isin(block)]
#     if gender:
#         df = df[df['Gender'].isin(gender)]
#     if empty:
#         df = df[(df['Gender'].isna()) & (df['Number of Students'] == 0)]
#     if partially_empty:
#         df = df[df['Number of Students'].isin(partially_empty)]
#     return df

# def populate_details():
#     st.markdown("---")
#     st.write("Create student pairs")
#     if st.button("Pair", help="Create student pairings", on_click=pair_roomates, key='pair_roomates'):
#         st.write("Student pairs created")
#     st.markdown("---")
#     st.write("Settle roomates to the already accommodated")
#     if st.button("Подселить", help="Подселить руммейтов к живущим", on_click=settle_roomates, key='settle_roomates'):
#         st.write("Roomates settled")
#     st.markdown("---")
#     with st.form(key="rooms"):
#         col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
#         col1.multiselect("List of blocks", options=st.session_state.nu.rooms.keys(), default=st.session_state.nu.rooms.keys(), key="block_list_room")
#         col2.multiselect("List of floors", options=range(2, 13), default=range(2, 13), key='floor_list_room')
#         col3.multiselect("Occupancy", options=[0, 1, 2, 3, 4], default=[0, 1, 2, 3, 4], key='occupancy_room')
#         col4.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_room')
#         col5.text_input("Room", placeholder="Example: 903", key='_room')
#         st.form_submit_button("Get Rooms", on_click=get_rooms)
#         if st.session_state.get_rooms_clicked:
#             st.dataframe(st.session_state.filtered_rooms_df)
#     with st.form(key="students"):
#         col1, col2, col3, col4 = st.columns(4)
#         col1.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_student')
#         col2.multiselect("Degree", options=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), default=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), key='degree_student')
#         col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].unique(), key='year_student')
#         col4.text_input("Student ID", placeholder="Comma-Sep, Example: 202085777", key='_student')
#         st.form_submit_button("Get Students", on_click=get_students)
#         if st.session_state.get_students_clicked:
#             st.dataframe(st.session_state.filtered_students_df)

#     st.button("Populate", help="Populate", on_click=populate, key='populate')
#     if st.session_state.populate_clicked:
#         st.write("Populated")
#         upload_df = get_upload_df()
#         buffer = BytesIO()
#         with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#             upload_df.to_excel(writer, sheet_name='Sheet1', index=False)
#             writer.close()

#             st.download_button(
#                 label="Получить файл заливки",
#                 data=buffer,
#                 help="Скачать CSV файл заливки",
#                 file_name='Файл_заливки.xlsx',
#                 mime="application/vnd.ms-excel"
#             )

# def get_upload_df():
#     return st.session_state.populator.to_upload_file()

# def populate():
#     if st.session_state.get_rooms_clicked and st.session_state.get_students_clicked:
#         st.session_state.populate_clicked = True
#         st.session_state.populator.populate(st.session_state.filtered_students_list, st.session_state.filtered_rooms_list)
#     else:
#         st.error("Please get rooms and students first")

# def get_rooms():
#     st.session_state.get_rooms_clicked = True
#     block_list = st.session_state.block_list_room
#     floor_list = st.session_state.floor_list_room
#     occupancy_list = st.session_state.occupancy_room
#     gender = st.session_state.gender_room
#     room = st.session_state._room
#     if room != "":
#         room = int(room)
#     else:
#         room = None
#     st.session_state.filtered_rooms_df, st.session_state.filtered_rooms_list = st.session_state.populator.get_rooms(block_list, floor_list, occupancy_list, gender, room)

# def get_students():
#     st.session_state.get_students_clicked = True
#     gender = st.session_state.gender_student
#     degree = st.session_state.degree_student
#     year = st.session_state.year_student
#     student_ids = st.session_state._student
#     if student_ids == "":
#         student_ids = None
#     else:
#         student_ids = [int(id) for id in student_ids.split(",")]
#     st.session_state.filtered_students_df, st.session_state.filtered_students_list = st.session_state.populator.filter_students(gender, degree, year, student_ids)

# def pair_roomates():
#     if not st.session_state.paired_roomates:
#         st.session_state.populator.match_roommates()
#     st.session_state.paired_roomates = True

# def settle_roomates():
#     if not st.session_state.settled_roomates:
#         st.session_state.populator.assign_roommate()
#     st.session_state.settled_roomates = True

# def file_processing():
#     if not st.session_state.file_processed:
#         st.session_state.populator = Populator(st.session_state.nu)
#         if st.session_state.room_data is not None:
#             st.session_state.populator.update_dorm(st.session_state.room_data)
#         st.session_state.populator.read_students_to_accommodate(st.session_state.occupant_data)
#         st.session_state.populator.refresh_df_students_to_accommodate()
#         st.write("File processing complete")

#     st.session_state.file_processed = True

# def get_page():
#     return st.session_state.page

# def render_page():
#     page = get_page()
#     if page == "Populator Page":
#         populator_page()
#     elif page == "Dormitory Table":
#         dormitory_table_page()

# def render_sidebar():
#     st.sidebar.title("Sidebar")
#     options = ["Populator Page", "Dormitory Table"]
#     page = st.sidebar.selectbox("Select a page", options)

#     if page != get_page():
#         st.session_state.page = page

# def populator_page():
#     st.title("Populator Page")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.header("Заполненность комнат")
#         st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)

#     with col2:
#         st.header("Список заселяемых")
#         st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"], on_change=callback_odataUpload)

#     #upload = st.button("Загрузить", key="upload", on_click=callbackUpload)
#     st.header("Список игнорируемых комнат")
#     st.session_state.excluded_data = st.file_uploader("Upload Excel file for excluded rooms", type=["xls", "xlsx"])
#     if st.session_state.excluded_data is not None:
#         st.write("Excluded rooms uploaded")
    
#     upload = st.button("Загрузить", key="upload", on_click=callbackUpload)

#     if st.session_state.upload_clicked:
#         if st.session_state.occupant_data is not None:
#             st.write("Второй файл сохранен")
#         else:
#             st.error("Please upload the file 'Список заселяемых'")
        
#         if st.session_state.excluded_data:
#             st.write("Excluded rooms file processed")

#         if st.session_state.occupant_data:
#             file_processing()
#             populate_details()

# def dormitory_table_page():
#     st.title("Current Dormitory State")
#     st.write("Below is the current state of the dormitory:")

#     df = fetch_dormitory_data()

#     block_filter = st.multiselect("Filter by Block", options=df['Block'].unique(), default=df['Block'].unique())
#     gender_filter = st.multiselect("Filter by Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
#     empty_filter = st.checkbox("Show only empty rooms")
#     partially_empty_filter = st.multiselect("Show rooms with specific number of students", options=range(1, 5), default=[])

#     filtered_df = apply_filters(df, block_filter, gender_filter, empty_filter, partially_empty_filter)

#     st.dataframe(filtered_df)

#     st.write(f"Number of selected rooms: {len(filtered_df)}")

# def main():
#     init_session_state()
#     render_sidebar()
#     render_page()

# main()

import streamlit as st
import pandas as pd
from populator_refactored import Populator
from models_refactored import Room, Student, Dormitory
from io import BytesIO
import psycopg2

def fetch_current_dormitory(excluded_rooms_file=None):
    conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
    cur = conn.cursor()
    fetch_query = "SELECT block, room, gender, students FROM dormitory"
    cur.execute(fetch_query)
    records = cur.fetchall()
    cur.close()
    conn.close()

    blocks = {}
    for block_num in range(22, 28):
        rooms = []
        for record in records:
            if record[0] == block_num:
                rooms.append(record[1])
        blocks[block_num] = Dormitory.Block(block_num, rooms, 2 if block_num != 22 else 3)

    dormitory = Dormitory(blocks, excluded_rooms_file)
    for record in records:
        block_num, room_num, gender, students = record
        room = dormitory.rooms[block_num][room_num]
        if gender:
            room.gender = gender
        if students:
            student_ids = [int(id) for id in students.split(", ")]
            for student_id in student_ids:
                student = Student(student_id, gender)
                student.room = room
                room.students.append(student)
    return dormitory

def fetch_dormitory_data():
    conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
    cur = conn.cursor()
    fetch_query = "SELECT block, room, gender, students FROM dormitory"
    cur.execute(fetch_query)
    records = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for record in records:
        data.append({
            "Block": record[0],
            "Room": record[1],
            "Gender": record[2],
            "Students": record[3]
        })

    df = pd.DataFrame(data)
    df = df.sort_values(by=["Block", "Room"])
    df['Number of Students'] = df['Students'].apply(lambda x: len(x.split(', ')) if x else 0)
    return df

def build_dormitory():
    if not st.session_state.build:
        st.session_state.nu = fetch_current_dormitory(st.session_state.excluded_data)
        print(st.session_state.nu)
    st.session_state.build = True

def init_session_state():
    st.set_page_config(layout="wide")
    if 'populate_clicked' not in st.session_state:
        st.session_state.populate_clicked = False
    if 'get_rooms_clicked' not in st.session_state:
        st.session_state.get_rooms_clicked = False
    if 'get_students_clicked' not in st.session_state:
        st.session_state.get_students_clicked = False
    if 'configured_blocks' not in st.session_state:
        st.session_state.configured_blocks = []
    if 'generate' not in st.session_state:
        st.session_state.generate = False
    if 'build' not in st.session_state:
        st.session_state.build = False
    if 'blocks' not in st.session_state:
        st.session_state.blocks = []
    if 'page' not in st.session_state:
        st.session_state.page = "Populator Page"
    if 'my_slider_value' not in st.session_state:
        st.session_state.my_slider_value = (22, 27)
    if "upload_clicked" not in st.session_state:
        st.session_state.upload_clicked = False
    if "room_data_uploaded" not in st.session_state:
        st.session_state.room_data_uploaded = False
    if "occupants_data_uploaded" not in st.session_state:
        st.session_state.occupants_data_uploaded = False
    if 'custom_blocks' not in st.session_state:
        st.session_state.custom_blocks = None
    if 'excluded_data' not in st.session_state:
        st.session_state.excluded_data = None
    if 'paired_roomates' not in st.session_state:
        st.session_state.paired_roomates = False
    if 'settled_roomates' not in st.session_state:
        st.session_state.settled_roomates = False
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    if 'nu' not in st.session_state:
        st.session_state.nu = fetch_current_dormitory()
    if 'filter_block' not in st.session_state:
        st.session_state.filter_block = None
    if 'filter_gender' not in st.session_state:
        st.session_state.filter_gender = None
    if 'filter_empty' not in st.session_state:
        st.session_state.filter_empty = False
    if 'filter_partially_empty' not in st.session_state:
        st.session_state.filter_partially_empty = []

def callbackUpload():
    st.session_state.upload_clicked = True

def callback_rdataUpload():
    st.session_state.upload_clicked = False
    st.session_state.room_data_uploaded = True

def callback_odataUpload():
    st.session_state.upload_clicked = False
    st.session_state.occupants_data_uploaded = True

def apply_filters(df, block, gender, empty, partially_empty):
    if block:
        df = df[df['Block'].isin(block)]
    if gender:
        df = df[df['Gender'].isin(gender)]
    if empty:
        df = df[(df['Gender'].isna()) & (df['Number of Students'] == 0)]
    if partially_empty:
        df = df[df['Number of Students'].isin(partially_empty)]
    return df

def populate_details():
    st.markdown("---")
    st.write("Create student pairs")
    if st.button("Pair", help="Create student pairings", on_click=pair_roomates, key='pair_roomates'):
        st.write("Student pairs created")
    st.markdown("---")
    st.write("Settle roommates to the already accommodated")
    if st.button("Подселить", help="Подселить руммейтов к живущим", on_click=settle_roomates, key='settle_roomates'):
        st.write("Roommates settled")
    st.markdown("---")
    with st.form(key="rooms"):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        col1.multiselect("List of blocks", options=st.session_state.nu.rooms.keys(), default=st.session_state.nu.rooms.keys(), key="block_list_room")
        col2.multiselect("List of floors", options=range(2, 13), default=range(2, 13), key='floor_list_room')
        col3.multiselect("Occupancy", options=[0, 1, 2, 3, 4], default=[0, 1, 2, 3, 4], key='occupancy_room')
        col4.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_room')
        col5.text_input("Room", placeholder="Example: 903", key='_room')
        st.form_submit_button("Get Rooms", on_click=get_rooms)
        if st.session_state.get_rooms_clicked:
            st.dataframe(st.session_state.filtered_rooms_df)
    with st.form(key="students"):
        col1, col2, col3, col4 = st.columns(4)
        col1.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_student')
        col2.multiselect("Degree", options=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), default=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), key='degree_student')
        #col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].unique(), key='year_student')
        col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].dropna().unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].dropna().unique(), key='year_student')
        col4.text_input("Student ID", placeholder="Comma-Sep, Example: 202085777", key='_student')
        st.form_submit_button("Get Students", on_click=get_students)
        if st.session_state.get_students_clicked:
            st.dataframe(st.session_state.filtered_students_df)

    st.button("Populate", help="Populate", on_click=populate, key='populate')
    if st.session_state.populate_clicked:
        st.write("Populated")
        upload_df = get_upload_df()
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            upload_df.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.close()

            st.download_button(
                label="Получить файл заливки",
                data=buffer,
                help="Скачать CSV файл заливки",
                file_name='Файл_заливки.xlsx',
               
                mime="application/vnd.ms-excel"
            )

def get_upload_df():
    return st.session_state.populator.to_upload_file()

def populate():
    if st.session_state.get_rooms_clicked and st.session_state.get_students_clicked:
        st.session_state.populate_clicked = True
        print("Calling populate method")
        st.session_state.populator.populate(st.session_state.filtered_students_list, st.session_state.filtered_rooms_list)
    else:
        st.error("Please get rooms and students first")

def get_rooms():
    st.session_state.get_rooms_clicked = True
    block_list = st.session_state.block_list_room
    floor_list = st.session_state.floor_list_room
    occupancy_list = st.session_state.occupancy_room
    gender = st.session_state.gender_room
    room = st.session_state._room
    if room != "":
        room = int(room)
    else:
        room = None
    st.session_state.filtered_rooms_df, st.session_state.filtered_rooms_list = st.session_state.populator.get_rooms(block_list, floor_list, occupancy_list, gender, room)

def get_students():
    st.session_state.get_students_clicked = True
    gender = st.session_state.gender_student
    degree = st.session_state.degree_student
    year = st.session_state.year_student
    student_ids = st.session_state._student
    if student_ids == "":
        student_ids = None
    else:
        student_ids = [int(id) for id in student_ids.split(",")]
    st.session_state.filtered_students_df, st.session_state.filtered_students_list = st.session_state.populator.filter_students(gender, degree, year, student_ids)

def pair_roomates():
    if not st.session_state.paired_roomates:
        print("Pairing roommates")
        st.session_state.populator.match_roommates()
    st.session_state.paired_roomates = True

def settle_roomates():
    if not st.session_state.settled_roomates:
        print("Settling roommates")
        st.session_state.populator.assign_roommate()
    st.session_state.settled_roomates = True

def file_processing():
    if not st.session_state.file_processed:
        st.session_state.populator = Populator(st.session_state.nu)
        if st.session_state.room_data is not None:
            st.session_state.populator.update_dorm(st.session_state.room_data)
        st.session_state.populator.read_students_to_accommodate(st.session_state.occupant_data)
        st.session_state.populator.refresh_df_students_to_accommodate()
        st.write("File processing complete")
        print("File processing complete")

    st.session_state.file_processed = True

def get_page():
    return st.session_state.page

def render_page():
    page = get_page()
    if page == "Populator Page":
        populator_page()
    elif page == "Dormitory Table":
        dormitory_table_page()

def render_sidebar():
    st.sidebar.title("Sidebar")
    options = ["Populator Page", "Dormitory Table"]
    page = st.sidebar.selectbox("Select a page", options)

    if page != get_page():
        st.session_state.page = page

def populator_page():
    st.title("Populator Page")

    col1, col2 = st.columns(2)
    with col1:
        st.header("Заполненность комнат")
        st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)

    with col2:
        st.header("Список заселяемых")
        st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"], on_change=callback_odataUpload)

    st.header("Список игнорируемых комнат")
    st.session_state.excluded_data = st.file_uploader("Upload Excel file for excluded rooms", type=["xls", "xlsx"])
    if st.session_state.excluded_data is not None:
        st.write("Excluded rooms uploaded")
    
    upload = st.button("Загрузить", key="upload", on_click=callbackUpload)

    if st.session_state.upload_clicked:
        if st.session_state.occupant_data is not None:
            st.write("Второй файл сохранен")
        else:
            st.error("Please upload the file 'Список заселяемых'")
        
        if st.session_state.excluded_data:
            st.write("Excluded rooms file processed")

        if st.session_state.occupant_data:
            file_processing()
            populate_details()

def dormitory_table_page():
    st.title("Current Dormitory State")
    st.write("Below is the current state of the dormitory:")

    df = fetch_dormitory_data()

    block_filter = st.multiselect("Filter by Block", options=df['Block'].unique(), default=df['Block'].unique())
    gender_filter = st.multiselect("Filter by Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
    empty_filter = st.checkbox("Show only empty rooms")
    partially_empty_filter = st.multiselect("Show rooms with specific number of students", options=range(1, 5), default=[])

    filtered_df = apply_filters(df, block_filter, gender_filter, empty_filter, partially_empty_filter)

    st.dataframe(filtered_df)

    st.write(f"Number of selected rooms: {len(filtered_df)}")

def main():
    init_session_state()
    render_sidebar()
    render_page()

main()


# import streamlit as st
# import pandas as pd
# from populator_refactored import Populator
# from models_refactored import Room, Student, Dormitory
# from io import BytesIO
# import psycopg2

# def fetch_current_dormitory():
#     conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
#     cur = conn.cursor()
#     fetch_query = "SELECT block, room, gender, students FROM dormitory"
#     cur.execute(fetch_query)
#     records = cur.fetchall()
#     cur.close()
#     conn.close()
    
#     blocks = {}
#     for block_num in range(22, 28):
#         rooms = []
#         for record in records:
#             if record[0] == block_num:
#                 rooms.append(record[1])
#         blocks[block_num] = Dormitory.Block(block_num, rooms, 2 if block_num != 22 else 3)
    
#     # NEW (19.07)
#     dormitory = Dormitory(blocks)
#     for record in records:
#         block_num, room_num, gender, students = record
#         room = dormitory.rooms[block_num][room_num]
#         if gender:
#             room.gender = gender
#         if students:
#             student_ids = [int(id) for id in students.split(", ")]
#             for student_id in student_ids:
#                 room.students.append(Student(student_id, gender))
#     return dormitory

# # FOR NEW PAGE (TESTING)
# def fetch_dormitory_data():
#     conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
#     cur = conn.cursor()
#     fetch_query = "SELECT block, room, gender, students FROM dormitory"
#     cur.execute(fetch_query)
#     records = cur.fetchall()
#     cur.close()
#     conn.close()
    
#     data = []
#     for record in records:
#         data.append({
#             "Block": record[0],
#             "Room": record[1],
#             "Gender": record[2],
#             "Students": record[3]
#         })
    
#     df = pd.DataFrame(data)
#     df = df.sort_values(by=["Block", "Room"])  # Sort by Block and Room
#     df['Number of Students'] = df['Students'].apply(lambda x: len(x.split(', ')) if x else 0)
#     return df

# def build_dormitory():
#     if not st.session_state.build:
#         st.session_state.nu = fetch_current_dormitory()
#         print(st.session_state.nu)  
#     st.session_state.build = True

# def init_session_state():
#     st.set_page_config(layout="wide")
#     if 'populate_clicked' not in st.session_state:
#         st.session_state.populate_clicked = False
#     if 'get_rooms_clicked' not in st.session_state:
#         st.session_state.get_rooms_clicked = False
#     if 'get_students_clicked' not in st.session_state:
#         st.session_state.get_students_clicked = False
#     if 'configured_blocks' not in st.session_state:
#         st.session_state.configured_blocks = []
#     if 'generate' not in st.session_state:
#         st.session_state.generate = False
#     if 'build' not in st.session_state:
#         st.session_state.build = False
#     if 'blocks' not in st.session_state:
#         st.session_state.blocks = []
#     if 'page' not in st.session_state:
#         st.session_state.page = "Populator Page"
#     if 'my_slider_value' not in st.session_state:
#         st.session_state.my_slider_value = (22, 27)
#     if "upload_clicked" not in st.session_state:
#         st.session_state.upload_clicked = False
#     if "room_data_uploaded" not in st.session_state:
#         st.session_state.room_data_uploaded = False
#     if "occupants_data_uploaded" not in st.session_state:
#         st.session_state.occupants_data_uploaded = False
#     if 'custom_blocks' not in st.session_state:
#         st.session_state.custom_blocks = None
#     if 'excluded_data' not in st.session_state:
#         st.session_state.excluded_data = None
#     if 'paired_roomates' not in st.session_state:
#         st.session_state.paired_roomates = False
#     if 'settled_roomates' not in st.session_state:
#         st.session_state.settled_roomates = False
#     if 'file_processed' not in st.session_state:
#         st.session_state.file_processed = False
#     if 'nu' not in st.session_state:
#         st.session_state.nu = fetch_current_dormitory()
#     if 'filter_block' not in st.session_state:
#         st.session_state.filter_block = None
#     if 'filter_gender' not in st.session_state:
#         st.session_state.filter_gender = None
#     if 'filter_empty' not in st.session_state:
#         st.session_state.filter_empty = False
#     if 'filter_partially_empty' not in st.session_state:
#         st.session_state.filter_partially_empty = []

# def callbackUpload():
#     st.session_state.upload_clicked = True

# def callback_rdataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.room_data_uploaded = True

# def callback_odataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.occupants_data_uploaded = True

# # FILTERS FOR NEW PAGE
# def apply_filters(df, block, gender, empty, partially_empty):
#     if block:
#         df = df[df['Block'].isin(block)]
#     if gender:
#         df = df[df['Gender'].isin(gender)]
#     if empty:
#         df = df[(df['Gender'].isna()) & (df['Number of Students'] == 0)]
#     if partially_empty:
#         df = df[df['Number of Students'].isin(partially_empty)]
#     return df

# def populate_details():
#     st.markdown("---")
#     st.write("Create student pairs") 
#     if st.button("Pair", help = "Create student pairings", on_click = pair_roomates, key = 'pair_roomates'):
#         st.write("Student pairs created")
#     st.markdown("---")
#     st.write("Settle roomates to the already accommodated") 
#     if st.button("Подселить", help = "Подселить руммейтов к живущим", on_click = settle_roomates, key = 'settle_roomates'):
#         st.write("Roomates settled")
#     st.markdown("---")
#     with st.form(key="rooms"): 
#         col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1]) 
#         col1.multiselect("List of blocks", options=st.session_state.nu.rooms.keys(), default=st.session_state.nu.rooms.keys(), key = "block_list_room")
#         col2.multiselect("List of floors", options=range(2, 13), default=range(2, 13), key = 'floor_list_room') 
#         col3.multiselect("Occupancy", options=[0,1,2,3,4], default=[0,1,2,3,4], key = 'occupancy_room')
#         col4.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key = 'gender_room')
#         col5.text_input("Room", placeholder="Example: 903", key = '_room')
#         st.form_submit_button("Get Rooms", on_click=get_rooms) 
#         if st.session_state.get_rooms_clicked:
#             st.dataframe(st.session_state.filtered_rooms_df)
#     with st.form(key="students"): 
#         col1, col2, col3, col4= st.columns(4) 
#         col1.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_student')
#         col2.multiselect("Degree", options=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), default=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), key = 'degree_student') 
#         col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].unique(), key = 'year_student')
#         col4.text_input("Student ID", placeholder="Comma-Sep, Example: 202085777", key = '_student')
#         st.form_submit_button("Get Students", on_click=get_students)
#         if st.session_state.get_students_clicked:
#             st.dataframe(st.session_state.filtered_students_df)
    
#     st.button("Populate", help = "Populate", on_click = populate, key = 'populate')
#     if st.session_state.populate_clicked:
#         st.write("Populated") 
#         upload_df = get_upload_df()
#         buffer = BytesIO()
#         with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#             upload_df.to_excel(writer, sheet_name='Sheet1', index=False)
#             writer.close()

#             st.download_button(
#                 label="Получить файл заливки",
#                 data=buffer,
#                 help = "Скачать CSV файл заливки",
#                 file_name='Файл_заливки.xlsx',
#                 mime="application/vnd.ms-excel"
#             )

# def get_upload_df():
#     return st.session_state.populator.to_upload_file()

# def populate():
#     if st.session_state.get_rooms_clicked and st.session_state.get_students_clicked:
#         st.session_state.populate_clicked = True
#         st.session_state.populator.populate(st.session_state.filtered_students_list, st.session_state.filtered_rooms_list)     
#     else:
#         st.error("Please get rooms and students first")

# def get_rooms():
#     st.session_state.get_rooms_clicked = True
#     block_list = st.session_state.block_list_room
#     floor_list = st.session_state.floor_list_room
#     occupancy_list = st.session_state.occupancy_room
#     gender = st.session_state.gender_room
#     room = st.session_state._room
#     if room != "":
#         room = int(room)
#     else:
#         room = None
#     st.session_state.filtered_rooms_df, st.session_state.filtered_rooms_list = st.session_state.populator.get_rooms(block_list, floor_list, occupancy_list, gender, room)

# def get_students():
#     st.session_state.get_students_clicked = True
#     gender = st.session_state.gender_student
#     degree = st.session_state.degree_student
#     year = st.session_state.year_student
#     student_ids = st.session_state._student
#     if student_ids == "":
#         student_ids = None
#     else:
#         student_ids = [int(id) for id in student_ids.split(",")]
#     st.session_state.filtered_students_df, st.session_state.filtered_students_list = st.session_state.populator.filter_students(gender, degree, year, student_ids)

# def pair_roomates():
#     if not st.session_state.paired_roomates:
#         st.session_state.populator.match_roommates()
#     st.session_state.paired_roomates = True

# def settle_roomates():
#     if not st.session_state.settled_roomates:
#         st.session_state.populator.assign_roommate()
#     st.session_state.settled_roomates = True

# def file_processing():
#     if not st.session_state.file_processed:
#         st.session_state.populator = Populator(st.session_state.nu)
#         if st.session_state.room_data is not None:
#             st.session_state.populator.update_dorm(st.session_state.room_data)
#         st.session_state.populator.read_students_to_accommodate(st.session_state.occupant_data)
#         st.session_state.populator.refresh_df_students_to_accommodate()
#         st.write("File processing complete")

#     st.session_state.file_processed = True

# def get_page():
#     return st.session_state.page


# # def render_page():
# #     page = get_page()
# #     if page == "Populator Page":
# #         populator_page()

# # WITH NEW PAGE
# def render_page():
#     page = get_page()
#     if page == "Populator Page":
#         populator_page()
#     elif page == "Dormitory Table":
#         dormitory_table_page()

# # def render_sidebar():
# #     st.sidebar.title("Sidebar")
# #     options = ["Populator Page"]
# #     page = st.sidebar.selectbox("Select a page", options)

# #     if page != get_page():
# #         st.session_state.page = page

# # WITH NEW PAGE
# def render_sidebar():
#     st.sidebar.title("Sidebar")
#     options = ["Populator Page", "Dormitory Table"]
#     page = st.sidebar.selectbox("Select a page", options)

#     if page != get_page():
#         st.session_state.page = page

# def populator_page():
#     st.title("Populator Page")

#     # Create two columns to center sub-headers and file uploaders 
#     col1, col2 = st.columns(2) 
#     # First sub-header and file uploader for room occupancy data 
#     with col1: 
#         st.header("Заполненность комнат") 
#         st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)

#     # Second sub-header and file uploader for list of occupants 
#     with col2: 
#         st.header("Список заселяемых") 
#         st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"], on_change=callback_odataUpload) 

#     # Add button to submit uploaded files 
#     upload = st.button("Загрузить", key="upload", on_click= callbackUpload) 
#     # Handle button click event        
#     if st.session_state.upload_clicked: 
#         # if not st.session_state.build:
#         #     st.error("Please build dormitory first")
#         # if st.session_state.room_data is not None: 
#         #     st.write("Первый файл сохранен")         
#         if st.session_state.occupant_data is not None: 
#             st.write("Второй файл сохранен") 
#         else: 
#             st.error("Please upload the file 'Список заселяемых'") 
        
#         if st.session_state.occupant_data:
#                 file_processing()
#                 populate_details()

# # NEW PAGE 
# def dormitory_table_page():
#     st.title("Current Dormitory State")
#     st.write("Below is the current state of the dormitory:")

#     df = fetch_dormitory_data()

#     block_filter = st.multiselect("Filter by Block", options=df['Block'].unique(), default=df['Block'].unique())
#     gender_filter = st.multiselect("Filter by Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
#     empty_filter = st.checkbox("Show only empty rooms")
#     partially_empty_filter = st.multiselect("Show rooms with specific number of students", options=range(1, 5), default=[])

#     filtered_df = apply_filters(df, block_filter, gender_filter, empty_filter, partially_empty_filter)
    
#     st.dataframe(filtered_df)

#     st.write(f"Number of selected rooms: {len(filtered_df)}")


# def main():
#     init_session_state()
#     render_sidebar()
#     render_page()

# main()



# STABLE VERSION
# import streamlit as st
# import pandas as pd
# from populator_refactored import Populator
# from models_refactored import Block, Room, Student, Dormitory
# from io import BytesIO

# blocks: list['Block'] = []

# def get_more_blocks(excel_file) -> dict[int, list[int]]:
#     df = pd.read_excel(excel_file)
#     df = df.iloc[:-1,:] # last row is total
#     df['№ комнаты'] = df['№ комнаты'].astype(int) # convert to int
#     df = df.groupby('Здание').agg({'№ комнаты': list})
#     new_blocks = {}
#     for block in df.index:
#         new_blocks[int(block[5:])] = df.loc[block, '№ комнаты']
    
#     return new_blocks

# def build_dormitory():
#     if not st.session_state.build:
#         blocks_ref = {}
#         for block in st.session_state.blocks:
#             # ПОМЕНЯЯЯЯЯЯЯЯЯЯЯТЬ
#             blocks_ref[block.blockID] = Dormitory.Block(block.blockID, block.rooms, block.places)
#         st.session_state.nu = Dormitory(blocks_ref, st.session_state.excluded_data) # dorm object 'nu'
#         print(st.session_state.nu)  # выдает в консоле все данные дорма (только 1 раз)
#     st.session_state.build = True  

# # Define the Block class
# class Block:
#     def __init__(self, blockID : int, rooms : list[int], places: int):
#         self.blockID = blockID
#         self.rooms = rooms
#         self.places = places
#         self.mutable = True


# def init_session_state():
#     st.set_page_config(layout="wide")
#     # Initialize session state
#     if 'populate_clicked' not in st.session_state:
#         st.session_state.populate_clicked = False
#     if 'get_rooms_clicked' not in st.session_state:
#         st.session_state.get_rooms_clicked = False
#     if 'get_students_clicked' not in st.session_state:
#         st.session_state.get_students_clicked = False
#     if 'configured_blocks' not in st.session_state:
#         st.session_state.configured_blocks = []
#     if 'generate' not in st.session_state:
#         st.session_state.generate = False
#     if 'build' not in st.session_state:
#         st.session_state.build = False
#     if 'blocks' not in st.session_state:
#         st.session_state.blocks = []
#     if 'page' not in st.session_state:
#         st.session_state.page = "Dormitory Generator" 
#     if 'my_slider_value' not in st.session_state:
#         st.session_state.my_slider_value = (22, 27)
#     if "addBlock_button_clicked" not in st.session_state:
#         st.session_state.addBlock_button_clicked = False
#     if "addBlocks_button_clicked" not in st.session_state:
#         st.session_state.addBlocks_button_clicked = False
#     if "newblockID" not in st.session_state:
#         st.session_state.newblockID = 0
#     if "upload_clicked" not in st.session_state:
#         st.session_state.upload_clicked = False
#     if "room_data_uploaded" not in st.session_state:
#         st.session_state.room_data_uploaded = False
#     if "occupants_data_uploaded" not in st.session_state:
#         st.session_state.occupants_data_uploaded = False
#     if 'custom_blocks' not in st.session_state:
#         st.session_state.custom_blocks = None
#     if 'excluded_data' not in st.session_state:
#         st.session_state.excluded_data = None
#     if 'paired_roomates' not in st.session_state:
#         st.session_state.paired_roomates = False
#     if 'settled_roomates' not in st.session_state:
#         st.session_state.settled_roomates = False
#     if 'file_processed' not in st.session_state:
#         st.session_state.file_processed = False

# def callbackUpload():
#     st.session_state.upload_clicked = True

# def callback_rdataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.room_data_uploaded = True

# def callback_odataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.occupants_data_uploaded = True

# def callbackAddBlock():
#     st.session_state.addBlock_button_clicked = True

# def callbackRemoveBlock(block):
#     pass

# def callbackAddBlocks():
#     st.session_state.addBlocks_button_clicked = True
    
# def callbackGenerate():
#     st.session_state.generate = True

# def callbackSlider():
#     st.session_state.generate = False
#     reset_dormitory()

# def reset_dormitory():
#     for block in blocks:
#         reset_block(block)
#     blocks.clear()
#     st.session_state.blocks.clear()

# def reset_block(block):
#     st.session_state.pop(block.blockID, None)
    

# # Generate dormitory based on block range
# def generate_dormitory(block_range):
#     # Initialize blocks within the given range
#     for blockID in range(block_range[0], block_range[1] + 1):
#         block = Block(blockID, True, (2, 12), 28, 2)
#         blocks.append(block)
#         if block.blockID not in st.session_state:
#             st.session_state[block.blockID] = block
#     return blocks

# def generate_dormitory_fixed(block_range : tuple[int, int], floors_range : tuple[int, int], rooms_range : int):
#     for blockID in range(block_range[0], block_range[1] + 1):
#         # Create list of rooms in the block with consideration of the number of floors and rooms per floor. Floor indicates first part of the room number, room index at the floor indicates second part of the room number
#         rooms: list[int] = generate_rooms(floors_range, (1, rooms_range))
#         if(blockID != 22):
#             block = Block(blockID, rooms, 2)
#         else:
#             block = Block(blockID, rooms, 3)
#         blocks.append(block)
#         if block.blockID not in st.session_state:
#             st.session_state[block.blockID] = block
#     return blocks

# # Generate rooms based on floor range and room range
# def generate_rooms(floor_range: tuple[int, int], room_range: tuple[int, int]):
#     rooms: list[int] = []
#     for floor in range(floor_range[0], floor_range[1] + 1):
#         for room in range(room_range[0], room_range[1] + 1):
#             rooms.append(floor * 100 + room)
#     return rooms

# # Page 1: Dormitory Generator
# def dormitory_generator_page():
#     st.title("Dormitory Generator")
#     #st.write("Welcome to the Dormitory Generator page!")
#     # Add a double-ended slider representing a range between 22 and 27
#     # slider_value = st.slider("Select a block range", min_value=22, max_value=27, value=st.session_state.my_slider_value, on_change=callbackSlider, key = "block_range_slider")
#     # st.session_state.my_slider_value = slider_value

#     st.header("Dormitory presets")
#     # Double Input Fields for block range, floor range, room range, and number of places
#     input_field_container = st.container()
#     with input_field_container:
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             # move text down
#             st.subheader("Block range")
#             st.subheader("Floor range")
#         with col2:
#             block_range_min = st.number_input("Min", min_value=19, max_value=28, value=22, step=1, key="block_range_min")
#             floor_range_min = st.number_input("Min", min_value=1, max_value=12, value=1, step=1, key="floor_range_min")
#         with col3:
#             block_range_max = st.number_input("Max", min_value=19, max_value=28, value=28, step=1, key="block_range_max")
#             floor_range_max = st.number_input("Max", min_value=1, max_value=12, value=12, step=1, key="floor_range_max")
#         rooms_per_floor = st.number_input("Rooms per floor", min_value=1, max_value=28, value=28, step=1, key="rooms_per_floor")
            
#     # Add a button to generate the dormitory
#     generate = st.button("Generate", help="Generate the dormitory configuration", on_click=callbackGenerate)
#     st.markdown("---")
#     blocks = []
#     if generate:
#         #Deprecated# blocks = generate_dormitory(st.session_state.my_slider_value)
#         blocks = generate_dormitory_fixed(block_range=(block_range_min, block_range_max), floors_range=(floor_range_min, floor_range_max), rooms_range=rooms_per_floor)
#         st.session_state.blocks = blocks
#     blocks = st.session_state.blocks
#     blocks.sort(key=lambda x: x.blockID)
#     # remove blocks that are in st.session_state.blocks_to_remove
#     # if "blocks_to_remove" in st.session_state:
#     #     for block in st.session_state.blocks_to_remove:
#     #         blocks.remove(block)
#     #         reset_block(block)
#     #     st.session_state.blocks_to_remove.clear()
        
#     # Render the generated dormitory
#     st.header("Сonfiguration")
#     for block in blocks:
#         # Use the block ID as the expand trigger
#         suffix = " Custom " if not block.mutable else ""
#         expander = st.expander("Block "+str(block.blockID)+ suffix, expanded=False)
#         with expander:
#             # Use input fields to edit the fields of each block
#             #---Deprecated---# block.active = st.checkbox("Active", value=st.session_state[block.blockID].active, key="active"+str(block.blockID))
#             #---Deprecated---# if not block.active:
#             #---Deprecated---#     continue
#             if block.mutable:
#                 floor_range : tuple[int, int] = st.slider("Floors", min_value=2, max_value=12, value = (floor_range_min, floor_range_max), key="floor"+str(block.blockID))
#                 room_range: int = st.number_input("Rooms per Floor", min_value=1, max_value=28, value = rooms_per_floor, key="room"+str(block.blockID))
#                 block.rooms = generate_rooms(floor_range, (1, room_range))
#                 block.places = st.number_input("Students per Room", min_value=1, max_value=4, value=st.session_state[block.blockID].places, key="place"+str(block.blockID))
#             else:
#                 st.write("Rooms: ", block.rooms)
#                 # change expander title text to include "(custom)" if the block is not mutable
                
                
#             # add a button to remove this block from the blocks list
#             removeBlock = st.button("Remove Block", help="Remove this block from the dormitory", key="remove"+str(block.blockID))
#             if removeBlock:
#                 st.session_state.blocks.remove(block)
#                 st.experimental_rerun()

#     #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#     st.markdown("---")      
#     button_container = st.container()
#     with button_container:
#         col1, col2 = st.columns(2)
#         with col1:
#             subcol1, subcol2 = st.columns(2)
#             with subcol1:
#                 # file upload to get new block data
#                 st.session_state.custom_blocks = st.file_uploader("Upload Excel file of blocks data", type=["xls", "xlsx"])
#                 if st.session_state.custom_blocks is not None: 
#                     st.write("Custom blocks uploaded")
#             with subcol2:
#                 # button that converts obtained data into a new blocks 
#                 addBlocks = st.button("Add Custom Blocks", help="Add custom blocks to the dormitory", on_click=callbackAddBlocks)
#                 if addBlocks and st.session_state.custom_blocks is not None:
#                     blocks_dic = get_more_blocks(st.session_state.custom_blocks)
#                     # traverse the dictionary (key = blockID, value = rooms) and create new blocks and add them to the session state
#                     for blockID, rooms in blocks_dic.items():
#                         newblock = Block(blockID, rooms, 4)
#                         newblock.mutable = False
#                         st.session_state[newblock.blockID] = newblock
#                         # traverse the blocks comparing blockIDs and at match with newblock.blockID replace the old block with the new one
#                         for oldBlock in blocks:
#                             if oldBlock.blockID == newblock.blockID:
#                                 st.session_state.blocks.remove(oldBlock)
#                         st.session_state.blocks.append(newblock)
#                     st.experimental_rerun()
#         # TODO: Adapt code to new block class
#         # TODO: Remove block button
#         # TODO: Custom blocks imutable
#         with col2:
#             subcol1, subcol2 = st.columns(2)
#             with subcol1:
#                 addBtn_container = st.container()
#                 add = addBtn_container.button("Add Block", help="Add a new block to the dormitory", on_click=callbackAddBlock)
#                 if add:
#                     invaid = False
#                     for block in blocks:
#                         if block.blockID == st.session_state.newblockID:
#                             addBtn_container.error("Block already exists")
#                             invaid = True
#                     if not invaid:
#                         newblock = Block(st.session_state.newblockID, generate_rooms((2, 12), (1, 28)), 2)
#                         st.session_state[newblock.blockID] = newblock
#                         st.session_state.blocks.append(newblock)
#                         st.experimental_rerun()
#             with subcol2:
#                 st.session_state.newblockID = st.number_input(label="tmp",help="Enter block ID to add",label_visibility= "collapsed",min_value=11, max_value=27, key = "AddBlockInp")
#     #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#     st.markdown("---")      
#     # Add a "Save" button that updates the dormitory data
#     if st.button("Save", help="Save the dormitory configuration"):
#         # Perform some action for Button 1
#         st.write("Configuration saved")
#         for block in blocks:
#             st.session_state[block.blockID] = block
#     st.markdown("---")      
#     EXCEPTEDROOMS_COLUMNS = ["Block", "Room"]
#     st.subheader("Список игнорируемых комнат(xls, xlsx)") 
#     st.session_state.excluded_data = st.file_uploader("Upload Excel file", type=["xls", "xlsx"]) 
#     if st.session_state.excluded_data is not None: 
#         st.write("Excluded rooms uploaded")
        
#     build = st.button("Build",help= "Build dormitory", on_click=build_dormitory)
#     if build:
#         st.write("Dormitory built")
        
# # Page 2: Populator Page
# def populator_page():
#     st.title("Populator Page")

#     # Create two columns to center sub-headers and file uploaders 
#     col1, col2= st.columns(2) 
#     # First sub-header and file uploader for room occupancy data 
#     with col1: 
#         st.header("Заполненность комнат") 
#         st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)

#     # Second sub-header and file uploader for list of occupants 
#     with col2: 
#         st.header("Список заселяемых") 
#         st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"], on_change=callback_odataUpload) 

#     # Add button to submit uploaded files 
#     upload = st.button("Загрузить", key="upload", on_click= callbackUpload) 
#     # Handle button click event        
#     if st.session_state.upload_clicked: 
#         if not st.session_state.build:
#             st.error("Please build dormitory first")
#         if st.session_state.room_data is not None: 
#             st.write("Первый файл сохранен")         
#         # else: 
#         #     st.error("Please upload the file 'Заполненность комнат'") 

#         if st.session_state.occupant_data is not None: 
#             st.write("Второй файл сохранен") 
#         else: 
#             st.error("Please upload the file 'Список заселяемых'") 
        
#         if st.session_state.build:
#             if st.session_state.occupant_data:
#                 file_processing()
#                 populate_details()


# def populate_details():
#     st.markdown("---")
#     # button_container = st.container
#     st.write("Create student pairs") 
#     if st.button("Pair", help = "Create student pairings", on_click = pair_roomates, key = 'pair_roomates'):
#         st.write("Student pairs created")
#     # st.session_state.populator.student_ids_to_destroy
#     st.markdown("---")
#     st.write("Settle roomates to the already accomodated") 
#     if st.button("Подселить", help = "Подселить руммейтов к живущим", on_click = settle_roomates, key = 'settle_roomates'):
#         st.write("Roomates settled")
#     st.markdown("---")
#     with st.form(key="rooms"): 
#         col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1]) 
#         col1.multiselect("List of blocks", options=st.session_state.nu.rooms.keys(),default=st.session_state.nu.rooms.keys(), key = "block_list_room")
#         col2.multiselect("List of floors", options=range(2, 13),default=range(2, 13), key = 'floor_list_room') 
#         col3.multiselect("Occupancy", options=[0,1,2,3,4], default=[0,1,2,3,4], key = 'occupancy_room')
#         col4.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key = 'gender_room')
#         col5.text_input("Room", placeholder="Example: 903", key = '_room')
#         st.form_submit_button("Get Rooms", on_click=get_rooms) 
#         if st.session_state.get_rooms_clicked:
#             st.dataframe(st.session_state.filtered_rooms_df)
#     with st.form(key="students"): 
#         col1, col2, col3, col4= st.columns(4) 
#         col1.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_student')
#         col2.multiselect("Degree", options=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), default=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), key = 'degree_student') 
#         col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].unique(), key = 'year_student')
#         col4.text_input("Student ID", placeholder="Comma-Sep, Example: 202085777", key = '_student')
#         st.form_submit_button("Get Students", on_click=get_students)
#         if st.session_state.get_students_clicked:
#             st.dataframe(st.session_state.filtered_students_df)
    
#     st.button("Populate", help = "Populate", on_click = populate, key = 'populate')
#     if st.session_state.populate_clicked:
#         st.write("Populated") 
#         upload_df = get_upload_df()
#         buffer = BytesIO()
#         with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#             # Write each dataframe to a different worksheet.
#             upload_df.to_excel(writer, sheet_name='Sheet1', index=False)
    

#             # Close the Pandas Excel writer and output the Excel file to the buffer
#             writer.close()

#             st.download_button(
#                 label="Получить файл заливки",
#                 data=buffer,
#                 help = "Скачать CSV файл заливки",
#                 file_name='Файл_заливки.xlsx',
#                 mime="application/vnd.ms-excel"
#             )
#         # st.download_button(label = "Получить файл заливки", data = csv, help = "Скачать CSV файл заливки", file_name='Файл_заливки.csv', mime='text/csv')

# def get_upload_df():
#     return st.session_state.populator.to_upload_file()

# def populate():
#     if st.session_state.get_rooms_clicked and st.session_state.get_students_clicked:
#         st.session_state.populate_clicked = True
#         st.session_state.populator.populate(st.session_state.filtered_students_list, st.session_state.filtered_rooms_list)     
#     else:
#         st.error("Please get rooms and students first")

# def get_rooms():
#     st.session_state.get_rooms_clicked = True
#     block_list = st.session_state.block_list_room
#     floor_list = st.session_state.floor_list_room
#     occupancy_list = st.session_state.occupancy_room
#     gender = st.session_state.gender_room
#     room = st.session_state._room
#     if room != "":
#         room = int(room)
#     else:
#         room = None
#     st.session_state.filtered_rooms_df, st.session_state.filtered_rooms_list = st.session_state.populator.get_rooms(block_list, floor_list, occupancy_list, gender, room)

# def get_students():
#     st.session_state.get_students_clicked = True
#     gender = st.session_state.gender_student
#     degree = st.session_state.degree_student
#     year = st.session_state.year_student
#     student_ids = st.session_state._student
#     if student_ids == "":
#         student_ids = None
#     else:
#         student_ids = [int(id) for id in student_ids.split(",")]
#     st.session_state.filtered_students_df, st.session_state.filtered_students_list = st.session_state.populator.filter_students(gender, degree, year, student_ids)


# def pair_roomates():
#     if not st.session_state.paired_roomates:
#         st.session_state.populator.match_roommates()
#     st.session_state.paired_roomates = True

# def settle_roomates():
#     if not st.session_state.settled_roomates:
#         st.session_state.populator.assign_roommate()
#     st.session_state.settled_roomates = True

# def file_processing():
#     if not st.session_state.file_processed:
#         st.session_state.populator = Populator(st.session_state.nu) # призывается популятор
#         # TODO: add condition to skip
#         if st.session_state.room_data is not None:
#             st.session_state.populator.update_dorm(st.session_state.room_data)
#         # --------------------
#         st.session_state.populator.read_students_to_accommodate(st.session_state.occupant_data)
#         st.session_state.populator.refresh_df_students_to_accommodate()
#         st.write("File processing complete")

#     st.session_state.file_processed = True

# def get_page():
#     return st.session_state.page

# def render_page():
#     page = get_page()
#     if page == "Dormitory Generator":
#         dormitory_generator_page()    
#     elif page == "Populator Page":
#         populator_page()

# def render_sidebar():
#     st.sidebar.title("Sidebar")
#     options = ["Dormitory Generator", "Populator Page" ]
#     page = st.sidebar.selectbox("Select a page", options)

#     # Update the page in session state when selectbox value changes
#     if page != get_page():
#         st.session_state.page = page

# def main():
#     init_session_state()
#     render_sidebar()
#     render_page()

# main()



# МБ НЕНУЖНО
# import streamlit as st
# import pandas as pd
# import psycopg2
# from populator_refactored import Populator
# from models_refactored import Dormitory, Student
# from io import BytesIO

# def fetch_dormitory_data():
#     conn = psycopg2.connect(dbname="dormitory_db", user="nurlantr", password="12345", host="localhost", port="5432")
#     query = "SELECT * FROM dormitory ORDER BY block, room"
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# def initialize_dormitory(df):
#     dormitory = Dormitory()
#     for _, row in df.iterrows():
#         block = row['block']
#         room = row['room']
#         gender = row['gender']
#         students = row['students']
#         student_ids = [int(sid) for sid in students.split(', ')] if students else []
#         for sid in student_ids:
#             if sid not in dormitory.rooms[block][room].students:
#                 new_student = Student(sid)  # Assuming you have a way to fetch or create a Student object
#                 dormitory.rooms[block][room].addStudent(new_student)
#         dormitory.rooms[block][room].gender = gender
#     return dormitory

# def init_session_state():
#     st.set_page_config(layout="wide")
#     if 'populate_clicked' not in st.session_state:
#         st.session_state.populate_clicked = False
#     if 'get_rooms_clicked' not in st.session_state:
#         st.session_state.get_rooms_clicked = False
#     if 'get_students_clicked' not in st.session_state:
#         st.session_state.get_students_clicked = False
#     if 'configured_blocks' not in st.session_state:
#         st.session_state.configured_blocks = []
#     if 'generate' not in st.session_state:
#         st.session_state.generate = False
#     if 'build' not in st.session_state:
#         st.session_state.build = False
#     if 'blocks' not in st.session_state:
#         st.session_state.blocks = []
#     if 'page' not in st.session_state:
#         st.session_state.page = "Populator Page"
#     if 'my_slider_value' not in st.session_state:
#         st.session_state.my_slider_value = (22, 27)
#     if "addBlock_button_clicked" not in st.session_state:
#         st.session_state.addBlock_button_clicked = False
#     if "addBlocks_button_clicked" not in st.session_state:
#         st.session_state.addBlocks_button_clicked = False
#     if "newblockID" not in st.session_state:
#         st.session_state.newblockID = 0
#     if "upload_clicked" not in st.session_state:
#         st.session_state.upload_clicked = False
#     if "room_data_uploaded" not in st.session_state:
#         st.session_state.room_data_uploaded = False
#     if "occupants_data_uploaded" not in st.session_state:
#         st.session_state.occupants_data_uploaded = False
#     if 'custom_blocks' not in st.session_state:
#         st.session_state.custom_blocks = None
#     if 'excluded_data' not in st.session_state:
#         st.session_state.excluded_data = None
#     if 'paired_roomates' not in st.session_state:
#         st.session_state.paired_roomates = False
#     if 'settled_roomates' not in st.session_state:
#         st.session_state.settled_roomates = False
#     if 'file_processed' not in st.session_state:
#         st.session_state.file_processed = False


# def callbackUpload():
#     st.session_state.upload_clicked = True


# def file_processing():
#     if not st.session_state.file_processed:
#         dormitory_data = fetch_dormitory_data()
#         dormitory = initialize_dormitory(dormitory_data)
#         st.session_state.populator = Populator(dormitory)
#         if st.session_state.room_data is not None:
#             st.session_state.populator.update_dorm(st.session_state.room_data)
#         st.session_state.populator.read_students_to_accommodate(st.session_state.occupant_data)
#         st.session_state.populator.refresh_df_students_to_accommodate()
#         st.write("File processing complete")

#     st.session_state.file_processed = True

# def get_upload_df():
#     return st.session_state.populator.to_upload_file()

# def populate():
#     if st.session_state.get_rooms_clicked and st.session_state.get_students_clicked:
#         st.session_state.populate_clicked = True
#         st.session_state.populator.populate(st.session_state.filtered_students_list, st.session_state.filtered_rooms_list)
#     else:
#         st.error("Please get rooms and students first")

# def get_rooms():
#     st.session_state.get_rooms_clicked = True
#     block_list = st.session_state.block_list_room
#     floor_list = st.session_state.floor_list_room
#     occupancy_list = st.session_state.occupancy_room
#     gender = st.session_state.gender_room
#     room = st.session_state._room
#     if room != "":
#         room = int(room)
#     else:
#         room = None
#     st.session_state.filtered_rooms_df, st.session_state.filtered_rooms_list = st.session_state.populator.get_rooms(block_list, floor_list, occupancy_list, gender, room)

#     st.session_state.filtered_rooms_df = st.session_state.filtered_rooms_df.sort_values(by=['Block', 'Room'])
#     st.dataframe(st.session_state.filtered_rooms_df)

# def get_students():
#     st.session_state.get_students_clicked = True
#     gender = st.session_state.gender_student
#     degree = st.session_state.degree_student
#     year = st.session_state.year_student
#     student_ids = st.session_state._student
#     if student_ids == "":
#         student_ids = None
#     else:
#         student_ids = [int(id) for id in student_ids.split(",")]
#     st.session_state.filtered_students_df, st.session_state.filtered_students_list = st.session_state.populator.filter_students(gender, degree, year, student_ids)

# def pair_roomates():
#     if not st.session_state.paired_roomates:
#         st.session_state.populator.match_roommates()
#     st.session_state.paired_roomates = True

# def settle_roomates():
#     if not st.session_state.settled_roomates:
#         st.session_state.populator.assign_roommate()
#     st.session_state.settled_roomates = True

# def populator_page():
#     st.title("Populator Page")

#     col1, col2= st.columns(2) 
#     with col1: 
#         st.header("Заполненность комнат") 
#         st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)

#     with col2: 
#         st.header("Список заселяемых") 
#         st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"], on_change=callback_odataUpload) 

#     upload = st.button("Загрузить", key="upload", on_click= callbackUpload) 
        
#     if st.session_state.upload_clicked: 
#         # if not st.session_state.build:
#         #     st.error("Please build dormitory first")
#         if st.session_state.room_data is not None: 
#             st.write("Первый файл сохранен")         
#         if st.session_state.occupant_data is not None: 
#             st.write("Второй файл сохранен") 
#         else: 
#             st.error("Please upload the file 'Список заселяемых'") 
        
#         # if st.session_state.build:
#         #     if st.session_state.occupant_data:
#         #         file_processing()
#         #         populate_details()
#         if st.session_state.occupant_data:
#             file_processing()
#             populate_details()

# def populate_details():
#     st.markdown("---")
#     st.write("Create student pairs") 
#     if st.button("Pair", help = "Create student pairings", on_click = pair_roomates, key = 'pair_roomates'):
#         st.write("Student pairs created")
#     st.markdown("---")
#     st.write("Settle roommates to the already accommodated") 
#     if st.button("Подселить", help = "Подселить руммейтов к живущим", on_click = settle_roomates, key = 'settle_roomates'):
#         st.write("Roommates settled")
#     st.markdown("---")
#     with st.form(key="rooms"): 
#         col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1]) 
#         col1.multiselect("List of blocks", options=st.session_state.nu.rooms.keys(),default=st.session_state.nu.rooms.keys(), key = "block_list_room")
#         col2.multiselect("List of floors", options=range(2, 13),default=range(2, 13), key = 'floor_list_room') 
#         col3.multiselect("Occupancy", options=[0,1,2,3,4], default=[0,1,2,3,4], key = 'occupancy_room')
#         col4.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key = 'gender_room')
#         col5.text_input("Room", placeholder="Example: 903", key = '_room')
#         st.form_submit_button("Get Rooms", on_click=get_rooms) 
#         if st.session_state.get_rooms_clicked:
#             st.dataframe(st.session_state.filtered_rooms_df)
#     with st.form(key="students"): 
#         col1, col2, col3, col4= st.columns(4) 
#         col1.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_student')
#         col2.multiselect("Degree", options=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), default=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), key = 'degree_student') 
#         col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].unique(), key = 'year_student')
#         col4.text_input("Student ID", placeholder="Comma-Sep, Example: 202085777", key = '_student')
#         st.form_submit_button("Get Students", on_click=get_students)
#         if st.session_state.get_students_clicked:
#             st.dataframe(st.session_state.filtered_students_df)
    
#     st.button("Populate", help = "Populate", on_click = populate, key = 'populate')
#     if st.session_state.populate_clicked:
#         st.write("Populated") 
#         upload_df = get_upload_df()
#         buffer = BytesIO()
#         with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#             upload_df.to_excel(writer, sheet_name='Sheet1', index=False)
#             writer.close()
#             st.download_button(
#                 label="Получить файл заливки",
#                 data=buffer,
#                 help = "Скачать CSV файл заливки",
#                 file_name='Файл_заливки.xlsx',
#                 mime="application/vnd.ms-excel"
#             )
# def callback_rdataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.room_data_uploaded = True

# def callback_odataUpload():
#     st.session_state.upload_clicked = False
#     st.session_state.occupants_data_uploaded = True

# def get_page():
#     return st.session_state.page

# def render_page():
#     page = get_page()
#     if page == "Populator Page":
#         populator_page()

# def render_sidebar():
#     st.sidebar.title("Sidebar")
#     options = ["Populator Page"]
#     page = st.sidebar.selectbox("Select a page", options)
#     if page != get_page():
#         st.session_state.page = page

# def main():
#     init_session_state()
#     render_sidebar()
#     render_page()

# main()

