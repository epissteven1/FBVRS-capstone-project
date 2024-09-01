import speech_recognition as sr
from PIL import Image
import streamlit as st
import os
print("Current working directory:", os.getcwd())




def render_images_to_image(baybayin_images, output_file, image_dir='Image', padding=20):
    images = []
    for img_name in baybayin_images:
        img_path = os.path.join(image_dir, img_name)
        print(f"Attempting to load image: {img_path}")  # Debug statement
        try:
            img = Image.open(img_path)
            images.append(img)
        except FileNotFoundError:
            st.error(f"Image file '{img_name}' not found in directory '{image_dir}'.")
        except Exception as e:
            st.error(f"Error loading image '{img_name}': {e}")

    if not images:
        st.error("No valid images were loaded to create the output image.")
        return None

    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)

    combined_image = Image.new('RGB', (total_width, max_height), 'white')
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    background_width = total_width + 2 * padding
    background_height = max_height + 2 * padding
    background = Image.new('RGB', (background_width, background_height), 'white')

    background.paste(combined_image, (padding, padding))

    try:
        background.save(output_file)
        print(f"Output image saved as: {output_file}")  # Debug statement
        return background
    except Exception as e:
        st.error(f"Error saving the output image: {e}")
        return None
        
base_dir = os.path.dirname(__file__)
img_path = os.path.join(base_dir, 'Image', img_name)

def app():
    
    st.title("Baybayin Transcription from Audio")

    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "flac"])

    if uploaded_file is not None:
        temp_audio_file = "temp_audio_file.wav"
        try:
            with open(temp_audio_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except Exception as e:
            st.error(f"Error saving the uploaded audio file: {e}")
            return

        text = audio_to_text(temp_audio_file)
        st.write(f"Transcribed Text: {text}")

        if not text.strip():
            st.write("The transcribed text is empty or invalid.")
            return
        
        baybayin_images = text_to_baybayin_images(text)
        if baybayin_images:
            combined_image = render_images_to_image(baybayin_images, 'output_image.png', image_dir='Image')
            st.image(combined_image, caption='Baybayin Transcription')
        else:
            st.write("No Baybayin images found for the transcribed text.")

        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
            
if __name__ == "__main__":
    app()
