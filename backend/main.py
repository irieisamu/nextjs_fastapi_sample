from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from io import BytesIO
import jinja2
from weasyprint import HTML, CSS
from fastapi.responses import FileResponse
import tempfile
import pathlib
from datetime import datetime

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nextjsfastapisample.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2テンプレート設定
templates_dir = pathlib.Path(__file__).parent / "templates"
if not templates_dir.exists():
    templates_dir.mkdir(parents=True)

# テンプレートローダーを設定
template_loader = jinja2.FileSystemLoader(templates_dir)
template_env = jinja2.Environment(loader=template_loader)

@app.get("/api/hello")
def read_hello():
    return {"message": "Hello from FastAPI! from backend"}

@app.get("/api/generate-pdf-weasy")
def generate_pdf_weasy():
    """WeasyPrintを使用してリッチなレイアウトのPDFを生成する"""
    
    # テンプレートファイルがない場合は、サンプルテンプレートを作成
    template_path = templates_dir / "report_template.html"
    if not template_path.exists():
        with open(template_path, "w", encoding="utf-8") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>レポート</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            font-size: 24pt;
            margin-bottom: 0.5cm;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.3cm;
        }
        .header {
            text-align: center;
            margin-bottom: 1cm;
        }
        .logo {
            width: 100px;
            height: auto;
        }
        .date {
            color: #7f8c8d;
            font-size: 10pt;
            margin-top: 0.5cm;
            text-align: right;
        }
        .content {
            margin: 1cm 0;
        }
        .section {
            margin-bottom: 1cm;
        }
        .section h2 {
            color: #3498db;
            font-size: 16pt;
            margin-bottom: 0.3cm;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.5cm 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            padding: 0.3cm;
            text-align: left;
        }
        td {
            padding: 0.3cm;
        }
        .chart {
            text-align: center;
            margin: 1cm 0;
        }
        .footer {
            margin-top: 2cm;
            border-top: 1px solid #eee;
            padding-top: 0.5cm;
            text-align: center;
            font-size: 9pt;
            color: #7f8c8d;
        }
        .info-box {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 0.5cm;
            margin: 0.5cm 0;
        }
        .grid-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5cm;
            margin-bottom: 1cm;
        }
        .grid-item {
            background-color: #f0f7ff;
            padding: 0.5cm;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>サンプルレポート</h1>
        <div class="date">作成日時: {{ date }}</div>
    </div>
    
    <div class="content">
        <div class="section">
            <h2>概要</h2>
            <p>このレポートは、WeasyPrintとFastAPIを使用して生成されたリッチなレイアウトのPDFサンプルです。HTML/CSSを使用してさまざまなスタイルやレイアウトを適用できます。</p>
            
            <div class="info-box">
                <strong>重要:</strong> WeasyPrintは強力なHTML/CSSレンダリングエンジンで、高品質なPDFを生成できます。
            </div>
        </div>
        
        <div class="section">
            <h2>データ</h2>
            <table>
                <thead>
                    <tr>
                        <th>項目</th>
                        <th>数値</th>
                        <th>カテゴリ</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in data %}
                    <tr>
                        <td>{{ item.name }}</td>
                        <td>{{ item.value }}</td>
                        <td>{{ item.category }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>グリッドレイアウト</h2>
            <div class="grid-container">
                <div class="grid-item">
                    <h3>特徴1</h3>
                    <p>CSSグリッドを使用したレイアウト例です。複数の列を簡単に作成できます。</p>
                </div>
                <div class="grid-item">
                    <h3>特徴2</h3>
                    <p>レスポンシブデザインの原則をPDFにも適用できます。</p>
                </div>
                <div class="grid-item">
                    <h3>特徴3</h3>
                    <p>複雑なレイアウトも直感的に作成可能です。</p>
                </div>
                <div class="grid-item">
                    <h3>特徴4</h3>
                    <p>CSSの全機能を活用してスタイリングできます。</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>© 2025 サンプルカンパニー - このPDFはWeasyPrintで生成されました</p>
    </div>
</body>
</html>
            """)
    
    try:
        # テンプレートを読み込み
        template = template_env.get_template("report_template.html")
        
        # テンプレートに渡すデータ
        context = {
            "date": datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"),
            "data": [
                {"name": "製品A", "value": 120, "category": "電子機器"},
                {"name": "製品B", "value": 85, "category": "家具"},
                {"name": "製品C", "value": 210, "category": "食品"},
                {"name": "製品D", "value": 65, "category": "衣料品"},
                {"name": "製品E", "value": 175, "category": "電子機器"}
            ]
        }
        
        # HTMLテンプレートをレンダリング
        html_content = template.render(**context)
        
        # HTMLからPDFを生成
        pdf_file = BytesIO()
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)
        
        # PDFをレスポンスとして返す
        return Response(
            content=pdf_file.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=report.pdf"}
        )
        
    except Exception as e:
        print(f"PDF生成エラー: {e}")
        return {"error": str(e)}

# Railway 用の起動コード
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)