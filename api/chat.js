hereexport default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const { model, message } = req.body;

  try {
    const r = await fetch(
      `https://dv-codex.vercel.app/api/v1/ai/chat/${model}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      }
    );

    const data = await r.text();
    res.status(200).send(data);
  } catch {
    res.status(500).send("Error");
  }
}
