import csv, os, time
from dotenv import load_dotenv
import requests

load_dotenv()

os.makedirs("data", exist_ok=True)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "nvidia/nemotron-3-nano-30b-a3b")
SYSTEM = "Ты редактор новостей. Напиши краткое резюме (2-4 предложения) на русском. Только текст резюме."

def llm(prompt: str) -> str:
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}], "max_tokens": 300, "temperature": 0.3},
        timeout=60
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

csv_path = "input.csv"
out_path = "output.txt"

rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
results = []
for i, row in enumerate(rows, 1):
    text = row.get("text", row.get("content", ""))
    title = row.get("title", row.get("headline", ""))
    try:
        results.append(f"{'='*50}\n{title}\n\n{llm(f'Заголовок: {title}\n\nТекст: {text}\n\nРезюме:').strip()}\n")
    except Exception as e:
        results.append(f"{'='*50}\n{title}\n\n[ОШИБКА: {e}]\n")
    if i < len(rows): time.sleep(1)
open(out_path, "w", encoding="utf-8").write("\n".join(results))
