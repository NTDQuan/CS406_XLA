#model
import os
import sys
sys.path.append("D:/Tai lieu hoc/Nhap/XLA_test/backend")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ----SAM
from segment_anything import SamPredictor, sam_model_registry
# ----Stable Diffusion
from diffusers import StableDiffusionInpaintPipeline
# ----GroundingDINO
from GroundingDINO.groundingdino.util.inference import load_model, load_image, predict, annotate
from GroundingDINO.groundingdino.util import box_ops
# ----Extra Libraries
from PIL import Image
import torch
import cv2
import matplotlib.pyplot as plt
import numpy as np
from edit_image import edit_image

IMAGEDIR = "images/"
# ------SAM Parameters
device = "cpu"
model_type = "vit_h"
sam_weight_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sam_weight', 'sam_vit_h_4b8939.pth'))
config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GroundingDINO', 'groundingdino', 'config', 'GroundingDINO_SwinT_OGC.py'))
weights_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..' , 'GroundingDINO', 'weights', 'groundingdino_swint_ogc.pth'))
print("loading predictor....")
predictor = SamPredictor(sam_model_registry[model_type](checkpoint=sam_weight_path).to(device=device))
print("predictor loaded!")
print("loading stable diffusion...")
# ------Stable Diffusion
pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting", torch_dtype=torch.float16,).to("cuda")
pipe.enable_vae_slicing()
pipe.enable_xformers_memory_efficient_attention()
print("stable diffusion loaded!")
print("loading GD....")
# ----Grounding DINO
groundingdino_model = load_model(config_file_path, weights_file_path)
print("GD loaded!")

path = 'losupply-quang-tri-thanh-pho-dong-ha-quang-tri-1648801646214781853-nuoc-ngot-coca-cola-lon-320ml-0-1658895994.jpg'
print("editting...")
edited_image = edit_image(path, "can of coke", "phone booth", 0.5, 0.2, groundingdino_model, predictor, pipe)
fig, axes = plt.subplots(1, 2, figsize=(30, 15))

axes[0].imshow(plt.imread(path))
axes[0].axis('off')
axes[0].set_title('Before', fontdict={'fontsize': 50})
axes[0].set_aspect('auto')

axes[1].imshow(edited_image)
axes[1].axis('off')
axes[1].set_title('After', fontdict={'fontsize': 50})
axes[1].set_aspect('auto')
plt.show()