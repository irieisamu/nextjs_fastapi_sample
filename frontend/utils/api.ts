export async function fetchMessage(): Promise<string> {
  const res = await fetch("http://localhost:8000/api/hello");
  const data = await res.json();
  return data.message;
}
