FROM python:3.10-slim

# WeasyPrintの依存関係をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-ipafont \
    fonts-ipaexfont \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 日本語フォント用のディレクトリを作成
RUN mkdir -p fonts templates

# フォントへのシンボリックリンクを作成
RUN ln -s /usr/share/fonts/opentype/ipafont-gothic/ipag.ttf /app/fonts/ipag.ttf 2>/dev/null || true \
    && ln -s /usr/share/fonts/opentype/ipafont-mincho/ipam.ttf /app/fonts/ipam.ttf 2>/dev/null || true \
    && ln -s /usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf /app/fonts/ipaexg.ttf 2>/dev/null || true \
    && ln -s /usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf /app/fonts/ipaexm.ttf 2>/dev/null || true

# バックエンドのコードをコピー
COPY . .

# ポート設定（環境変数を使うためシェルを使用）
EXPOSE 8000

# シェルスクリプトを使って環境変数を正しく解釈
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}