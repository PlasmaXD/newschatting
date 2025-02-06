import streamlit as st
import requests
import os
from dotenv import load_dotenv
# .envファイルを読み込む
load_dotenv()

# 環境変数を取得
BACKEND_URL = os.getenv('BACKEND_URL')

# BACKEND_URL = "http://0.0.0.0:8000"

st.title("ニュース分析アプリ")
st.subheader("トップニュース")

# ニュースデータ取得
params = {
    "q": "日本",      # 検索キーワード
    "page_size": 10   # 取得記事数
}
response = requests.get(f"{BACKEND_URL}/news", params=params)

if response.status_code != 200:
    st.error(f"HTTPエラー: {response.status_code}")
else:
    news_data = response.json()
    st.success("ニュースデータの取得に成功しました。")
    
    if 'articles' in news_data and news_data['articles']:
        st.write(f"取得した記事数: {len(news_data['articles'])}")
        
        for idx, article in enumerate(news_data['articles'], start=1):
            st.markdown(f"### {idx}. {article.get('title', 'タイトルなし')}")
            content = article.get('content')
            if content:
                with st.expander("要約を見る"):
                    # バックエンドに要約リクエスト
                    sum_res = requests.post(f"{BACKEND_URL}/summarize", json={"content": content})
                    if sum_res.status_code == 200:
                        sum_data = sum_res.json()
                        if "summary" in sum_data:
                            st.write(f"**要約:** {sum_data['summary']}")
                        else:
                            st.error(f"要約の生成中にエラーが発生しました: {sum_data.get('detail', '不明なエラー')}")
                    else:
                        st.error(f"要約リクエストでHTTPエラーが発生しました: {sum_res.status_code}")
            else:
                st.warning("この記事には要約するコンテンツがありません。")
    else:
        st.warning("現在、利用可能なニュース記事がありません。")

st.markdown("---")

st.subheader("雑談生成")

st.write("最新のニュースに基づいた雑談を生成します。以下のオプションを設定してください。")

# 雑談生成のオプション設定
with st.form(key='conversation_form'):
    topic = st.text_input("トピック（任意）", value="最新のニュース")
    style = st.text_input("スタイル（任意）", value="カジュアルで親しみやすい")
    generate_button = st.form_submit_button(label='雑談を生成')

if generate_button:
    # リクエストボディの作成
    payload = {
        "topic": topic,
        "style": style
    }
    
    # 雑談生成リクエスト
    conv_res = requests.post(f"{BACKEND_URL}/generate-conversation", json=payload)
    
    if conv_res.status_code == 200:
        conv_data = conv_res.json()
        conversation = conv_data.get("conversation", "")
        if conversation:
            st.success("雑談の生成に成功しました。")
            st.write(conversation)
        else:
            st.error("雑談の生成中にエラーが発生しました。")
    else:
        # エラーメッセージの表示
        try:
            error_data = conv_res.json()
            error_detail = error_data.get("detail", "不明なエラー")
        except ValueError:
            error_detail = "不明なエラー"
        st.error(f"雑談生成リクエストでHTTPエラーが発生しました: {conv_res.status_code} - {error_detail}")
