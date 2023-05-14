import streamlit as st
import pandas as pd 
from populator_refactored import Populator
from models_refactored import Dormitory
from io import BytesIO

blocks: list['Block'] = []

def build_dormitory():
    st.session_state.build = True
    
    # all functions of processing
    blocks_ref = {}
    for block in blocks:
        if block.active:   
            blocks_ref[block.blockID] = Dormitory.Block(block.blockID, list(block.floors), [1, block.rooms], block.places)
    st.session_state.nu = Dormitory(blocks_ref, st.session_state.excluded_data)
    st.write(st.session_state.nu)
    print(st.session_state.nu)

# Define the Block class
class Block:
    def __init__(self, blockID, active, floors, rooms, places):
        self.blockID = blockID
        self.active = active
        self.floors = floors
        self.rooms = rooms
        self.places = places



def init_session_state():
    st.set_page_config(layout="wide")
    # Initialize session state
    if 'configured_blocks' not in st.session_state:
        st.session_state.configured_blocks = []
    if 'generate' not in st.session_state:
        st.session_state.generate = False
    if 'build' not in st.session_state:
        st.session_state.build = False
    if 'blocks' not in st.session_state:
        st.session_state.blocks = []
    if 'page' not in st.session_state:
        st.session_state.page = "Dormitory Generator" 
    if 'my_slider_value' not in st.session_state:
        st.session_state.my_slider_value = (22, 27)
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False
    if "newblockID" not in st.session_state:
        st.session_state.newblockID = 0
    if "upload_clicked" not in st.session_state:
        st.session_state.upload_clicked = False
    if "room_data_uploaded" not in st.session_state:
        st.session_state.room_data_uploaded = False
    if 'excluded_data' not in st.session_state:
        st.session_state.excluded_data = None

def callbackUpload():
    st.session_state.upload_clicked = True

def callback_rdataUpload():
    st.session_state.room_data_uploaded = True

def callbackAdd():
    st.session_state.button_clicked = True

def callbackGenerate():
    st.session_state.generate = True

def callbackSlider():
    st.session_state.generate = False
    reset_dormitory()

def reset_dormitory():
    for block in blocks:
        reset_block(block)
    blocks.clear()
    st.session_state.blocks.clear()

def reset_block(block):
    st.session_state.pop(block.blockID, None)

@st.cache_data
def load_data(file): 
    data = pd.read_excel(BytesIO(file.read()), engine="openpyxl")
    return data

# Generate dormitory based on block range
def generate_dormitory(block_range):
    # Initialize blocks within the given range
    for blockID in range(block_range[0], block_range[1] + 1):
        block = Block(blockID, True, (2, 12), 28, 2)
        blocks.append(block)
        if block.blockID not in st.session_state:
            st.session_state[block.blockID] = block

    return blocks

# Page 1: Dormitory Generator
def dormitory_generator_page():
    st.title("Dormitory Generator")
    st.write("Welcome to the Dormitory Generator page!")
    # Add a double-ended slider representing a range between 22 and 27
    slider_value = st.slider("Select a block range", min_value=22, max_value=27, value=st.session_state.my_slider_value, on_change=callbackSlider, key = "block_range_slider")
    st.session_state.my_slider_value = slider_value

    # Add a button to generate the dormitory
    generate = st.button("Generate", help="Generate the dormitory configuration", on_click=callbackGenerate)
    st.markdown("---")
    if st.session_state.generate:
        if generate:
            reset_dormitory()
        blocks = generate_dormitory(st.session_state.my_slider_value)
        blocks += st.session_state.blocks
        blocks.sort(key=lambda x: x.blockID)

        # Render the generated dormitory
        st.header("Сonfiguration")
        for block in blocks:
            # Use the block ID as the expand trigger
            expander = st.expander("Block "+str(block.blockID), expanded=False, )
            with expander:
                # Use input fields to edit the fields of each block
                block.active = st.checkbox("Active", value=st.session_state[block.blockID].active, key="active"+str(block.blockID))
                if not block.active:
                    continue
                block.floors = st.slider("Floors", min_value=2, max_value=12, value=st.session_state[block.blockID].floors, key="floor"+str(block.blockID))
                block.rooms = st.number_input("Rooms per Floor", min_value=1, max_value=28, value=st.session_state[block.blockID].rooms, key="room"+str(block.blockID))
                block.places = st.number_input("Students per Room", min_value=1, max_value=4, value=st.session_state[block.blockID].places, key="place"+str(block.blockID))

        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        st.markdown("---")      
        button_container = st.container()
        with button_container:
            col1, col2 = st.columns(2)
            with col1:
                # Add a "Save" button that updates the dormitory data
                if st.button("Save", help="Save the dormitory configuration"):
                    # Perform some action for Button 1
                    st.write("Configuration saved")
                    for block in blocks:
                        st.session_state[block.blockID] = block
            with col2:
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    addBtn_container = st.container()
                    add = addBtn_container.button("Add Block", help="Add a new block to the dormitory", on_click=callbackAdd)
                    if add:
                        invaid = False
                        for block in blocks:
                            if block.blockID == st.session_state.newblockID:
                                addBtn_container.error("Block already exists")
                                invaid = True
                        if not invaid:
                            newblock = Block(st.session_state.newblockID, True, (2, 12), 28, 2)
                            st.session_state[newblock.blockID] = newblock
                            st.session_state.blocks.append(newblock)
                            st.experimental_rerun()
                with subcol2:
                    st.session_state.newblockID = st.number_input(label="tmp",help="Enter block ID to add",label_visibility= "collapsed",min_value=19, max_value=27, key = "AddBlockInp")
        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        st.markdown("---")      
        EXCEPTEDROOMS_COLUMNS = ["Block", "Room"]
        st.subheader("Список игнорируемых комнат(xls, xlsx)") 
        st.session_state.excluded_data = st.file_uploader("Upload Third Excel file", type=["xls", "xlsx"]) 
        if st.session_state.excluded_data is not None: 
            st.write("Excluded rooms uploaded")
            
        st.button("Build",help= "Build dormitory", on_click=build_dormitory)
        
        
