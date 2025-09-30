import json
import cv2 as cv
import numpy as np
from fastapi import FastAPI, Form, UploadFile, File # type: ignore
from fastapi.responses import StreamingResponse, Response # type: ignore
from PIL import Image
import io
import base64

from fastapi.middleware.cors import CORSMiddleware # type: ignore

from paint_by_numbers import paint_by_numbers_gen


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pbn-gen.vercel.app"],
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
        print("ERROR: FAILED TO DECODE IMG")
        return{"ERROR": "FAILED TO DECODE IMG"}
    
    print(f"Image {file.filename} decoded successfully")
    colored_img, combined_img, canvas, palette = paint_by_numbers_gen(img_np, numColors)
    if(combined_img is None or canvas is None or palette is None):
        return Response(status_code=204)
    #conv imgs to PIL    
    combined_img = Image.fromarray(combined_img)
    canvas = Image.fromarray(canvas)
    palette = Image.fromarray(palette)
    colored_img = Image.fromarray(colored_img)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        combined_img_io = BytesIO()
        combined_img.save(combined_img_io, format="PNG")
        combined_img_io.seek(0)
        zip_file.writestr("combined_img.png", combined_img_io.read())
        
        canvas_io = BytesIO()
        canvas.save(canvas_io, format="PNG")
        canvas_io.seek(0)
        zip_file.writestr("canvas.png", canvas_io.read())
        
        palette_io = BytesIO()
        palette.save(palette_io, format="PNG")
        palette_io.seek(0)
        zip_file.writestr("palette.png", palette_io.read())
        
        colored_img_io = BytesIO()
        colored_img.save(colored_img_io, format="PNG")
        colored_img_io.seek(0)
        zip_file.writestr("colored_img.png", colored_img_io.read())
    
    zip_buffer.seek(0)
    print("Images zipped")
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content": "attachment; filename=processed_images.zip"
    })

@app.get("/")
async def root():
    return {"message": "API is running"}


@app.get("/ping")
async def ping():
    print("Ping received")
    return {"message": "ok"}