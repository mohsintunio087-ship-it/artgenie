from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    safety_checker=None
)
pipe = pipe.to("cuda")

print("Model load ho gaya!")

prompt = "a beautiful mountain landscape at sunset, highly detailed, digital art"

image = pipe(prompt).images[0]
image.save("my_image.png")

print("Image generate ho gayi! my_image.png check karein.")