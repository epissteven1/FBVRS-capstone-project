import streamlit as st

st.set_page_config(
    page_title="Filipino-to-Baybayin-Voice-Recognition-System",
    page_icon="App/App_Images/logo1.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import statements
import base64
from App_Pages import Home, AppDescription, Record, Feedback, Instruction
from streamlit_option_menu import option_menu

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("App/App_Images/Sidebar1.png")

# Custom CSS for page styling
st.markdown(f"""
    <style>
        body {{
            text-align: center;
            background-color: white;
        }}
        
        .sidebar-content {{
            background-color: #242525;
            color: white;
        }}
      .st-emotion-cache-13k62yr {{
            position: absolute;
           
            color: rgb(193, 231, 247);
            inset: 0px;
            color-scheme: transparent;
            overflow: hidden;
         
        }}
    
       
        footer {{
            visibility: visible;
        }}
        footer:before {{
            content: 'Capstone1 @ 2023-2024: FBVRS';
            color: #FF4B4B;
            display: block;
            position: relative;
            padding: 2px;
            top: 3px;
        }}
        [data-testid="stSidebarContent"] {{
        background-image: url("data:image/png;base64,{img}");
        background-position:center;
        
        }}
        [data-testid="stVerticalBlockBorderWrapper"] {{
         background-color: transparent;
        }}
        
        [data-testid="stAppViewBlockContainer"] {{
        background-color: #333333;;
        }}
        [data-testid="stAppViewContainer"] {{
        background-color: white;
        }}
        [data-testid="stHeader"] {{
        background-color: #696969;
        }}
       
    </style>
""", unsafe_allow_html=True)


# Function to render the app
def app():
    menu_list = ["Home", "Predict", "Description", "Translate", "Feedback", "Test"]
    with st.sidebar:
        option = option_menu("MENU",
                             menu_list,
                             icons=['house', 'record', 'sliders', 'search', 'chat', 'test'],
                             menu_icon="app-indicator",
                             default_index=1,
                             styles={
                                 "container": {"padding": "5!important"},
                                 "icon": {"color": "#b77b82", "font-size": "20px"},  # Adjusted for smaller view
                                 "nav-link": {"font-size": "12px", "text-align": "left", "margin": "0px",
                                              "--hover-color": "#F6E1D3"},
                                 "nav-link-selected": {"background-color": "#00008B"},
                                 "nav-link-hover": {"background-color": "#f0f0f5"}  # Hover effect
                             })

    # Render selected page
    if option == menu_list[0]:
        Home.app()
    if option == menu_list[1]:
        Record.app()
    if option == menu_list[2]:
        AppDescription.app()
    if option == menu_list[3]:
        Predict.app()
    if option == menu_list[4]:
        Feedback.app()
    if option == menu_list[5]:
        Instruction.app()

    # Custom CSS for mobile responsiveness
   # Custom CSS for fixing the black space issue on smartphones
    st.markdown("""
    <style>
    /* Set the sidebar to take full screen width when expanded on mobile */
    .sidebar {
        width: 60px !important; /* Default width with only icons */
        transition: width 0.3s; /* Smooth transition for expansion */
    }

    /* Expand the sidebar fully when hovered on mobile screens */
    @media only screen and (max-width: 600px) {
        .sidebar:hover {
            width: 100vw !important; /* Full width expansion */
        }
        /* Ensure the content inside expands properly when hovered */
        .sidebar:hover .sidebar-content {
            display: block;
        }
    }

    /* Handle black space by adjusting the padding */
    .block-container {
        padding-left: 0rem !important; /* Remove extra padding */
    }
    </style>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    app()
