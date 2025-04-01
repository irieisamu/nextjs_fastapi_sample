from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

app = FastAPI()

# CORSの設定（開発中は "*"、本番は特定ドメインに制限）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nextjsfastapisample.vercel.app", "http://localhost:3000"],  # ローカル開発用を追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def read_hello():
    return {"message": "Hello from FastAPI! from backend"}

@app.get("/api/generate-pdf")
def generate_pdf():
    # PDFを生成するためのメモリバッファを作成
    buffer = BytesIO()
    
    # PDFキャンバスを作成
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # PDFの内容を追加
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, 28*cm, "サンプルPDFドキュメント")
    
    p.setFont("Helvetica", 12)
    p.drawString(2*cm, 26*cm, "これはNext.jsとFastAPIで生成されたPDFファイルです。")
    p.drawString(2*cm, 25*cm, "このPDFはReportLabライブラリを使用して作成されています。")
    
    # 日付を追加
    import datetime
    now = datetime.datetime.now()
    date_string = now.strftime("%Y年%m月%d日 %H:%M:%S")
    p.drawString(2*cm, 23*cm, f"生成日時: {date_string}")
    
    # PDFを保存
    p.showPage()
    p.save()
    
    # バッファの位置を先頭に戻す
    buffer.seek(0)
    
    # PDFをレスポンスとして返す
    return Response(
        content=buffer.getvalue(), 
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sample.pdf"}
    )

# Railway 用の起動コード（__name__ == "__main__" のときだけ実行）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)