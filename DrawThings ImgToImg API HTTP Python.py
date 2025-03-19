import os
import json
import base64
import requests
# Have your img2img images saved in downloads folder as

# image_1.png, image_2.png etc. 

# Image generation settings
STEPS = 4  # Set to 4 for turbo models, 25 for regular models. 
PROMPT = "Generate an Image of a dog."  # The prompt describing what to generate

# Set the folder where images are stored
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

# API endpoint for the Draw Things img2img feature
DRAW_THINGS_URL = "http://127.0.0.1:7860/sdapi/v1/img2img"


# Function to generate an image using Draw Things API with img2img support
def generate_image(prompt, base64_image=None):
    print(f"Generating image with {STEPS} steps...")

    # Define API parameters
    params = {
        "prompt": prompt,
        "negative_prompt": "(bokeh, worst quality, low quality, normal quality, (variations):1.4), blur:1.5",
        "seed": -1,  # Randomized seed for variation; change this for deterministic results
        "steps": STEPS,  # Number of inference steps
        "cfg_scale": 10,  # Control the effect of the prompt on generation
        "batch_count": 1  # Only generate one image per request
    }

    # If an initial image is provided, use img2img mode
    if base64_image:
        params["init_images"] = [base64_image]
        params["denoising_strength"] = 0.6  # Adjust the effect strength in img2img mode

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
            return temp_image_path  # Return the saved image path

    # Print an error if the request fails
    print(f"Error generating image: {response.status_code}, {response.text}")
    return None  # Return None if there was an error

# Function to read an image and convert it to a base64 string
def encode_image_to_base64(image_path):
    """
    Reads an image from a file and converts it to a base64 string.

    Parameters:
    - image_path: Path to the image file.

    Returns:
    - Base64-encoded string of the image, or None if the file is not found.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return None  # Return None if the image file is missing

# Main script execution
if __name__ == "__main__":
    """
    Main execution block.
    - Loops through a set of images (Image_1.png, Image_2.png, etc.).
    - If an image exists, it is used for img2img transformation.
    - If no image exists, a new image is generated from the prompt.
    - Saves and prints the path of the newly generated image.
    """

    for i in range(1, 100):  # Adjust the range for the number of images you want to process
        # Construct the image file path (e.g., Image_1.png, Image_2.png, etc.)
        image_path = os.path.join(DOWNLOADS_FOLDER, f"image_{i}.png")

        # Check if the image file exists, and encode it if available
        base64_image = encode_image_to_base64(image_path) if os.path.exists(image_path) else None

        # Generate image using the API
        generated_image_path = generate_image(PROMPT, base64_image=base64_image)

        # Print results
        if generated_image_path:
            print(f"✅ Image for Slide {i} saved at: {generated_image_path}")
        else:
            print(f"❌ Failed to generate image for Slide {i}.")