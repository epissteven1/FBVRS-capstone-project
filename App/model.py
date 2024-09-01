import os
import numpy as np
import cv2
import librosa
import soundfile as sf
import tempfile
import tensorflow as tf
import streamlit as st


class AudioToImageModel:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.input_shape = (128, 87, 1)
        self.num_classes = 21  # Number of classes

    def preprocess_audio(self, audio_data, sr, target_sr=44100):
        # Save audio data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_path = temp_audio_file.name
            sf.write(temp_audio_path, audio_data, sr)

        # Load audio data with the desired sampling rate
        audio_data_resampled, sr_resampled = librosa.load(temp_audio_path, sr=target_sr)

        # Remove temporary file
        os.unlink(temp_audio_path)

        spectrogram = librosa.feature.melspectrogram(y=audio_data_resampled, sr=sr_resampled)
        log_mel_spectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)
        resized_spectrogram = cv2.resize(log_mel_spectrogram, (self.input_shape[1], self.input_shape[0]),
                                         interpolation=cv2.INTER_CUBIC)
        resized_spectrogram = np.expand_dims(resized_spectrogram, axis=-1)
        normalized_spectrogram = resized_spectrogram / -80.0
        return normalized_spectrogram

    def generate_image_from_audio(self, audio_data, sr, target_sr=44100):
        preprocessed_audio = self.preprocess_audio(audio_data, sr, target_sr)
        predicted_image = self.model.predict(np.expand_dims(preprocessed_audio, axis=0))

        # Ensure that the predicted image has the correct shape
        if len(predicted_image.shape) == 3:  # Ensure it's a multi-channel image
            return predicted_image[0]  # Return the first image in the batch
        else:
            return predicted_image  # Return as is


def display_multi_channel_image(image_tensor):
    st.subheader("Predicted Images")
    num_channels = image_tensor.shape[-1]
    for i in range(num_channels):
        st.image(image_tensor[:, :, i], caption=f"Channel {i+1}", use_column_width=True)


