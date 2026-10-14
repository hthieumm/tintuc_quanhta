import os, httpx, asyncio, json
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL", "https://api.xah.io/v1")
# Try models: dungcsnd113/gemini-flash-3.8, deepseek-v4.1-flash, or configured model
models_to_try = [
    os.getenv("LLM_MODEL_NAME", "dungcsnd113/gemini-flash-3.8"),
    "dungcsnd113/gemini-flash-3.8",
    "deepseek-v4.1-flash",
    "gemini-2.5-flash-lite",
]

prompt = """Bạn là chuyên gia phần mềm xuất sắc. Hãy phân tích và giải thích repo GitHub 'qdrant/qdrant' (Cơ sở dữ liệu Vector) bằng tiếng Việt thật dễ hiểu cho người mới học hoặc lập trình viên.
Trả về định dạng JSON thuần (không kèm markdown ngoài) gồm:
{
  "what_it_does": "Giải thích ngắn gọn 1-2 câu repo này sinh ra để làm gì",
  "problem_solved": "Giải thích bài toán/nỗi đau thực tế nó giải quyết so với database truyền thống",
  "key_features": ["Tính năng 1", "Tính năng 2", "Tính năng 3"],
  "quickstart": "docker run -p 6333:6333 qdrant/qdrant",
  "target_audience": "Ai nên dùng repo này"
}"""

async def main():
    for model in models_to_try:
        print(f"Testing model: {model}...")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.3
        }
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                r = await client.post(f"{base_url}/chat/completions", headers=headers, json=payload)
                print("Status:", r.status_code)
                if r.status_code == 200:
                    resp_json = r.json()
                    content = resp_json["choices"][0]["message"]["content"]
                    print("SUCCESS! Output:")
                    print(content)
                    return model
                else:
                    print("Error response:", r.text[:200])
        except Exception as e:
            print("Exception:", e)

if __name__ == "__main__":
    asyncio.run(main())
