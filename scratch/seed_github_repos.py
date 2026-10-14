import sqlite3
import json
from datetime import datetime, timezone

DB_PATH = 'backend/data/spider_radar.db'

def setup_and_seed_github():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Thêm các cột bổ trợ nếu chưa có
    cols = [col[1] for col in c.execute('PRAGMA table_info(github_repos)').fetchall()]
    
    if 'description' not in cols:
        c.execute('ALTER TABLE github_repos ADD COLUMN description TEXT DEFAULT ""')
    if 'today_stars' not in cols:
        c.execute('ALTER TABLE github_repos ADD COLUMN today_stars INTEGER DEFAULT 0')
    if 'tech_score' not in cols:
        c.execute('ALTER TABLE github_repos ADD COLUMN tech_score REAL DEFAULT 9.0')
    if 'is_bookmarked' not in cols:
        c.execute('ALTER TABLE github_repos ADD COLUMN is_bookmarked INTEGER DEFAULT 0')
    if 'demo_code' not in cols:
        c.execute('ALTER TABLE github_repos ADD COLUMN demo_code TEXT DEFAULT ""')
    if 'license' not in cols:
        c.execute('ALTER TABLE github_repos ADD COLUMN license TEXT DEFAULT "Apache 2.0"')

    # 2. Danh sách các Repositories công nghệ AI & Systems chuẩn đặc tả
    repos = [
        {
            "repo_full_name": "decision-ai/decision-3-lite",
            "repo_url": "https://github.com/decision-ai/decision-3-lite",
            "stars": 4821,
            "today_stars": 421,
            "forks": 382,
            "primary_language": "Rust / Python",
            "license": "Apache 2.0",
            "description": "An ultra-fast System 1 reflexive reasoning engine designed for deterministic text classification and prompt pre-filtering.",
            "topics": ["ai", "inference", "edge", "decision3"],
            "tech_score": 9.6,
            "is_bookmarked": 1,
            "demo_code": """from decision_engine import SystemOneEngine, TensorClassifier

# 1. Tải checkpoint siêu nhẹ (180MB RAM footprint trong Docker)
engine = SystemOneEngine.load('checkpoints/decision3_core.safetensors')

# 2. Suy luận nhị phân siêu tốc độ (Single-pass tensor)
result = engine.predict_binary(text='Lãi suất điều hành tăng nhẹ')

# 3. Trả về kết quả cho Spider Canvas trong 5.4ms
print(f'Decision: {result.decision}, Latency: {result.latency_ms}ms')""",
            "readme_content": """# Decision 3 Lite: Sub-10ms Reflexive Reasoning Engine

Decision 3 Lite đóng vai trò là tầng phản xạ trực giác (Reflexive Pass Layer), giúp nhận diện và gán nhãn thực thể với độ trễ sub-10ms mà không tiêu tốn tài nguyên GPU. Nó chạy hoàn hảo trong Docker container trên CPU với chỉ 180MB RAM.

### Điểm nổi bật
- **Độ trễ suy luận (P50)**: 5.4ms trên CPU x86/ARM
- **Mức tiêu thụ bộ nhớ**: 180MB RAM footprint
- **Khả năng nhúng**: Docker C-FFI ready (Port 8000)
- **Tích hợp Spider News Radar**: Giúp tiết kiệm tới 84.6% token gọi LLM System 2.

### Cài đặt nhanh Docker:
```bash
docker run -d -p 8000:8000 decision-3-lite-serve:latest
```"""
        },
        {
            "repo_full_name": "NandhaKishorM/laya",
            "repo_url": "https://github.com/NandhaKishorM/laya",
            "stars": 3450,
            "today_stars": 310,
            "forks": 290,
            "primary_language": "Python / CUDA",
            "license": "MIT",
            "description": "Laya Reinforcement Learning Agent - Real-time policy decision making engine with 30-60ms GPU inference latency.",
            "topics": ["ai", "reinforcement-learning", "robotics", "cuda"],
            "tech_score": 9.2,
            "is_bookmarked": 1,
            "demo_code": """import laya
import torch

agent = laya.Agent.load_policy('policy_v2.pt', device='cuda:0')
obs = torch.tensor([0.45, 0.12, -0.08, 0.95], device='cuda:0')
action, latency_ms = agent.step(obs)
print(f'Laya Action: {action}, Inference: {latency_ms:.2f}ms')""",
            "readme_content": """# Laya RL Agent: High-Performance Decision Framework

Laya là động cơ RL chuyên dụng phục vụ các tác vụ ra quyết định tức thời với độ trễ từ 30ms đến 60ms trên GPU CUDA NVIDIA.

### Đặc tả kỹ thuật
- Tối ưu hóa TensorRT và CUDA Graph execution
- Hỗ trợ endpoint `/v1/systemone` tương thích trực tiếp với Spider News Radar
- Tối ưu bộ nhớ VRAM, tự động giải phóng khi không tải trọng."""
        },
        {
            "repo_full_name": "vllm-project/vllm",
            "repo_url": "https://github.com/vllm-project/vllm",
            "stars": 28100,
            "today_stars": 180,
            "forks": 4200,
            "primary_language": "Python / C++",
            "license": "Apache 2.0",
            "description": "A high-throughput and memory-efficient inference and serving engine for LLMs with PagedAttention.",
            "topics": ["ai", "systems", "llm-serving", "paged-attention"],
            "tech_score": 9.5,
            "is_bookmarked": 0,
            "demo_code": """from vllm import LLM, SamplingParams

prompts = ["Phân tích tác động của việc FED nới lỏng lãi suất:"]
sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=100)

llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")
outputs = llm.generate(prompts, sampling_params)
print(outputs[0].outputs[0].text)""",
            "readme_content": """# vLLM: Easy, Fast, and Cheap LLM Serving for Everyone

vLLM là thư viện phục vụ mô hình ngôn ngữ lớn (LLM) tiêu chuẩn công nghiệp với kiến trúc quản lý bộ nhớ PagedAttention đột phá.

### Tính năng cốt lõi
- Tăng thông lượng phục vụ lên 2x-4x so với HuggingFace TGI
- Hỗ trợ suy luận phân tán nhiều GPU (Tensor Parallelism)
- Tương thích 100% OpenAI API protocol."""
        },
        {
            "repo_full_name": "huggingface/candle",
            "repo_url": "https://github.com/huggingface/candle",
            "stars": 15200,
            "today_stars": 95,
            "forks": 1100,
            "primary_language": "Rust",
            "license": "Apache 2.0",
            "description": "Minimalist ML framework for Rust with focus on performance, ease of use, and serverless deployment.",
            "topics": ["systems", "rust", "inference", "wasm"],
            "tech_score": 9.0,
            "is_bookmarked": 1,
            "demo_code": """use candle_core::{Device, Tensor};

fn main() -> candle_core::Result<()> {
    let device = Device::Cpu;
    let a = Tensor::randn(0f32, 1., (2, 3), &device)?;
    let b = Tensor::randn(0f32, 1., (3, 4), &device)?;
    let c = a.matmul(&b)?;
    println!("Matrix product: {:?}", c);
    Ok(())
}""",
            "readme_content": """# Candle: Minimalist ML Framework for Rust

Candle là framework học máy tối giản được xây dựng bởi HuggingFace dành riêng cho Rust, hướng tới khả năng triển khai biên (Edge) và Serverless không cần runtime Python cồng kềnh.

### Ưu điểm
- Khởi động tức thì (Cold start < 1ms)
- Không phụ thuộc PyTorch hay CUDA phức tạp
- Biên dịch trực tiếp sang WebAssembly (Wasm)."""
        },
        {
            "repo_full_name": "ggml-org/llama.cpp",
            "repo_url": "https://github.com/ggml-org/llama.cpp",
            "stars": 64500,
            "today_stars": 240,
            "forks": 9200,
            "primary_language": "C / C++",
            "license": "MIT",
            "description": "LLM inference in C/C++ with minimal setup and state-of-the-art performance on a wide variety of hardware.",
            "topics": ["systems", "edge", "quantization", "c++"],
            "tech_score": 9.8,
            "is_bookmarked": 0,
            "demo_code": """// llama.cpp execution
#include "llama.h"

int main() {
    llama_backend_init();
    llama_model_params model_params = llama_model_default_params();
    llama_model * model = llama_load_model_from_file("models/model.gguf", model_params);
    // Execute inference...
    llama_backend_free();
    return 0;
}""",
            "readme_content": """# llama.cpp: Port of Facebook's LLaMA model in C/C++

Mục tiêu chính của llama.cpp là cho phép suy luận LLM với thiết lập tối thiểu và hiệu năng tối đa trên CPU thông thường và GPU thương mại (Apple Metal, Vulkan, CUDA)."""
        },
        {
            "repo_full_name": "qdrant/qdrant",
            "repo_url": "https://github.com/qdrant/qdrant",
            "stars": 21400,
            "today_stars": 115,
            "forks": 1600,
            "primary_language": "Rust",
            "license": "Apache 2.0",
            "description": "Qdrant - High-performance, massive-scale Vector Database and Vector Search Engine written in Rust.",
            "topics": ["vector", "search", "database", "rust"],
            "tech_score": 9.4,
            "is_bookmarked": 1,
            "demo_code": """from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)
client.recreate_collection(
    collection_name="macro_news",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)
print("Qdrant collection ready for macro embeddings!")""",
            "readme_content": """# Qdrant Vector Database

Qdrant là cơ sở dữ liệu véc-tơ hiệu năng cao viết bằng Rust, hỗ trợ tìm kiếm láng giềng gần nhất (HNSW) kết hợp bộ lọc payload JSON thời gian thực cực kỳ linh hoạt."""
        },
        {
            "repo_full_name": "bytecodealliance/wasmtime",
            "repo_url": "https://github.com/bytecodealliance/wasmtime",
            "stars": 14900,
            "today_stars": 45,
            "forks": 1400,
            "primary_language": "Rust",
            "license": "Apache 2.0",
            "description": "A fast and secure runtime for WebAssembly and WASI by the Bytecode Alliance.",
            "topics": ["wasm", "edge", "systems", "rust"],
            "tech_score": 9.1,
            "is_bookmarked": 0,
            "demo_code": """use wasmtime::*;

fn main() -> Result<()> {
    let engine = Engine::default();
    let module = Module::from_file(&engine, "spider_filter.wasm")?;
    let mut store = Store::new(&engine, ());
    let instance = Instance::new(&mut store, &module, &[])?;
    println!("WebAssembly Spider sandbox initialized!");
    Ok(())
}""",
            "readme_content": """# Wasmtime: A small and fast WebAssembly runtime

Wasmtime là môi trường thực thi WebAssembly độc lập, an toàn và tối ưu hóa cao độ, được thiết kế cho các tác vụ tính toán biên và plugin sandbox."""
        },
        {
            "repo_full_name": "chroma-core/chroma",
            "repo_url": "https://github.com/chroma-core/chroma",
            "stars": 14800,
            "today_stars": 60,
            "forks": 1300,
            "primary_language": "Python / Rust",
            "license": "Apache 2.0",
            "description": "Chroma - the open-source AI-native embedding database for LLM apps.",
            "topics": ["vector", "ai", "search", "embeddings"],
            "tech_score": 8.9,
            "is_bookmarked": 0,
            "demo_code": """import chromadb

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="spider_knowledge")
collection.add(
    documents=["Lãi suất điều hành FED giữ nguyên 5.25%-5.50%"],
    ids=["doc1"]
)
results = collection.query(query_texts=["Lãi suất Mỹ"], n_results=1)
print(results)""",
            "readme_content": """# Chroma: The AI-native open-source embedding database

Chroma là cơ sở dữ liệu nhúng mở được thiết kế giúp xây dựng ứng dụng LLM với bộ nhớ truy xuất tài liệu (RAG) đơn giản nhất."""
        }
    ]

    for r in repos:
        c.execute("""
            INSERT OR REPLACE INTO github_repos (
                repo_full_name, repo_url, stars, forks, primary_language,
                topics_json, readme_content, description, today_stars,
                tech_score, is_bookmarked, demo_code, license, crawled_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            r["repo_full_name"],
            r["repo_url"],
            r["stars"],
            r["forks"],
            r["primary_language"],
            json.dumps(r["topics"], ensure_ascii=False),
            r["readme_content"],
            r["description"],
            r["today_stars"],
            r["tech_score"],
            r["is_bookmarked"],
            r["demo_code"],
            r["license"]
        ))

    conn.commit()
    count = c.execute("SELECT COUNT(*) FROM github_repos").fetchone()[0]
    conn.close()
    print(f"Hoàn tất nạp dữ liệu GitHub Repos! Tổng số repos trong SQLite: {count}")

if __name__ == "__main__":
    setup_and_seed_github()
