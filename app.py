from flask import Flask, request, jsonify, send_from_directory
from database import login, register
from services import instantid
import os
import requests
from werkzeug.utils import secure_filename
import time 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
USER_UPLOADS_FOLDER = 'useruploads'
GENERATED_FOLDER = 'generated'

# Ensure all directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(USER_UPLOADS_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Allow uploading up to 10 files
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg', '.webp', '.glb']

# ------------------ Existing Endpoints ------------------

@app.route('/login', methods=['GET'])
def login_api():
    email = request.args.get('email')
    password = request.args.get('password')
    if login.login_user(email, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/register', methods=['POST'])
def register_api():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not email or not password or not name:
        return jsonify({"message": "Email, name, and password are required"}), 400
    if register.register_user(name, email, password):
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "User already exists"}), 409

@app.route('/save-avatar', methods=['POST'])
def save_avatar():
    data = request.get_json()
    avatar_url = data.get('avatar_url')
    if not avatar_url:
        return jsonify({"message": "Avatar URL missing"}), 400

    response = requests.get(avatar_url)
    if response.status_code == 200:
        filename = os.path.join(UPLOAD_FOLDER, os.path.basename(avatar_url))
        with open(filename, 'wb') as f:
            f.write(response.content)
        return jsonify({"message": "Avatar saved", "file": filename}), 200
    else:
        return jsonify({"message": "Failed to download avatar"}), 500
@app.route('/generated/<path:filename>', methods=['GET'])
def serve_generated_avatar(filename):
    return send_from_directory(GENERATED_FOLDER, filename)

@app.route('/generator', methods=['POST'])
def avatar_generator():
    try:
        data = request.get_json()
        selected_category = str(data.get('selectedCategory'))
        selected_cloth = data.get('selectedImg')
        if selected_category == "suit":
            color = selected_cloth.replace("http://localhost:5000/uploads/suit/", "") 
        elif selected_category == "shirts":
            color = selected_cloth.replace("http://localhost:5000/uploads/shirts/", "")
            selected_category = 'shirt'
        elif selected_category == "tshirts":
            color = selected_cloth.replace("http://localhost:5000/uploads/tshirts/", "")
            selected_category = 't-shirt'
        selected_color = color.replace(".png", "")
        avatar_generated_path =instantid.generator(selected_category,selected_color)
        filename = os.path.basename(avatar_generated_path)  # e.g., "avatar_bg.png"
        server_url = request.host_url.rstrip('/')  # http://localhost:5000
        public_url = f"{server_url}/generated/{filename}"
    except Exception as e:
        return jsonify({"message": "Avatar generation failed", "error": str(e)}), 500   

    return jsonify({
        "message": "Avatar generated successfully",
        "generated_avatar": public_url
    }), 201

# ------------------ New Upload Endpoint ------------------

@app.route('/useruploads', methods=['POST'])
def handle_user_uploads():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({"error": "No files uploaded"}), 400

    # Get metadata
    metadata_json = request.form.get('metadata')
    if not metadata_json:
        return jsonify({"error": "Metadata missing"}), 400
    
    try:
        metadata = eval(metadata_json)  # Or better: use `json.loads`
    except Exception as e:
        return jsonify({"error": "Invalid metadata format", "details": str(e)}), 400

    uploaded_files = []
    for file in files:
        filename = secure_filename(f"{int(time.time())}-{file.filename}") 
        filepath = os.path.join(USER_UPLOADS_FOLDER, filename)
        file.save(filepath)

        uploaded_files.append({
            "filename": filename,
            "path": filepath,
            "url": f"/useruploads/{filename}"
        })

    return jsonify({
        "status": "success",
        "uploaded": len(uploaded_files),
        "files": uploaded_files,
        "metadata": metadata
    }), 200

# Serve uploaded files statically (just like Express)
@app.route('/useruploads/<path:filename>', methods=['GET'])
def serve_user_uploads(filename):
    return send_from_directory(USER_UPLOADS_FOLDER, filename)

# ------------------ Image Listing from Uploads ------------------

@app.route('/images', methods=['GET'])
def list_images_by_category():
    categorized = {}
    base_url = request.host_url.rstrip('/') + "/uploads"

    for category in os.listdir(UPLOAD_FOLDER):
        category_path = os.path.join(UPLOAD_FOLDER, category)
        if os.path.isdir(category_path):
            images = []
            for file in os.listdir(category_path):
                images.append({
                    "filename": file,
                    "url": f"{base_url}/{category}/{file}"
                })
            categorized[category] = images

    return jsonify(categorized)

# Serve uploaded images from /uploads
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ------------------ Entry Point ------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
