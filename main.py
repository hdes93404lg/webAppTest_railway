from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="我的網站")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/yingge-trip.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health():
    return {"status": "ok"}
