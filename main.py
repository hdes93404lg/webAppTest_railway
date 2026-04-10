from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="我的網站")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "首頁",
        "message": "Hello World",
    })


@app.get("/health")
async def health():
    return {"status": "ok"}
