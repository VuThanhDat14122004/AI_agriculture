from flask import Flask, request, render_template, redirect, url_for
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
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            detect_and_count_cows(filepath)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
