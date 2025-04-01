import { useEffect, useState } from "react";
import { fetchMessage, downloadPdf } from "../utils/api";

export default function Home() {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMessage().then(setMessage);
  }, []);

  const handleDownloadPdf = async (useTtfFont: boolean = false) => {
    setIsLoading(true);
    setError(null);
    try {
      await downloadPdf(useTtfFont);
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
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Hello from Next.js!</h1>
      <p>Message from FastAPI: {message}</p>

      <div style={{ marginTop: "2rem" }}>
        <h2>PDFダウンロード</h2>
        <p>日本語フォントを使用したPDFをダウンロードできます。</p>
        
        <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
          <button
            onClick={() => handleDownloadPdf(false)}
            disabled={isLoading}
            style={buttonStyle("#0070f3")}
          >
            {isLoading ? "処理中..." : "組み込みフォントでPDFダウンロード"}
          </button>

          <button
            onClick={() => handleDownloadPdf(true)}
            disabled={isLoading}
            style={buttonStyle("#28a745")}
          >
            {isLoading ? "処理中..." : "TTFフォントでPDFダウンロード"}
          </button>
        </div>

        <div style={{ marginTop: "10px" }}>
          <small style={{ color: "#666" }}>
            * TTFフォントオプションは、サーバー側にIPAexフォントが配置されている場合のみ正常に動作します。
          </small>
        </div>

        {error && (
          <p style={{ color: "red", marginTop: "10px" }}>{error}</p>
        )}
      </div>
    </div>
  );
}