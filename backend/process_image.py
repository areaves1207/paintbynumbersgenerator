from fastapi import FastAPI, UploadFile, File

from fastapi.middleware.cors import CORSMiddleware
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
    return {"filename": file.filename, "message": "File uploaded successfully"}
