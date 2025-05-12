from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse,FileResponse
from fastapi.staticfiles import StaticFiles 
from vision_logic import whole



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

tempplate = Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def hello(request:Request):
    return tempplate.TemplateResponse("home.html",{"request":request})




@app.get("/sub")
def open_camera():
    whole()
   
    return RedirectResponse(url="/", status_code=303)

@app.get("/download_pdf")
def download_pdf():
    return FileResponse("user guide.pdf", media_type='application/pdf', filename="user guide.pdf")
