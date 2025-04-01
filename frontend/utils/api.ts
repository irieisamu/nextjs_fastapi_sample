export async function fetchMessage(): Promise<string> {
  const res = await fetch("https://nextjsfastapisample-production.up.railway.app/api/hello");
  const data = await res.json();
  return data.message;
}

export async function fetchMessage(): Promise<string> {
  const res = await fetch("https://nextjsfastapisample-production.up.railway.app/api/hello");
  const data = await res.json();
  return data.message;
}

export async function downloadPdf(options: {
  type: 'reportlab' | 'reportlab-ttf' | 'weasyprint';
} = { type: 'reportlab' }): Promise<void> {
  try {
    // 使用するエンドポイントを選択
    let endpoint;
    let filename;
    
    switch (options.type) {
      case 'reportlab-ttf':
        endpoint = "https://nextjsfastapisample-production.up.railway.app/api/generate-pdf-with-ttf";
        filename = "sample_with_ttf.pdf";
        break;
      case 'weasyprint':
        endpoint = "https://nextjsfastapisample-production.up.railway.app/api/generate-pdf-weasy";
        filename = "report.pdf";
        break;
      case 'reportlab':
      default:
        endpoint = "https://nextjsfastapisample-production.up.railway.app/api/generate-pdf";
        filename = "sample.pdf";
        break;
    }
    
    // APIエンドポイントからPDFをフェッチ
    const response = await fetch(endpoint);
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    // レスポンスをBlobに変換
    const blob = await response.blob();
    
    // BlobからURLを作成
    const url = window.URL.createObjectURL(blob);
    
    // 一時的なリンク要素を作成してクリックイベントをトリガーする
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    
    // クリーンアップ
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error("PDFのダウンロードに失敗しました:", error);
    throw error;
  }
}