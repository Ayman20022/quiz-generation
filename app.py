import streamlit as st
import sounddevice as sd
import speech_recognition as sr
import soundfile as sf
import time 
import tempfile
import os
import numpy as np
from audiotranscription import create_quiz


def start():

    fs = 44100  # Sample frequency Commonly used values for audio recording include 44100 Hz (44.1 kHz), 48000 Hz (48 kHz), and 96000 Hz (96 kHz).
    seconds = 10  # Duration of recording

    # Start recording
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)

    st.write('AI is listening ')

    sd.wait()  # Wait until recording is finished
    
    st.write("AI has finished recording ")
    
    # we're going to create a temporaray file in which we're going to store our recorded audio 
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        audio_file = tmpfile.name
        sf.write(tmpfile.name, recording, fs)
    # we're going to instantiate the speechReconition Recognizer()
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data) 
    st.write('AI is transcribing your speech : '+text)
    st.write('The google form link  : '+create_quiz(text))

    
def main():
    st.title("Record")
    st.write("Start recording")
    if st.button('Start transcribing'):
        start()
        

if __name__ == "__main__":
    main()
