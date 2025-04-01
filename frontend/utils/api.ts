export async function fetchMessage(): Promise<string> {
  const res = await fetch("https://nextjsfastapisample-production.up.railway.app/api/hello");
  const data = await res.json();
  return data.message;
}
