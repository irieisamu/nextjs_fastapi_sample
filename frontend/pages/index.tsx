import { useEffect, useState } from "react";
import { fetchMessage, downloadPdf } from "../utils/api";

export default function Home() {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMessage().then(setMessage);
  }, []);

  const handleDownloadPdf = async (type: 'reportlab' | 'reportlab-ttf' | 'weasyprint') => {
    setIsLoading(true);
    setError(null);
    try {
      await downloadPdf({ type });
    } catch (err) {
      setError("PDFのダウンロードに失敗しました。");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // ボタン用のスタイル
  const buttonStyle = (color: string) => ({
    padding: "10px 20px",
    fontSize: "16px",
    background: color,
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: isLoading ? "not-allowed" : "pointer",
    opacity: isLoading ? 0.7 : 1,
    marginRight: "10px",
    marginBottom: "10px",
  });

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ borderBottom: "1px solid #eee", paddingBottom: "10px" }}>Next.js + FastAPI デモ</h1>
      <p>Message from FastAPI: <strong>{message}</strong></p>

      <div style={{ marginTop: "2rem", background: "#f9f9f9", padding: "20px", borderRadius: "8px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
        <h2 style={{ color: "#333" }}>PDFダウンロード</h2>
        <p>異なるレンダリングエンジンを使用してPDFをダウンロードできます。</p>
        
        <div style={{ background: "#fff", padding: "15px", borderRadius: "6px", marginBottom: "15px" }}>
          <h3 style={{ fontSize: "18px", marginTop: 0 }}>ReportLab（基本的なレイアウト）</h3>
          <p>シンプルなレイアウトのPDFを生成します。日本語フォントをサポートしています。</p>
          <button
            onClick={() => handleDownloadPdf('reportlab')}
            disabled={isLoading}
            style={buttonStyle("#0070f3")}
          >
            {isLoading ? "処理中..." : "組み込みフォントでPDF生成"}
          </button>

          <button
            onClick={() => handleDownloadPdf('reportlab-ttf')}
            disabled={isLoading}
            style={buttonStyle("#0062cc")}
          >
            {isLoading ? "処理中..." : "TTFフォントでPDF生成"}
          </button>
        </div>

        <div style={{ background: "#fff", padding: "15px", borderRadius: "6px" }}>
          <h3 style={{ fontSize: "18px", marginTop: 0 }}>WeasyPrint（リッチなレイアウト）</h3>
          <p>HTML/CSSを使用した複雑なレイアウトのPDFを生成します。グリッドレイアウト、テーブル、カスタムスタイルをサポートしています。</p>
          <button
            onClick={() => handleDownloadPdf('weasyprint')}
            disabled={isLoading}
            style={buttonStyle("#28a745")}
          >
            {isLoading ? "処理中..." : "リッチなレイアウトでPDF生成"}
          </button>
        </div>

        <div style={{ marginTop: "15px", fontSize: "14px", color: "#666" }}>
          <p><strong>注意:</strong></p>
          <ul>
            <li>TTFフォントオプションは、サーバー側にIPAexフォントが配置されている場合のみ正常に動作します。</li>
            <li>WeasyPrintはサーバー側に正しくインストールされている必要があります。</li>
          </ul>
        </div>

        {error && (
          <div style={{ background: "#fff0f0", padding: "10px", borderLeft: "4px solid #ff0000", marginTop: "15px" }}>
            <p style={{ color: "#d32f2f", margin: 0 }}>{error}</p>
          </div>
        )}
      </div>
    </div>
  );
}