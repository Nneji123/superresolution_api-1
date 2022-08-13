import os
import os.path
if os.path.exists("./models/ColorizeArtistic_gen.pth") == False:
    cmd = "wget -O ./models/ColorizeArtistic_gen.pth https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth"
    os.system(cmd)
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse, FileResponse
import numpy as np
import io
from PIL import Image
import cv2
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.CPU)
import torch
import fastai
from ISR.models import RDN
from deoldify.visualize import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

app = FastAPI()

rdn = RDN(weights='noise-cancel')

colorizer = get_image_colorizer(artistic=True)


@app.get('/')
def home():
    return {'Title': 'Super Resolution and Colorisation API'}


# Endpoint for enhancing resolution and colorization of image
@app.post("/enhance_and_colorise")
async def root(file: UploadFile = File(...)):

    
    contents = io.BytesIO(await file.read())
    
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
    
    cv2.imwrite("new.jpg",img)
    
    sr_img = rdn.predict(img, by_patch_of_size=300)
    
    res, im_png = cv2.imencode(".png", sr_img)
    
    images = io.BytesIO(im_png.tobytes())

    sr2_img = colorizer.get_transformed_image(images, render_factor=35)
    
    new_img = np.array(sr2_img)
    # img = cv2.imdecode(np.array(sr_img), cv2.IMREAD_COLOR)
    
    res, im2_png = cv2.imencode(".png", new_img) 

    return StreamingResponse(io.BytesIO(im2_png.tobytes()), media_type="image/png")


# endpoint for just enhancing the image
@app.post("/enhance")
async def root(file: UploadFile = File(...)):

    # image = load_image_into_numpy_array(await file.read())

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    sr_img = rdn.predict(img, by_patch_of_size=300)

    res, im_png = cv2.imencode(".png", sr_img)

    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

# endpoint for just colorising the image
# Please review this section I may have mixed up something
@app.post("/colorise")
async def root(file: UploadFile = File(...)):

    
    contents = io.BytesIO(await file.read())
    
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
    
    cv2.imwrite("new.jpg",img)
    
    #sr_img = rdn.predict(img, by_patch_of_size=300)
    
   # res, im_png = cv2.imencode(".png", sr_img)
    
    #images = io.BytesIO(im_png.tobytes())

    sr2_img = colorizer.get_transformed_image("new.jpg", render_factor=35)
    
    new_img = np.array(sr2_img)
    # img = cv2.imdecode(np.array(sr_img), cv2.IMREAD_COLOR)
    
    res, im2_png = cv2.imencode(".png", new_img) 

    return StreamingResponse(io.BytesIO(im2_png.tobytes()), media_type="image/png")





