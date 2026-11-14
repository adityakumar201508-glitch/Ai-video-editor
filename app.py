from flask import Flask, request, render_template_string, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Video Editor</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    background: #10111b;
    color: white;
    font-family: Arial;
    text-align: center;
    padding: 25px;
}
.box {
    background: #202235;
    padding: 25px;
    border-radius: 18px;
    max-width: 500px;
    margin: 30px auto;
}
input, textarea, button {
    width: 100%;
    padding: 14px;
    margin: 12px 0;
    box-sizing: border-box;
    border-radius: 10px;
}
button {
    background: #725cff;
    color: white;
    border: none;
    font-size: 17px;
}
video {
    width: 100%;
    margin-top: 15px;
}
</style>
</head>
<body>
<h1>🎬 AI VIDEO EDITOR</h1>
<p>Your personal AI video editing studio</p>

<div class="box">
<h2>Upload Your Video</h2>
<form action="/upload" method="POST" enctype="multipart/form-data">
<input type="file" name="video" accept="video/*" required>
<textarea name="instruction" placeholder="Tell AI how to edit your video..."></textarea>
<button type="submit">Upload Video</button>
</form>
{% if filename %}
<h3>Video Uploaded Successfully!</h3>
<video controls src="/uploads/{{ filename }}"></video>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    video = request.files.get("video")
    if not video or not video.filename:
        return "Please select a video."

    filename = secure_filename(video.filename)
    if not filename.lower().endswith(
        (".mp4", ".mov", ".avi", ".mkv", ".webm")
    ):
        return "Unsupported video format."

    video.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template_string(HTML, filename=filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
