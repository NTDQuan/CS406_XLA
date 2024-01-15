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
import os



device = "cpu"

def edit_image(path, item, prompt, box_threshold, text_threshold, groundingdino_model, predictor, pipe):
    '''
    - path (str): Path to the image file
    - item (str): Item to be recognized in the image
    - prompt (str): Item to replace the selected object in the image
    - box_threshold (float): Threshold for the bounding box predictions.
    - text_threshold (float): Threshold for the text predictions.
    '''
    device = "cpu"
    src, img = load_image(path)
    boxes, logits, phrases = predict(
        model=groundingdino_model,
        image=img,
        caption=item,
        box_threshold=box_threshold,
        text_threshold=text_threshold
    )
    predictor.set_image(src)
    H, W, _ = src.shape
    boxes_xyxy = box_ops.box_cxcywh_to_xyxy(boxes) * torch.Tensor([W, H, W, H])
    new_boxes = predictor.transform.apply_boxes_torch(boxes_xyxy, src.shape[:2]).to("cpu")
    masks, _, _ = predictor.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=new_boxes,
        multimask_output=False,
    )
    return pipe(prompt=prompt,
        image=Image.fromarray(src).resize((512, 512)),
        mask_image=Image.fromarray(masks[0][0].cpu().numpy()).resize((512, 512))
    ).images[0]