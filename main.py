import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    ImageMessage,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from database import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="我的網站")
templates = Jinja2Templates(directory="templates")

# Line Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# CWA 雷達回波圖 URL
RADAR_IMAGE_URL = "https://www.cwa.gov.tw/Data/radar/CV1_TW_3600.png"
RADAR_PREVIEW_URL = "https://www.cwa.gov.tw/Data/radar/CV1_TW_1000.png"


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/yingge-trip.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/callback")
async def line_callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = (await request.body()).decode("utf-8")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    user_text = event.message.text.strip()

    if "雷達" in user_text:
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(
                            original_content_url=RADAR_IMAGE_URL,
                            preview_image_url=RADAR_PREVIEW_URL,
                        )
                    ],
                )
            )
