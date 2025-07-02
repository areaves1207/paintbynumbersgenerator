import json
import cv2 as cv
import numpy as np
from fastapi import FastAPI, Form, UploadFile, File # type: ignore
from fastapi.responses import StreamingResponse # type: ignore
from PIL import Image
import io
import base64

from fastapi.middleware.cors import CORSMiddleware # type: ignore

from paint_by_numbers import paint_by_numbers_gen



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#chatgpt generated img encoder
def array_to_base64_img(np_array):
    img = Image.fromarray(np_array.astype("uint8"))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


from PIL import Image
from io import BytesIO
import zipfile

@app.post("/upload_img/")
async def create_upload_img(file: UploadFile = File(...), numColors: int = Form(...)):
    print(f"Received file: {file.filename} with content type: {file.content_type}")
    print(f"Received NumColors value of: {numColors}")

    #read in img from front end as uint8 thru cv
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img_np = cv.imdecode(np_arr, cv.IMREAD_COLOR)

    if img_np is None:
        return{"ERROR": "FAILED TO DECODE IMG"}
    
    print(f"Image {file.filename} decoded successfully")
    result_tight, result_smooth = paint_by_numbers_gen(img_np, numColors)
    #conv imgs to PIL    
    result_tight = Image.fromarray(result_tight)
    result_smooth = Image.fromarray(result_smooth)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        img1_io = BytesIO()
        result_tight.save(img1_io, format="PNG")
        img1_io.seek(0)
        zip_file.writestr("final_image_tight.png", img1_io.read())
        
        img2_io = BytesIO()
        result_smooth.save(img2_io, format="PNG")
        img2_io.seek(0)
        zip_file.writestr("final_image_smooth.png", img2_io.read())
    
    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content": "attachment; filename=processed_images.zip"
    })