# Page 2: Populator Page
def populator_page():
    st.title("Populator Page")
    ROOM_COLUMNS = ["Block", "Room", "ID", "Gender"] 
    OCCUPANT_COLUMNS = ["ID", "Gender", "Degree", "Year", "Roomate1", "Roomate2", "Roomate3"] 

    # Define flags for mandatory files in order to use it in the last step 
    flagRooms = False 
    flagOccupants = False 
    # Create two columns to center sub-headers and file uploaders 
    col1, col2= st.columns(2) 
    # First sub-header and file uploader for room occupancy data 
    with col1: 
        st.header("Заполненность комнат") 
        st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)

    # Second sub-header and file uploader for list of occupants 
    with col2: 
        st.header("Список заселяемых") 
        st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"]) 
                     
    # Add button to submit uploaded files 
    upload_button = st.button("Загрузить", key="upload", on_click= callbackUpload) 
    # Handle button click event 
    if upload_button: 
        if not st.session_state.build:
            st.error("Please build dormitory first")
        if st.session_state.room_data is not None: 
            st.write("Первый файл сохранен")         
        else: 
            st.error("Please upload the file 'Заполненность комнат'") 

        if st.session_state.occupant_data is not None: 
            st.write("Второй файл сохранен") 
        else: 
            st.error("Please upload the file 'Список заселяемых'") 
            
        if st.session_state.build:
            file_processing()
            populate_details()

def populate_details():
    st.markdown("---")
    # button_container = st.container
    st.write("Create student pairs") 
    st.button("Pair", help = "Create student pairings", on_click = pair_roomates)
    st.markdown("---")
    st.write("Settle roomates to the already accomodated") 
    st.button("Подселить", help = "Подселить руммейтов к живущим", on_click = settle_roomates)
    st.markdown("---")
    with st.form(key="rooms"): 
        col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1]) 
        col1.multiselect("List of blocks", options=st.session_state.nu.rooms.keys(),default=st.session_state.nu.rooms.keys(), key = "block_list_room")
        col2.multiselect("List of floors", options=range(2, 13),default=range(2, 13), key = 'floor_list_room') 
        col3.multiselect("Occupancy", options=[0,1,2,3,4], default=[0,1,2,3,4], key = 'occupancy_room')
        col4.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key = 'gender_room')
        col5.text_input("Room", placeholder="Example: 903", key = '_room')
        g_room = st.form_submit_button("Get Rooms", on_click=get_rooms) 
        if g_room:
            st.dataframe(st.session_state.filtered_rooms_df)
    with st.form(key="students"): 
        col1, col2, col3, col4= st.columns(4) 
        col1.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"], key='gender_student')
        col2.multiselect("Degree", options=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), default=st.session_state.populator.df_students_to_accommodate["Degree"].unique(), key = 'degree_student') 
        col3.multiselect("Year", options=st.session_state.populator.df_students_to_accommodate["Year"].unique(), default=st.session_state.populator.df_students_to_accommodate["Year"].unique(), key = 'year_student')
        col4.text_input("Student ID", placeholder="Comma-Sep, Example: 202085777", key = '_student')
        g_student = st.form_submit_button("Get Students", on_click=get_students)
        if g_student:
            st.dataframe(st.session_state.filtered_students_df)
        
def get_rooms():
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
    st.session_state.populator.match_roommates()

def settle_roomates():
    st.session_state.populator.assign_roomate()
        
def file_processing():
    st.session_state.populator = Populator(st.session_state.nu)
    st.session_state.populator.update_dorm(st.session_state.room_data)
    st.session_state.populator.read_students_to_accommodate(st.session_state.occupant_data)
    st.session_state.populator.refresh_df_students_to_accommodate()
    
def get_page():
    return st.session_state.page

def render_page():
    page = get_page()
    if page == "Dormitory Generator":
        dormitory_generator_page()    
    elif page == "Populator Page":
        populator_page()

def render_sidebar():
    st.sidebar.title("Sidebar")
    options = ["Dormitory Generator", "Populator Page" ]
    page = st.sidebar.selectbox("Select a page", options)

    # Update the page in session state when selectbox value changes
    if page != get_page():
        st.session_state.page = page

def main():
    init_session_state()
    render_sidebar()
    render_page()

main()