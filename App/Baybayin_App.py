import streamlit as st

st.set_page_config(
    page_title="Filipino-to-Baybayin-Voice-Recognition-System",
    page_icon="App/App_Images/logo1.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import statements
import base64
from App_Pages import Home, AppDescription, Record, Feedback
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
    menu_list = ["Home", "Predict", "Description", "Translate", "Feedback"]
    with st.sidebar:
        option = option_menu("MENU",
                             menu_list,
                             icons=['house', 'record', 'sliders', 'search', 'chat'],
                             menu_icon="app-indicator",
                             default_index=1,
                             styles={
                                 "container": {"padding": "5!important"},
                                 "icon": {"color": "#b77b82", "font-size": "20px"},
                                 "nav-link": {"font-size": "12px", "text-align": "left", "margin": "0px",
                                              "--hover-color": "#F6E1D3"},
                                 "nav-link-selected": {"background-color": "#00008B"},
                             })

    # Render selected page
    if option == menu_list[0]:
        Home.app()
    if option == menu_list[1]:
        Record.app()
    if option == menu_list[2]:
        AppDescription.app()
    if option == menu_list[3]:
        Feedback.app()


    # Custom CSS for collapsible sidebar with icons on the left
    st.markdown("""
    <style>
    /* Initially hide the sidebar content (text), but keep the icons visible */
    .sidebar .sidebar-content {display: none;}
    .sidebar-collapsed .sidebar-content {display: none;} /* Content hidden when collapsed */
    
    /* Show only icons on the left */
    .sidebar {width: 60px !important; min-width: 60px !important;} /* Adjust sidebar width */
    
    /* Sidebar icon size and alignment */
    .icon {margin-left: auto; margin-right: auto;}
    
    /* When sidebar is expanded (on hover or toggle), show text */
    .sidebar:hover .sidebar-content {display: block;} 
    .sidebar:hover {width: 200px !important;} /* Expand sidebar when hovered */
    
    /* Mobile view adjustments */
    @media only screen and (max-width: 600px) {
        .sidebar {width: 60px !important;}  /* Sidebar defaults to icons only on small screens */
    }
    </style>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    app()
