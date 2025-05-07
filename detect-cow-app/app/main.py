from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from model import detect_and_count_cows

app = Flask(__name__)
UPLOAD_FOLDER = "/tmp/processed"  # Đổi sang /tmp để đảm bảo quyền ghi trên Render
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Tạo thư mục lưu trữ nếu chưa tồn tại
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if not file.filename.lower().endswith(('.mp4', '.avi')):
            return "Only .mp4 and .avi files are supported", 400

        # Kiểm tra kích thước file
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        if file_size > MAX_FILE_SIZE:
            return "File too large. Max size is 10MB.", 400
        file.seek(0)  # Reset con trỏ file

        filename = file.filename
        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], f"processed_{filename}")

        try:
            file.save(upload_path)
            detect_and_count_cows(upload_path, output_path)
            return redirect(url_for("result", filename=f"processed_{filename}"))
        except Exception as e:
            return f"Error processing video: {str(e)}", 500
    return render_template("index.html")

@app.route("/result/<filename>")
def result(filename):
    return render_template("result.html", filename=filename)

@app.route("/video/<filename>")
def video(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)