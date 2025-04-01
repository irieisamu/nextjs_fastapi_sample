export async function fetchMessage(): Promise<string> {
  const res = await fetch("https://nextjsfastapisample-production.up.railway.app/api/hello");
  const data = await res.json();
  return data.message;
}

export async function downloadPdf(): Promise<void> {
  try {
    // APIエンドポイントからPDFをフェッチ
    const response = await fetch("https://nextjsfastapisample-production.up.railway.app/api/generate-pdf");
    
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
    a.download = "sample.pdf";
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