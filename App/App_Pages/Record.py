import os
import speech_recognition as sr
from PIL import Image, ImageOps
import streamlit as st
import tempfile
import base64
from io import BytesIO
import cv2
import numpy as np
import noisereduce as nr  # Noise reduction library

# Mapping from syllable to image filename
baybayin_image_mapping = {
    'a': 'A.png', 'e': 'E.png', 'i': 'I.png', 'o': 'O.png', 'u': 'U.png',
    'ka': 'Ka.png', 'ga': 'Ga.png', 'nga': 'Nga.png', 'ta': 'Ta.png', 'da': 'Da.png',
    'na': 'Na.png', 'pa': 'Pa.png', 'ba': 'Ba.png', 'ma': 'Ma.png', 'ya': 'Ya.png',
    'ra': 'Ra.png', 'la': 'La.png', 'wa': 'Wa.png', 'sa': 'Sa.png', 'ha': 'Ha.png',
    'be': 'Be.png', 'bi': 'Bi.png', 'bo': 'Bo.png', 'bu': 'Bu.png', 'de': 'De.png',
    'di': 'Di.png', 'do': 'Do.png', 'du': 'Du.png', 'ge': 'Ge.png', 'gi': 'Gi.png',
    'go': 'Go.png', 'gu': 'Gu.png', 'he': 'He.png', 'hi': 'Hi.png', 'ho': 'Ho.png',
    'hu': 'Hu.png', 'ke': 'Ke.png', 'ki': 'Ki.png', 'ko': 'Ko.png', 'ku': 'Ku.png',
    'le': 'Le.png', 'li': 'Li.png', 'lo': 'Lo.png', 'lu': 'Lu.png', 'me': 'Me.png',
    'Mi': 'Mi.png', 'mo': 'Mo.png', 'mu': 'Mu.png', 'ne': 'Ne.png', 'ni': 'Ni.png',
    'no': 'No.png', 'nu': 'Nu.png', 'nge': 'Nge.png', 'ngi': 'Ngi.png', 'ngo': 'Ngo.png',
    'ngu': 'Ngu.png', 'pe': 'Pe.png', 'pi': 'Pi.png', 'po': 'Po.png', 'pu': 'Pu.png',
    're': 'Re.png', 'ri': 'Ri.png', 'ro': 'Ro.png', 'ru': 'Ru.png', 'se': 'Se.png', 'si': 'Si.png',
    'so': 'So.png', 'su': 'Su.png', 'te': 'Te.png', 'ti': 'Ti.png', 'to': 'To.png',
    'tu': 'Tu.png', 'we': 'We.png', 'wi': 'Wi.png', 'wo': 'Wo.png', 'wu': 'Wu.png',
    'ye': 'Ye.png', 'yi': 'Yi.png', 'yo': 'Yo.png', 'yu': 'Yu.png'
}


def reduce_noise(audio_data):
    # Convert audio to numpy array
    audio_np = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
    # Reduce noise using the noisereduce library
    reduced_noise = nr.reduce_noise(y=audio_np, sr=audio_data.sample_rate)
    return sr.AudioData(reduced_noise.tobytes(), audio_data.sample_rate, audio_data.sample_width)


def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        # Adjust for ambient noise and capture audio
        audio_data = recognizer.record(source)
        # Apply noise reduction
        audio_data = reduce_noise(audio_data)
    try:
        text = recognizer.recognize_google(audio_data, language='tl-PH')  # Tagalog
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"


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


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def apply_canny_edge_detection(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    # Create a mask with edges
    mask = Image.fromarray(edges)
    return mask


def render_images_to_image(baybayin_images, output_file, image_dir='Image'):
    if not baybayin_images:
        return None, None

    # Load the images
    images = [Image.open(os.path.join(image_dir, img)).convert("RGBA") for img in baybayin_images]

    if not images:
        return None, None

    # Apply edge detection and transparency
    for i in range(len(images)):
        edge_mask = apply_canny_edge_detection(images[i])
        images[i].putalpha(edge_mask)

    # Calculate the total width and height for the final image
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)

    # Create a new blank image with the calculated dimensions
    combined_image = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))

    # Paste each image onto the blank image, centering them vertically
    x_offset = 0
    for img in images:
        y_offset = (max_height - img.height) // 2  # Center the image vertically
        combined_image.paste(img, (x_offset, y_offset), img)
        x_offset += img.width

    # Save the combined image
    combined_image.save(output_file)

    # Return the combined image and base64 string
    return combined_image, image_to_base64(combined_image)


def app():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if st.button("Start Listening"):
        st.write("Listening...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                # Listen with a timeout of 10 seconds, and auto-stop if no real voice is detected
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    f.write(audio.get_wav_data())
                    temp_audio_file = f.name

                text = audio_to_text(temp_audio_file)
                st.write(f"Transcribed Text: {text}")

                baybayin_images = text_to_baybayin_images(text)
                combined_image, image_base64 = render_images_to_image(baybayin_images, 'output_image.png',
                                                                      image_dir='Image')

                if combined_image:
                    st.markdown(
                        f"""    
                        <div style="display: flex; justify-content: center; align-items: center;">
                            <img src="data:image/png;base64,{image_base64}" alt="Baybayin Transcription" />
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.write("No Baybayin images found for the transcribed text.")
            except sr.WaitTimeoutError:
                st.write("No real voice detected within 10 seconds. Stopping the listener.")


if __name__ == "__main__":
    app()	
