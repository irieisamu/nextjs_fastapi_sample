import { useEffect, useState } from "react";
import { fetchMessage } from "../utils/api";

export default function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchMessage().then(setMessage);
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Hello from Next.js!</h1>
      <p>Message from FastAPI: {message}</p>
    </div>
  );
}
