import streamlit as st
import pandas as pd 
from populator_refactored import Populator
from models_refactored import Dormitory
from io import BytesIO
blocks = []

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
    slider_value = st.slider("Select a block range", min_value=22, max_value=27, value=st.session_state.my_slider_value, on_change=callbackSlider)
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

    st.title("2. Uploading Data") 
    # Define flags for mandatory files in order to use it in the last step 
    flagRooms = False 
    flagOccupants = False 
    # Create two columns to center sub-headers and file uploaders 
    col1, col2= st.columns(2) 
    # First sub-header and file uploader for room occupancy data 
    with col1: 
        st.header("Заполненность комнат(xls, xlsx)") 
        st.session_state.room_data = st.file_uploader("Upload First Excel file", type=["xls", "xlsx"], on_change=callback_rdataUpload)
        if st.session_state.room_data is not None: 
            rooms_df = load_data(st.session_state.room_data)
            st.write(rooms_df)

    # Second sub-header and file uploader for list of occupants 
    with col2: 
        st.header("Список заселяемых(xls, xlsx)") 
        st.session_state.occupant_data = st.file_uploader("Upload Second Excel file", type=["xls", "xlsx"]) 
                     
    # Add button to submit uploaded files 
    upload_button = st.button("Загрузить", key="upload", on_click= callbackUpload) 
    # Handle button click event 
    if upload_button: 
        if st.session_state.room_data is not None: 
            st.write("Загружен файл", st.session_state.room_data)
            # Process room data file 
            rooms_df = load_data(st.session_state.room_data) 
            st.write(rooms_df)
            # Validate column names 
            if set(rooms_df.columns) == set(ROOM_COLUMNS): 
                flagRooms = True 
                st.write("Первый файл сохранен") 
                #ЗДЕСЬ ДОЛЖНА БЫТЬ ВЫЗВАНА ФУНКЦИЯ ЧТЕНИЯ ЗАНЯТЫХ КОМНАТ С АРГУМЕНТОМ room_df 
                # Call your function with the room data as argument 
            else: 
                st.error(f"Invalid columns in 'Заполненность комнат' file. Expected columns: {ROOM_COLUMNS}") 
        else: 
            st.error("Please upload the file 'Заполненность комнат'") 

        if st.session_state.occupant_data is not None: 
            # Process occupant data file 
            occupants_df = load_data(st.session_state.occupant_data)
            # Validate column names 
            if set(occupants_df.columns) == set(OCCUPANT_COLUMNS): 
                flagOccupants = True 
                st.write("Второй файл сохранен") 
                #А ЗДЕСЬ ДОЛЖНА БЫТЬ ВЫЗВАНА ФУНКЦИЯ ЧТЕНИЯ СПИСКА ЗАСЕЛЯЕМЫХ С АРУГМЕНТОМ occupants_df 
                # Call your function with the occupant data as argument 
            else: 
                st.error(f"Invalid columns in 'Список заселяемых' file. Expected columns: {OCCUPANT_COLUMNS}") 
        else: 
            st.error("Please upload the file 'Список заселяемых'") 

        file_processing()
    st.markdown("---")
    # button_container = st.container
    st.write("Create pairings and Settle the roomates")
    c1, c2 = st.columns(2)
    c1.button("Pair", help = "Create student pairings", on_click = pair_roomates)
    c2.button("Подселить", help = "Подселить руммейтов к живущим", on_click = settle_roomates)
    st.markdown("---")
    with st.form(key="rooms"): 
        col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1]) 
        col1.multiselect("List of blocks", options=range(st.session_state.my_slider_value[0] , st.session_state.my_slider_value[1]+1),default= range(st.session_state.my_slider_value[0] , st.session_state.my_slider_value[1]+1))
        col2.multiselect("List of floors", options=range(2, 13),default=range(2, 13)) 
        col5.text_input("Room", placeholder="Example: 903")
        col4.selectbox("Gender", options=["All", "Male", "Female"]) 
        col3.number_input("Occupancy", min_value=0, max_value=4, value=1) 
        st.form_submit_button("Get Rooms") 
 
    with st.form(key="students"): 
        degree_options = []
        col1, col2, col3, col4= st.columns(4) 
        col1.selectbox("Gender", options=["All", "Male", "Female"]) 
        col2.selectbox("Degree", options=degree_options) 
        col3.selectbox("Year", options=[1, 2, 3, 4]) 
        col4.text_input("Student ID", placeholder="Example: 202085777")
        st.form_submit_button("Get Students")

def pair_roomates():
    st.session.state.populator.match_roommates()

def settle_roomates():
    st.session.state.populator.assign_roomate()
        
def file_processing():
    st.session.state.populator = Populator(init_session_state.nu)
    st.session.state.populator.update_dorm(st.session_state.room_data)
    st.session.state.populator.read_students_to_accommodate(st.session_state.occupant_data)
    
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