# fastapi
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from random import randint
import uuid
import tempfile
import shutil

#model
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
from src.edit_image import edit_image
from pydantic import BaseModel


app = FastAPI()

origin = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

commandline_args = os.environ.get('COMMANDLINE_ARGS', "--Precision-full --no-half")
# ------SAM Parameters
device = "cpu"
model_type = "vit_h"
predictor = SamPredictor(sam_model_registry[model_type](checkpoint="sam_weight/sam_vit_h_4b8939.pth").to(device=device))
# ------Stable Diffusion
pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting", torch_dtype=torch.float32,).to("cpu")
# ----Grounding DINO
groundingdino_model = load_model("GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", "GroundingDINO/weights/groundingdino_swint_ogc.pth")
temp_dir = tempfile.mkdtemp()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload/")
async def process_form(
    newObject: str = Form(...),
    object: str = Form(...),
    selectedImage: UploadFile = File(...),
):

    try:
        input_image_path = f"{temp_dir}/{selectedImage.filename}"
        #save the file
        with open(input_image_path, "wb") as image_file:
            shutil.copyfileobj(selectedImage.file, image_file)
        image_result = edit_image(input_image_path, object, newObject,0.3,0.2,groundingdino_model, predictor, pipe)
        result_image_path = f"{temp_dir}/result.jpg"
        image_result.save(result_image_path)

        return FileResponse(result_image_path, media_type="image/jpeg")
    except Exception as e:
        return {"error": str(e)}
