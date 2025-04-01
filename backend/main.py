from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSの設定（VercelのURLに合わせて調整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では `https://your-vercel-app.vercel.app` に限定してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def read_hello():
    return {"message": "Hello from FastAPI!from backend"}
