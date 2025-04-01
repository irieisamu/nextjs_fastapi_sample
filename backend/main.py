from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

# CORSの設定（開発中は "*"、本番は特定ドメインに制限）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 例: ["https://your-vercel-app.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def read_hello():
    return {"message": "Hello from FastAPI! from backend"}

# Railway 用の起動コード（__name__ == "__main__" のときだけ実行）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
