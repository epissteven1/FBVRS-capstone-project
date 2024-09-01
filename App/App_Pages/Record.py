import os

# Go up one directory from the current script location to access the 'App' directory
app_dir = os.path.dirname(os.path.dirname(__file__))

# Construct the path to the 'Image' directory inside 'App'
image_path = os.path.join(app_dir, "Image", "Ga.png")

st.write("Constructed Image Path:", image_path)
st.image(image_path)
