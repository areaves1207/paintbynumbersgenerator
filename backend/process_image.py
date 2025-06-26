import cv2 as cv
import numpy as np
from fastapi import FastAPI, UploadFile, File

from fastapi.middleware.cors import CORSMiddleware

from .paint_by_numbers import paint_by_numbers_gen



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





items = []


@app.get("/")
def root():
    return{"Hello": "World"}


@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

@app.get("/item/{item_id}")
def get_item(item_id: int) -> str:
    item = items[item_id]
    return item




@app.post("/uploadimg/")
async def create_upload_img(file: UploadFile = File(...)):
    print(f"Received file: {file.filename} with content type: {file.content_type}")

    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img_np = cv.imdecode(np_arr, cv.IMREAD_COLOR)

    if img_np is None:
        return{"ERROR": "FAILED TO DECODE IMG"}
    
    print("Image {file.filename} decoded successfully")
    paint_by_numbers_gen(img_np)

    return {"File uploaded successfully"}


