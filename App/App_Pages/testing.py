import streamlit as st

def app:
st.write("hello")
print("Current working directory:", os.getcwd())
print("Image directory path:", os.path.join(os.path.dirname(__file__), image_dir))
