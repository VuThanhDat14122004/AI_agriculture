import streamlit as st
import tempfile
import cv2
from model import process_video

st.title("Cow Detection App")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    tfile.close()

    stframe = st.empty()
    for frame in process_video(tfile.name):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")
