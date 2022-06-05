"""
FastAPI controller.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.routing import Mount

from utils.root import get_project_root

templates = Jinja2Templates(directory="templates")

routes = [
    Mount(f'/static', StaticFiles(directory='static'), name='static')
]

app = FastAPI(routes=routes)


@app.get("/")
async def root():
    return {"message": "We Live Baby."}


@app.get('/base', response_class=HTMLResponse)
async def return_base(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run('api.base:app', host='localhost', port=1337, reload=True)