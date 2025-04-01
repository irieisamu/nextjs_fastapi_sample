from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uvicorn
import tempfile
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import pathlib

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
    # 組み込みの日本語CIDフォントを登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))  # 日本語ゴシック体
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))     # 日本語明朝体
    
    # カレントディレクトリにfontsフォルダがある場合は外部フォントを使用
    # 注意: 実際のデプロイ時にはフォントファイルを配置する必要があります
    fonts_dir = pathlib.Path(__file__).parent / "fonts"
    use_external_font = False
    
    # 外部フォントがある場合は登録
    if fonts_dir.exists():
        font_path = fonts_dir / "ipaexg.ttf"  # IPAexゴシック
        if font_path.exists():
            pdfmetrics.registerFont(TTFont('IPAexGothic', str(font_path)))
            use_external_font = True
    
    # PDFを生成するためのメモリバッファを作成
    buffer = BytesIO()
    
    # PDFキャンバスを作成
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # フォント選択（外部フォントまたは組み込みフォント）
    title_font = 'IPAexGothic' if use_external_font else 'HeiseiKakuGo-W5'
    body_font = 'IPAexGothic' if use_external_font else 'HeiseiKakuGo-W5'
    
    # PDFの内容を追加
    p.setFont(title_font, 16)
    p.drawString(2*cm, 28*cm, "サンプルPDFドキュメント")
    
    p.setFont(body_font, 12)
    p.drawString(2*cm, 26*cm, "これはNext.jsとFastAPIで生成されたPDFファイルです。")
    p.drawString(2*cm, 25*cm, "このPDFはReportLabライブラリを使用して作成されています。")
    p.drawString(2*cm, 24*cm, "日本語フォントに対応しています。")
    
    # 日付を追加
    import datetime
    now = datetime.datetime.now()
    date_string = now.strftime("%Y年%m月%d日 %H:%M:%S")
    p.drawString(2*cm, 22*cm, f"生成日時: {date_string}")
    
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

@app.get("/api/generate-pdf-with-ttf")
def generate_pdf_with_ttf():
    """
    外部TTFフォントを使用してPDFを生成するエンドポイント
    注意: このエンドポイントが動作するには、fontsディレクトリ内にTTFフォントが必要です
    """
    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        temp_path = tmp.name
    
    # 外部フォントのパスを指定
    try:
        # カレントディレクトリにfontsフォルダとフォントファイルがあるかチェック
        fonts_dir = pathlib.Path(__file__).parent / "fonts"
        gothic_font_path = fonts_dir / "ipaexg.ttf"  # IPAexゴシック
        mincho_font_path = fonts_dir / "ipaexm.ttf"  # IPAex明朝
        
        # フォントが存在するか確認
        if not gothic_font_path.exists() or not mincho_font_path.exists():
            # フォントがない場合は組み込みフォントを使用する方のエンドポイントにリダイレクト
            return generate_pdf()
            
        # フォントを登録
        pdfmetrics.registerFont(TTFont('IPAexGothic', str(gothic_font_path)))
        pdfmetrics.registerFont(TTFont('IPAexMincho', str(mincho_font_path)))
        
        # PDFを生成
        c = canvas.Canvas(temp_path, pagesize=A4)
        
        # タイトル
        c.setFont('IPAexGothic', 18)
        c.drawString(2*cm, 28*cm, "外部フォントを使用したPDF")
        
        # 本文
        c.setFont('IPAexGothic', 12)
        c.drawString(2*cm, 26*cm, "これは外部TTFフォント（IPAexゴシック）を使用したPDFです。")
        c.drawString(2*cm, 25*cm, "日本語が正しく表示されます。")
        
        # 明朝体のテキスト
        c.setFont('IPAexMincho', 12)
        c.drawString(2*cm, 23*cm, "こちらは明朝体（IPAex明朝）のテキストです。")
        
        # 日付
        import datetime
        now = datetime.datetime.now()
        date_string = now.strftime("%Y年%m月%d日 %H:%M:%S")
        c.drawString(2*cm, 21*cm, f"生成日時: {date_string}")
        
        c.showPage()
        c.save()
        
        # 生成したPDFを返す
        return FileResponse(
            path=temp_path,
            media_type="application/pdf",
            filename="sample_with_ttf.pdf"
        )
    
    except Exception as e:
        # エラーが発生した場合は組み込みフォントを使用する方のエンドポイントにリダイレクト
        print(f"外部フォントロードエラー: {e}")
        return generate_pdf()

# Railway 用の起動コード（__name__ == "__main__" のときだけ実行）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)