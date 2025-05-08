import streamlit as st
import tempfile
from model import detect_and_count_cows

st.title("Cow Detection from Video")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    output_video_path = detect_and_count_cows(tfile.name)

    st.video(output_video_path)
