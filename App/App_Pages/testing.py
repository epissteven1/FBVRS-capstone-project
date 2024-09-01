import os
import streamlit as st

def app():
    st.write("hello")
    print("Current working directory:", os.getcwd())

    # Define image_dir or set it to a default value if undefined
    image_dir = 'Image'  # Adjust this according to your directory structure

    # Safely get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_directory_path = os.path.join(script_dir, image_dir)
    print("Image directory path:", image_directory_path)

