import os
import speech_recognition as sr
from PIL import Image
import streamlit as st

baybayin_image_mapping = {
    'a': 'A.png', 'e': 'E.png', 'i': 'I.png', 'o': 'O.png', 'u': 'U.png',
    'ka': 'ka.png', 'ga': 'ga.png', 'nga': 'nga.png', 'ta': 'ta.png', 'da': 'da.png',
    'na': 'na.png', 'pa': 'pa.png', 'ba': 'ba.png', 'ma': 'ma.png', 'ya': 'ya.png',
    'ra': 'ra.png', 'la': 'la.png', 'wa': 'wa.png', 'sa': 'sa.png', 'ha': 'ha.png'
}

def audio_to_text(audio_file):
    if not os.path.exists(audio_file):
        return "Audio file not found."
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='tl-PH')
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def split_into_syllables(word):
    vowels = 'aeiou'
    syllables = []
    current_syllable = ""
    for char in word:
        if char in vowels:
            current_syllable += char
            syllables.append(current_syllable)
            current_syllable = ""
        else:
            if current_syllable:
                syllables.append(current_syllable)
            current_syllable = char
    if current_syllable:
        syllables.append(current_syllable)
    return syllables

def text_to_baybayin_images(text):
    words = text.split()
    baybayin_images = []
    for word in words:
        syllables = split_into_syllables(word)
        for syllable in syllables:
            image_filename = baybayin_image_mapping.get(syllable)
            if image_filename:
                baybayin_images.append(image_filename)
    return baybayin_images

def render_images_to_image(baybayin_images, output_file, image_dir='Image', padding=20):
    images = []
    for img_name in baybayin_images:
        img_path = os.path.join(image_dir, img_name)
        try:
            img = Image.open(img_path)
            images.append(img)
        except FileNotFoundError:
            st.error(f"Image file {img_name} not found in directory '{image_dir}'.")
        except Exception as e:
            st.error(f"Error loading image {img_name}: {e}")

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

    background.save(output_file)
    return background

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
            

st.image('App/Image/ga.png')


if __name__ == "__main__":
    app()
