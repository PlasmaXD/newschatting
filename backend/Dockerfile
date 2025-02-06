FROM python:3.9-slim

# 作業ディレクトリ作成
WORKDIR /app

# パッケージインストール
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install -r requirements.txt

# アプリケーションコードコピー
COPY . .

# ポート設定（FastAPI/uvicornデフォルト: 8000）
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Uvicornを使ってアプリ起動コマンド（App RunnerはPORT環境変数を渡すのでそれに対応するためhost/portを環境変数参照に修正してもよい）
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD uvicorn app:app --host 0.0.0.0 --port $PORT
# CMD uvicorn app:app --host 0.0.0.0 --port $PORT
# CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
