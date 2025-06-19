from diffusers import StableDiffusionPipeline, ControlNetModel
from PIL import Image
import face_recognition
import os
from rembg import remove
import time

def load_pipeline():
    
    controlnet_path = None
    if controlnet_path is None:
        # Create absolute path to the ControlNet model
        base_dir = os.path.abspath(os.path.dirname(__file__))
        controlnet_path = os.path.join(base_dir, "checkpoints/ControlNetModel")  # <-- FIXED

    if not os.path.exists(os.path.join(controlnet_path, "config.json")):
        raise FileNotFoundError(f"Config not found in {controlnet_path}. Did you download the model correctly?")

    controlnet = ControlNetModel.from_pretrained(
        controlnet_path,
        local_files_only=False
    )

    pipe = StableDiffusionPipeline.from_pretrained(
        "Lykon/dreamshaper-8",
        controlnet=controlnet
    )

    return pipe


def generate_avatar(pipe, prompt: str, input_image_path: str, output_path: str):
    init_image = Image.open(input_image_path).convert("RGB").resize((512, 512))
    print(prompt)

    result = pipe(
        prompt=prompt,
        image=init_image,
        num_inference_steps=30,
        guidance_scale=7.5,
    ).images[0]

    result.save(output_path)
    return output_path

def get_first_image_with_face(directory_path=None, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

    if directory_path is None:
        # Create absolute path to ../useruploads
        base_dir = os.path.abspath(os.path.dirname(__file__))  # path to services/instantid.py
        directory_path = os.path.join(base_dir, "../useruploads")

    directory_path = os.path.abspath(directory_path)
    for filename in os.listdir(directory_path):
        if os.path.splitext(filename)[1].lower() in allowed_extensions:
            image_path = os.path.join(directory_path, filename)

            try:
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)

                if face_locations:
                    return {
                        "path": image_path,
                        "faces_detected": len(face_locations),
                        "locations": face_locations
                    }
            except Exception as e:
                print(f"Error processing file {image_path}: {e}")

    return None

def generator(selected_category, selected_color):
    face_detected_image = get_first_image_with_face()
    if not face_detected_image:
        raise RuntimeError("No image with a detectable face found.")
    timestamp = int(time.time())
    generated_name = f"generated_avatar_{timestamp}.png"
    # Paths inside 'generated/' folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    generated_dir = os.path.join(base_dir, "../generated")
    os.makedirs(generated_dir, exist_ok=True)

    generated_path = os.path.join(generated_dir, generated_name)
    pipe = load_pipeline()

    generate_avatar(
        pipe=pipe,
        prompt = "Generate a single man half-body  realistic avator and a neutral expression single pose  with " + selected_color + " color " + selected_category + ".",
        input_image_path=face_detected_image["path"],
        output_path=generated_path
    )
    return generated_path
