# 🧑‍🎨 Avatar Creator API – Flask + Diffusers + ControlNet

This project is an AI-powered avatar generation API built with **Flask**, **ControlNet**, and **Stable Diffusion**. It allows users to upload face images, apply clothing styles (suits, shirts, t-shirts), and generate realistic avatars with customizable prompts.

---

## 🚀 Features

- Upload and detect face from user image
- Generate avatars with selected clothing and color
- ControlNet integration for image-to-image avatar generation
- Secure login and registration system
- Serve and save generated images
- Organized upload and download folders
- Flask RESTful API with CORS support

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Flask** (API framework)
- **Diffusers (Hugging Face)** – for Stable Diffusion pipelines
- **ControlNetModel**
- **face_recognition** – for face detection
- **Pillow (PIL)** – image preprocessing
- **rembg** – background removal
- **PyTorch**
- **Rembg**, **requests**, **Werkzeug**, **os**, **time**, **json**

---

## 📁 Folder Structure

project-root/
│
├── services/
│ └── instantid.py # Main avatar generator logic
│
├── useruploads/ # Uploaded user face images
├── uploads/ # Clothing assets (suits, shirts, etc.)
├── generated/ # Output avatars
├── checkpoints/ # ControlNet model directory (ignored)
│
├── app.py # Main Flask API
├── requirements.txt
├── .gitignore
└── README.md


2. Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

3. Install Requirements

pip install -r requirements.txt


4. Download ControlNet Checkpoint
Place your ControlNetModel (with config.json, etc.) inside:

/services/checkpoints/ControlNetModel/

5. Run the Server
python app.py
