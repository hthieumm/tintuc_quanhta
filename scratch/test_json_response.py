import os
import json
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL", "https://api.xah.io/v1")
model = os.getenv("LLM_MODEL_NAME", "dungcsnd113/gemini-flash-3.8")

prompt = """Bạn là chuyên gia phần mềm xuất sắc. Hãy phân tích và giải thích repo GitHub 'qdrant/qdrant' (Cơ sở dữ liệu Vector) bằng tiếng Việt thật dễ hiểu cho người mới học hoặc lập trình viên.
Trả về định dạng JSON thuần (chỉ JSON, không bọc markdown ```json):
{
  "what_it_does": "Giải thích ngắn gọn 1-2 câu repo này sinh ra để làm gì",
  "problem_solved": "Giải thích bài toán/nỗi đau thực tế nó giải quyết so với database truyền thống",
  "key_features": ["Tính năng 1", "Tính năng 2", "Tính năng 3"],
  "quickstart": "docker run -p 6333:6333 qdrant/qdrant",
  "target_audience": "Ai nên dùng repo này",
  "practical_use_case": "Ví dụ ứng dụng thực tế ngoài đời"
}"""

async def main():
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.3
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(f"{base_url}/chat/completions", headers=headers, json=payload)
        content = r.json()["choices"][0]["message"]["content"]
        clean = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean)
        with open("scratch/sample_explanation.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print("PARSED OK! Saved to scratch/sample_explanation.json")

if __name__ == "__main__":
    asyncio.run(main())
