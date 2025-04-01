import { useEffect, useState } from "react";
import { fetchMessage, downloadPdf } from "../utils/api";

export default function Home() {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMessage().then(setMessage);
  }, []);

  const handleDownloadPdf = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await downloadPdf();
    } catch (err) {
      setError("PDFのダウンロードに失敗しました。");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Hello from Next.js!</h1>
      <p>Message from FastAPI: {message}</p>

      <div style={{ marginTop: "2rem" }}>
        <button
          onClick={handleDownloadPdf}
          disabled={isLoading}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            background: "#0070f3",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: isLoading ? "not-allowed" : "pointer",
            opacity: isLoading ? 0.7 : 1,
          }}
        >
          {isLoading ? "処理中..." : "PDFをダウンロード"}
        </button>

        {error && (
          <p style={{ color: "red", marginTop: "10px" }}>{error}</p>
        )}
      </div>
    </div>
  );
}