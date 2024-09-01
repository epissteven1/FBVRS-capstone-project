import os
import streamlit as st

def app():
    st.write("hello")
    
    # Current working directory
    current_dir = os.getcwd()
    st.write(f"Current working directory: {current_dir}")

    # Define image_dir
    image_dir = 'Image'
    
    # Safely get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_directory_path = os.path.join(script_dir, image_dir)
    st.write(f"Image directory path: {image_directory_path}")

if __name__ == "__main__":
    app()
