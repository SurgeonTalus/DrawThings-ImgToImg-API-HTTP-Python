# DrawThings Img2Img API (HTTP Python)

This project provides an API-based solution to generate images using Draw Things' Img2Img feature in Python. It allows users to transform existing images into new variations based on a text prompt.

## Example Images

### Original Image
![Original Image](https://github.com/SurgeonTalus/DrawThings-ImgToImg-API-HTTP-Python/blob/main/image_1.png)

### Img2Img Generated Image
![Generated Image](https://github.com/SurgeonTalus/DrawThings-ImgToImg-API-HTTP-Python/blob/main/image_1-img2img%20Dog.png)

## Features
- **Img2Img transformation**: Convert existing images into new styles based on a prompt.
- **Customizable settings**: Adjust steps, denoising strength, and prompt influence.
- **Batch processing**: Loop through multiple images for transformation.
- **Error handling**: Detect missing images and API failures.


## Installation
Ensure you have Python installed along with the required dependencies:

```bash
pip install requests
```

## Usage

1. **Place input images** in your `Downloads` folder, named as `image_1.png`, `image_2.png`, etc.
2. **Run the script** to generate new images based on the input images and prompt.

```python
python script.py
```

## Configuration
Modify the script variables to customize the behavior:

```python
STEPS = 4  # Turbo models use 4 steps, regular models use 25
PROMPT = "Generate an Image of a dog."  # Text prompt for image transformation
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")
```

## API Details
- **Endpoint**: `http://127.0.0.1:7860/sdapi/v1/img2img`
- **Required Parameters**:
  - `prompt`: Description of the image to generate.
  - `init_images`: Base64-encoded input image.
  - `denoising_strength`: Controls how much the image changes.

## Example Output
Upon successful execution, the script will save transformed images and display messages like:

```bash
✅ Image for Slide 1 saved at: /tmp/generated_image.png
✅ Image for Slide 2 saved at: /tmp/generated_image.png
```

In case of errors:

```bash
❌ Failed to generate image for Slide 1.
```

## License
This project is open-source under the MIT License.

---

Contributions and improvements are welcome!
Here is the original inspiration for the script: https://docs.drawthings.ai/documentation/documentation/8.scripts
