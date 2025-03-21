import os
import subprocess
import json
import base64
import requests

# Get the home directory dynamically
home_dir = os.path.expanduser('~')

# Define the path to the folder where LoRAs are stored.
path = os.path.join(home_dir, 'Library', 'Containers', 'com.liuliu.draw-things', 'Data', 'Documents', 'Models')

# Function to open the LoRA folder in Finder
def open_lora_folder():
    subprocess.run(['open', path])

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
PROMPT = "Generate an Image of a dog."
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads/img2img/")
DRAW_THINGS_URL = "http://127.0.0.1:7860/sdapi/v1/img2img"

# Function to generate an image using the Draw Things API
def generate_image(prompt, base64_image=None):
    print(f"Generating image with {STEPS} steps...")

    # Define API parameters
    params = {
        "prompt": prompt,
        "negative_prompt": "(bokeh, worst quality, low quality, normal quality, (variations):1.4), blur:1.5",
        "seed": -1,
        "steps": STEPS,
        "cfg_scale": 10,
        "batch_count": 1,
        "sampler_name": "LCM",
        "model": "SDXL Base v1.0 (8-bit)",
        "loras": [
            {"file": "dmd2_sdxl_4_step_lora_f16.ckpt", "weight": 1},
            {"file": "", "weight": 1.0}
        ]
    }

    # If an initial image is provided, use img2img mode
    if base64_image:
        params["init_images"] = [base64_image]
        params["denoising_strength"] = 0.6

    # Send the request to the API
    headers = {"Content-Type": "application/json"}
    response = requests.post(DRAW_THINGS_URL, json=params, headers=headers)

    # Process the API response
    if response.status_code == 200:
        data = response.json()
        images = data.get("images", [])
        if images:
            # Save the generated image to a temporary file
            temp_image_path = os.path.join("/tmp", "generated_image.png")
            with open(temp_image_path, "wb") as img_file:
                img_file.write(base64.b64decode(images[0]))  # Decode and save the image
            return temp_image_path

    print(f"Error generating image: {response.status_code}, {response.text}")
    return None

# Main script execution
if __name__ == "__main__":
    for i in range(1, 100):  # Adjust the range as needed
        # Construct the image file path
        image_path = os.path.join(DOWNLOADS_FOLDER, f"image_{i}.png")

        # Check if the image file exists, and encode it if available
        base64_image = encode_image_to_base64(image_path) if os.path.exists(image_path) else None

        # Try generating the image
        generated_image_path = generate_image(PROMPT, base64_image=base64_image)

        if generated_image_path:
            print(f"✅ Image for Slide {i} saved at: {generated_image_path}")
        else:
            print(f"❌ Failed to generate image for Slide {i}.")
            # Ask the user if they want to open the LoRA folder
            user_input = input("Do you want to open the LoRAs in Finder to manually get the filenames? (y/n): ").strip().lower()

            if user_input == 'y':
                open_lora_folder()
                break  # Exit the script after opening the folder
            elif user_input == 'n':
                print("Exiting the script.")
                break  # Exit the script if the user doesn't want to open the folder
            else:
                print("Invalid input. Exiting the script.")
                break  # Exit the script if the input is invalid