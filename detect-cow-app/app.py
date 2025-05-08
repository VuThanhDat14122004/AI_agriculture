import streamlit as st
import os
from model import process_video

st.title("Detect and Count Cows in Video")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if uploaded_file:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.info("⏳ Processing video, please wait...")
    output_path = process_video("input_video.mp4")
    st.success("✅ Done!")

    st.video(output_path)
