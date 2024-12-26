
from flask import Flask, request, jsonify
import boto3  # AWS SDK for Python
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure AWS S3
S3_BUCKET = "your-bucket-name"
S3_REGION = "your-region"
s3_client = boto3.client('s3', region_name=S3_REGION)

# Directory to temporarily save uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# Backend Routes
# =========================

@app.route("/login", methods=["POST"])
def login():
    """Simulate user authentication."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Simple authentication simulation (Replace with real authentication logic)
    if username == "admin" and password == "password":
        return jsonify({"message": "Login successful!", "status": "success"}), 200
    return jsonify({"message": "Invalid credentials.", "status": "fail"}), 401

@app.route("/upload", methods=["POST"])
def upload_script():
    """Handle script file uploads."""
    if "script" not in request.files:
        return jsonify({"message": "No file part.", "status": "fail"}), 400

    file = request.files["script"]
    if file.filename == "":
        return jsonify({"message": "No selected file.", "status": "fail"}), 400

    # Save file locally and upload to S3
    filename = secure_filename(file.filename)
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(local_path)

    try:
        s3_client.upload_file(local_path, S3_BUCKET, filename)
        os.remove(local_path)  # Clean up local file
        return jsonify({"message": "File uploaded successfully.", "status": "success"}), 200
    except Exception as e:
        return jsonify({"message": f"Upload failed: {e}", "status": "fail"}), 500

if __name__ == "__main__":
    app.run(debug=True)
