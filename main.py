import uvicorn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from programs.video_stack import videostack
from programs.coach import golf_coach
from programs.video_play import videoplay
from fastapi.templating import Jinja2Templates
import os



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request} )

@app.get("/getvideo/")

async def read_videos(request: Request):
    
    files = os.listdir("static/videos")
    
    return templates.TemplateResponse("list_video.html", {"request": request, "files": files})

@app.get("/videoplay/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: None = None ):
    print(id)
    file_path = "static/videos/" + id
    
    result = await videoplay(file_path)

    return (file_path + " : recieved")


"""
 Video Play
"""

@app.post("/uploadvideofile/", response_description="Image uploaded and data added into the database")
async def create_upload_video(file: UploadFile = File(...)):
    
    file_name = file.filename
    file_path = f"static/videos/" + file_name
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    result = await videoplay(file_path)

    return (file_path + "/  recieved")
   
              
@app.get("/videoplay")
async def main():
    content ="""
<body>
<form action="uploadvideofile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
"""
    return HTMLResponse(content=content)

"""
 Video Stack
"""

@app.post("/uploadfiles/", response_description="Image uploaded and data added into the database")
async def create_upload_files(files: list[UploadFile] = File(...)):
    file_names = []
    file_paths = []
    
    for file in files:
        file_name = file.filename
        file_names.append(file_name)
        file_path = f"static/videos/" + file_name
        file_paths.append(file_path)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
    result = await videostack(file_paths)
    return(result)

@app.get("/videostack")
async def main():
    content ="""
<body>
<form action="uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
"""
    return HTMLResponse(content=content)

"""
 Video Trace
"""

@app.post("/uploadvideo/", response_description="Image uploaded and data added into the database")
async def create_upload_video(file: UploadFile = File(...)):
    
    file_name = file.filename
    file_path = f"static/videos/" + file_name
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    print(file_path)
    result = await golf_coach(file_path)
   
    return(result)
   
              
@app.get("/videotrace")
async def main():
    content ="""
<body>
<form action="uploadvideo/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
"""
    return HTMLResponse(content=content)



if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload=True)
