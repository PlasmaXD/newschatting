仮想環境のアクティベート（既にアクティベートされている場合はスキップ）:

```bash
source venv/bin/activate
```

```bash
pip install --no-cache-dir -r requirements.txt
```

docker run --env-file .env -p 8000:8000 my-app
