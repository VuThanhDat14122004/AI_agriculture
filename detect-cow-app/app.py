import streamlit as st
import os
import uuid
from model import process_video

st.title("🎥 Phát hiện và đếm bò trong video")

uploaded_file = st.file_uploader("Tải lên video MP4", type=["mp4"])

if uploaded_file is not None:
    # Tạo đường dẫn tạm cho video gốc và video đầu ra
    video_id = str(uuid.uuid4())
    input_path = f"uploads/{video_id}.mp4"
    output_path = f"processed_videos/{video_id}_processed.mp4"

    # Lưu video đầu vào
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("📥 Video đã được tải lên. Bắt đầu xử lý...")

    # Tiến hành xử lý
    with st.spinner("Đang xử lý video..."):
        process_video(input_path, output_path)

    st.success("✅ Video đã xử lý xong!")
    st.video(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 Tải video đã xử lý", f, file_name="output.mp4")
