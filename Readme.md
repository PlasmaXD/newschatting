# ニュース分析App

このプロジェクトは、最新ニュースの取得、記事の要約生成、およびニュースに基づいた雑談生成を行うWebアプリケーション.
バックエンドはFastAPIを利用してAPIエンドポイント（[`backend/app.py`](backend/app.py)）を実装し、フロントエンドはStreamlitを用いてユーザーインターフェース（[`frontend/app.py`](frontend/app.py)）を提供する.

## ディレクトリ構造

- **backend/**  
  - [`app.py`](backend/app.py) : FastAPIを用いたAPIエンドポイント  
    - `/news` : NewsAPIから最新ニュースを取得  
    - `/summarize` : 記事の要約を生成  
    - `/generate-conversation` : ニュースに基づく雑談生成  
  - [`Dockerfile`](backend/Dockerfile) : Dockerイメージ作成用ファイル  
  - [`requirements.txt`](backend/requirements.txt) : 必要なPythonパッケージ  
  - その他、仮想環境（`venv/`）や設定ファイル（`.env`）等

- **frontend/**  
  - [`app.py`](frontend/app.py) : Streamlitを使ったフロントエンド. バックエンドAPIとの通信によりニュースの表示や操作を行う.  
  - その他設定ファイル（`.gitignore`等）

- その他  
  - ルートにはプロジェクト全体で利用する`.env`やユーティリティファイルが存在する.

## セットアップ方法

### 1. 環境変数の設定

プロジェクトルートおよび`backend/`ディレクトリに存在する`.env`ファイルに下記の変数を設定する.

- `API_KEY`: NewsAPIのAPIキー  
- `OPENAI_API_KEY`: OpenAIのAPIキー  
- `BACKEND_URL`: フロントエンドから利用するバックエンドのURL（例: `http://0.0.0.0:8000`）

### 2. バックエンドのセットアップ

#### ローカル実行の場合

1. `backend/`ディレクトリで仮想環境をアクティベート

    ```bash
    source venv/bin/activate
    ```

2. 依存パッケージをインストール

    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```

3. FastAPIサーバーを起動

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

#### Dockerを利用する場合

1. [Dockerfile](http://_vscodecontentref_/0)を使用してDockerイメージをビルド

    ```bash
    docker build -t my-app backend/
    ```

2. Dockerコンテナを起動

    ```bash
    docker run --env-file backend/.env -p 8000:8000 my-app
    ```

### 3. フロントエンドのセットアップ

1. 必要なパッケージ（例：Streamlit）をインストール  
   ※ 別途仮想環境を利用する場合は適宜構築する.

2. フロントエンドアプリを起動

    ```bash
    streamlit run frontend/app.py
    ```

## システムの動作

- **ニュースの取得**  
  フロントエンドは[`GET /news`](backend/app.py#L31)エンドポイントへリクエストを送り、NewsAPIから取得した最新ニュースデータを表示する.

- **記事の要約生成**  
  各ニュース記事の「要約を見る」エリアでは、[`POST /summarize`](backend/app.py#L50)エンドポイントを呼び出して記事内容を要約する.

- **雑談生成**  
  ユーザーが入力したオプションに基づき、[`POST /generate-conversation`](backend/app.py#L84)エンドポイントがニュース記事を元にカジュアルな会話を生成する.

## 注意事項

- 各エンドポイントはJSON形式のレスポンスを返す.  
- エラーハンドリングとして、APIからは適切なHTTPステータスコードおよびエラーメッセージが返される.

## システムの要件

- Python 3.8以上
- FastAPI
- Streamlit
- Docker（オプション）
- NewsAPIのAPIキー
- OpenAIのAPIキー

## 技術スタック

- **バックエンド**: FastAPI
- **フロントエンド**: Streamlit
<!-- - **データベース**: なし（必要に応じて追加可能）
- **認証**: なし（必要に応じて追加可能） -->

## アーキテクチャ
本アプリケーションはフロントエンドをStreamlit Cloud上、バックエンドをAWS AppRunner上にそれぞれ配置し、以下の流れで動作する:

1. ユーザーがStreamlit Cloud上のUIを操作  
2. FastAPIがAWS AppRunner上で稼働し、リクエストを受け付け  
3. NewsAPIやOpenAIのAPIキーを用いて必要な処理を行い、結果を返却

---
````
