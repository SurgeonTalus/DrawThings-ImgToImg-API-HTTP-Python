import os
import subprocess
import json
import base64
import requests
import time

# Get the home directory dynamically
home_dir = os.path.expanduser('~')

# Define the path to the folder where LoRAs are stored.
path = os.path.join(home_dir, 'Library', 'Containers', 'com.liuliu.draw-things', 'Data', 'Documents', 'Models')

# Function to encode an image to base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return None

# Image generation settings
STEPS = 4
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads/img2img/")
DRAW_THINGS_URL = "http://127.0.0.1:7860/sdapi/v1/img2img"

# Function to generate an image using the Draw Things API
def generate_image(prompt, base64_image=None, model="SDXL Base v1.0 (8-bit)", denoising_strength=None, loras=None):
    print(f"Generating image with {STEPS} steps using {model}...")

    # Default LoRAs if not provided
    if loras is None:
        loras = [
            {"file": "dmd2_sdxl_4_step_lora_f16.ckpt", "weight": 1},
            {"file": "ronyellow_300_ema_0,050_lora_f32.ckpt", "weight": 1}
        ]

    # Define API parameters
    params = {
        "prompt": prompt,
        "negative_prompt": "(bokeh, worst quality, low quality, normal quality, (variations):1.4), blur:1.5",
        "seed": -1,
        "steps": STEPS,
        "cfg_scale": 10,
        "batch_count": 1,
        "sampler_name": "LCM",
        "model": model,
        "loras": loras
    }

    # If an initial image is provided (img2img mode)
    if base64_image:
        params["init_images"] = [base64_image]
        params["denoising_strength"] = denoising_strength  # Apply only for img2img (SDXL step)

    # Send the request to the API
    headers = {"Content-Type": "application/json"}
    response = requests.post(DRAW_THINGS_URL, json=params, headers=headers)

    # Process the API response
    if response.status_code == 200:
        data = response.json()
        images = data.get("images", [])
        if images:
            # Generate the filename based on the prompt and truncate it to 20 characters
            filename = f"image_{prompt[:20]}.png"
            filename = filename[:25]  # Keep "image_" + 20 characters + ".png"
            image_file_path = os.path.join(DOWNLOADS_FOLDER, filename)
            
            # Save the generated image to a file
            with open(image_file_path, "wb") as img_file:
                img_file.write(base64.b64decode(images[0]))  # Decode and save the image
            return image_file_path

    print(f"Error generating image: {response.status_code}, {response.text}")
    return None

# Main script execution
if __name__ == "__main__":
    # List of three prompts
    prompts = [
        "In the style of Aaron Douglas  #Ferdinands Tango (Ron helps a sad alpaca find happiness by dancing the tango, demonstrating the power of simple kindness.)  Illustration: Ron, wearing a yellow t-shirt and green pants, is enthusiastically leading an alpaca in a tango dance. The alpaca’s ears are perked up, its posture straightened, and it appears joyful. Ron's face is happy. A large, ornate gramophone plays music nearby, emitting swirling musical notes. The scene exudes warmth.",
        "Don Bluth, candid shot, cinematic, documentary, facing left, 2d, flat color, no shadow. cartoon comic. Summer. Daylight**Character:** Little Red Riding Hood meets the wolf **Importance:** She is the central figure in this exchange. **Facial Expression:** Confused **Arms:** Her arms are raised slightly in surprise.  **Scene:** A dimly lit forest path, with dense trees and underbrush on either side. The sun is beginning to set, casting long, ominous shadows. **Complementary Details:** A basket filled with goodies hangs from her left arm, while her right hand clutches her red hood tightly around her neck.  **Mood:** Uneasy  **Objects of Note:** The forest is dark and foreboding, with massive trees looming over Little Red Riding Hood. The basket she carries is large and prominently placed, its contents hinted at by the golden-brown color of what could be bread.",
        "In the style of Aaron Douglas  **Illustration Detail:**  The most important element to illustrate is the giant Lego house.     The house is overwhelmingly large, constructed entirely of brightly colored Lego bricks in a chaotic but charming design. A long, winding slide extends from the roof, appearing playful and inviting. Raindrops are visibly clinging to the Lego surface, glistening under a soft light. The man building it has a happy expression, his feet firmly planted on the ground.    **Mood:** Whimsical."
    ]

    for i, prompt in enumerate(prompts, start=1):
        print(f"\n--- PROCESSING IMAGE {i} ---\n")

        # Generate a fresh image using SD3 (no denoising_strength)
        print(f"🔄 Generating Image {i} (SD3 Large Turbo 3.5)...")
        image_1_path = generate_image(prompt, model="SD3 Large Turbo 3.5 (8-bit)")  # No denoising_strength

        if image_1_path:
            print(f"✅ Image {i} generated with SD3 at: {image_1_path}")
        else:
            print(f"❌ Failed to generate Image {i} with SD3.")
            continue  # Skip to next iteration if image generation fails

        # Wait for 1 second before processing
        time.sleep(1)

        # Process the image with SDXL (denoising_strength=0.6)
        print(f"🔄 Processing Image {i} with SDXL Base v1.0...")
        image_2_path = generate_image(prompt, base64_image=encode_image_to_base64(image_1_path), model="SDXL Base v1.0 (8-bit)", denoising_strength=0.6)

        if image_2_path:
            print(f"✅ Processed Image {i} saved at: {image_2_path}")
        else:
            print(f"❌ Failed to process Image {i} with SDXL.")
            continue  # Skip to next iteration if image processing fails

        # Wait before restarting with SD3 for the next image
        time.sleep(1)