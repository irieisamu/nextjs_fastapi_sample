export async function fetchMessage(): Promise<string> {
  const res = await fetch("https://nextjsfastapisample-production.up.railway.app/api/hello");
  const data = await res.json();
  return data.message;
}

export async function downloadPdf(useTtfFont: boolean = false): Promise<void> {
  try {
    // 使用するエンドポイントを選択
    const endpoint = useTtfFont 
      ? "https://nextjsfastapisample-production.up.railway.app/api/generate-pdf-with-ttf"
      : "https://nextjsfastapisample-production.up.railway.app/api/generate-pdf";
    
    // APIエンドポイントからPDFをフェッチ
    const response = await fetch(endpoint);
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    // レスポンスをBlobに変換
    const blob = await response.blob();
    
    // BlobからURLを作成
    const url = window.URL.createObjectURL(blob);
    
    // ファイル名を決定
    const filename = useTtfFont ? "sample_with_ttf.pdf" : "sample.pdf";
    
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