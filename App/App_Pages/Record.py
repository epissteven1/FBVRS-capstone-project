import os
import streamlit as st

# Go up one directory from the current script location to access the 'App' directory
app_dir = os.path.dirname(os.path.dirname(__file__))

# Construct the path to the 'Image' directory inside 'App'
image_dir = os.path.join(app_dir, "App", "Image")

# Print directory contents to verify the file exists
st.write("Files in 'Image' Directory:", os.listdir(image_dir))

# Construct the path to the specific image
image_path = os.path.join(image_dir, "Ga.png")

# Print the constructed image path
st.write("Constructed Image Path:", image_path)

# Display the image
try:
    st.image(image_path)
except FileNotFoundError:
    st.error(f"Image file 'Ga.png' not found in directory '{image_dir}'.")
