from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from model import detect_and_count_cows

app = Flask(__name__)
UPLOAD_FOLDER = "static/processed"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], f"processed_{filename}")

            file.save(upload_path)
            detect_and_count_cows(upload_path, output_path)

            return redirect(url_for("result", filename=f"processed_{filename}"))
    return render_template("index.html")

@app.route("/result/<filename>")
def result(filename):
    return render_template("result.html", filename=filename)

@app.route("/video/<filename>")
def video(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
