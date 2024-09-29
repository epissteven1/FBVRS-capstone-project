import speech_recognition as sr
from PIL import Image
import streamlit as st
import os
import base64
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# Mapping of Baybayin characters to image filenames
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

def render_images_to_image(baybayin_images, output_file, image_dir='App/Image', padding=20):
    images = []
    # Ensure the image_dir is an absolute path
    image_dir = os.path.abspath(image_dir)
    for img_name in baybayin_images:
        img_path = os.path.join(image_dir, img_name)
        print(f"Attempting to load image: {img_path}")  # Debug statement
        try:
            img = Image.open(img_path)
            images.append(img)
        except FileNotFoundError:
            st.error(f"Image file '{img_name}' not found in directory '{image_dir}'.")
            print(f"FileNotFoundError: Image file '{img_name}' not found in directory '{image_dir}'.")
        except Exception as e:
            st.error(f"Error loading image '{img_name}': {e}")
            print(f"Exception: Error loading image '{img_name}': {e}")

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
        st.error(f"Error saving output image: {e}")
        print(f"Exception: Error saving output image: {e}")
        return None

def app():
    st.title("Baybayin Transcription from Audio")

    # Offer users the option to record or upload audio
    option = st.radio("Choose input method:", ('Upload Audio', 'Record Audio'))

    if option == 'Upload Audio':
        uploaded_file = st.file_uploader("Browse or Record Audio", type=["wav", "mp3"])
        if uploaded_file is not None:
            # Save the uploaded file temporarily
            with open("temp_audio_file", "wb") as f:
                f.write(uploaded_file.getbuffer())
            process_audio("temp_audio_file")

    elif option == 'Record Audio':
        st.write("Record your audio below:")
        
        # Use session state to store audio data
        if 'recorded_audio' not in st.session_state:
            st.session_state.recorded_audio = None

        webrtc_ctx = webrtc_streamer(
            key="audio-recorder",
            mode=WebRtcMode.SENDONLY,
            media_stream_constraints={
                "audio": True,
                "video": False
            }
        )

        # Once recording is done, store the audio data in session state
        if webrtc_ctx.audio_receiver:
            audio_frames = webrtc_ctx.audio_receiver.get_frames()
            if audio_frames:
                # Process audio frames and store them in session state
                st.session_state.recorded_audio = b"".join([frame.to_ndarray().tobytes() for frame in audio_frames])
                st.success("Recording saved!")

        if st.session_state.recorded_audio:
            st.audio(st.session_state.recorded_audio)
            with open("temp_audio_file.wav", "wb") as f:
                f.write(st.session_state.recorded_audio)
            process_audio("temp_audio_file.wav")

def process_audio(audio_file):
    # Convert audio to text
    text = audio_to_text(audio_file)
    st.write(f"Transcribed Text: {text}")

    # You can add the Baybayin image rendering part here
    # ...

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='tl-PH')
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"

if __name__ == "__main__":
    app()
