from flask import Flask, request, render_template, redirect, url_for, Response
import os
from model import detect_and_count_cows

app = Flask(__name__)
UPLOAD_FOLDER = "static/processed"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

video_path = None  # lưu lại video mới upload

@app.route("/", methods=["GET", "POST"])
def upload_file():
    global video_path
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            video_path = filepath
            return redirect(url_for("video_stream"))
    return render_template("index.html")

@app.route("/video")
def video_stream():
    return render_template("video.html")

@app.route("/video_feed")
def video_feed():
    if video_path:
        return Response(detect_and_count_cows(video_path),
                        mimetype="multipart/x-mixed-replace; boundary=frame")
    return "No video uploaded", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
