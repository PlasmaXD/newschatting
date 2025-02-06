from fastapi import FastAPI, HTTPException
import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import httpx
from dotenv import load_dotenv
from starlette.concurrency import run_in_threadpool

app = FastAPI()

# .env ファイルから環境変数を読み込み
load_dotenv()

# 環境変数から API キーを取得
API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("API_KEY 環境変数が設定されていません。")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY 環境変数が設定されていません。")

# OpenAI クライアントの初期化
client = OpenAI(api_key=OPENAI_API_KEY)

class SummarizeRequest(BaseModel):
    content: str

class ConversationRequest(BaseModel):
    topic: Optional[str] = "最新のニュース"
    style: Optional[str] = "カジュアルで親しみやすい"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/news")
async def get_news():
    url = f"https://newsapi.org/v2/everything?q=日本&pageSize=5&apiKey={API_KEY}"
    async with httpx.AsyncClient() as client_http:
        response = await client_http.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"NewsAPI returned status {response.status_code}"
        )
    news_data = response.json()
    articles = news_data.get("articles", [])
    simplified_articles = [
        {
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "content": article.get("content")
        }
        for article in articles
    ]
    return {"articles": simplified_articles}

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    content = request.content
    if not content:
        raise HTTPException(status_code=400, detail="No content provided for summarization.")
    try:
        # 同期の create メソッドをバックグラウンドで実行する
        response = await run_in_threadpool(
            lambda: client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes news articles."
                    },
                    {
                        "role": "user",
                        "content": f"以下の文章を要約してください:\n\n{content}"
                    }
                ],
                max_tokens=150,
                temperature=0.5,
            )
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@app.post("/generate-conversation")
async def generate_conversation(request: ConversationRequest):
    topic = request.topic
    style = request.style

    # ステップ1: ニュース記事の取得
    news_response = await get_news()
    articles = news_response.get("articles", [])
    if not articles:
        raise HTTPException(status_code=404, detail="会話を生成するためのニュース記事が見つかりませんでした。")

    # ステップ2: 記事情報のコンパイル
    compiled_news = "\n\n".join([
        f"**{article['title']}**\n{article['description']}\n詳細はこちら: {article['url']}"
        for article in articles
    ])

    try:
        # 同期の create メソッドをバックグラウンドで実行する
        conversation_response = await run_in_threadpool(
            lambda: client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"あなたは{style}な会話の達人です。"},
                    {"role": "user", "content": f"以下のニュース記事に基づいて、{topic}についてのカジュアルな会話を生成してください:\n\n{compiled_news}"}
                ],
                max_tokens=300,
                temperature=0.7,
            )
        )
        conversation = conversation_response.choices[0].message.content.strip()
        return {"conversation": conversation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"会話の生成に失敗しました: {str(e)}")
