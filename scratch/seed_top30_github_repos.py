import sqlite3
import json
import os
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "spider_radar.db")
con = sqlite3.connect(db_path)
cur = con.cursor()

# Ensure table columns exist
cur.execute("PRAGMA table_info(github_repos)")
cols = [r[1] for r in cur.fetchall()]
for col, col_type in [
    ("description", "TEXT DEFAULT ''"),
    ("today_stars", "INTEGER DEFAULT 0"),
    ("tech_score", "REAL DEFAULT 9.0"),
    ("is_bookmarked", "INTEGER DEFAULT 0"),
    ("demo_code", "TEXT DEFAULT ''"),
    ("license", "TEXT DEFAULT 'Apache 2.0'")
]:
    if col not in cols:
        cur.execute(f"ALTER TABLE github_repos ADD COLUMN {col} {col_type}")

# Repositories dataset (30 repos)
repos_data = [
    {
        "repo_full_name": "Significant-Gravitas/AutoGPT",
        "repo_url": "https://github.com/Significant-Gravitas/AutoGPT",
        "stars": 168400,
        "today_stars": 185,
        "forks": 42100,
        "primary_language": "Python",
        "license": "MIT",
        "description": "AutoGPT is an experimental open-source autonomous agent system using LLMs to accomplish complex multi-step objectives.",
        "topics": ["ai", "agents", "llm", "automation"],
        "tech_score": 9.1,
        "is_bookmarked": 0,
        "demo_code": "from autogpt.agent import Agent\nagent = Agent.create(goal='Analyze macroeconomic news')\nagent.run()",
        "readme_content": "# AutoGPT: Autonomous AI Agent Platform\nAn autonomous AI agent that chains LLM thoughts to independently achieve goals."
    },
    {
        "repo_full_name": "AUTOMATIC1111/stable-diffusion-webui",
        "repo_url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
        "stars": 142300,
        "today_stars": 110,
        "forks": 27900,
        "primary_language": "Python",
        "license": "AGPL-3.0",
        "description": "Stable Diffusion web UI is the standard open-source browser interface based on Gradio for Stable Diffusion and generative AI models.",
        "topics": ["ai", "diffusion", "image-generation", "gradio"],
        "tech_score": 9.2,
        "is_bookmarked": 0,
        "demo_code": "import webui\nwebui.start_server(listen='127.0.0.1', port=7860)",
        "readme_content": "# Stable Diffusion Web UI\nA feature-rich browser UI for running text-to-image AI diffusion models locally."
    },
    {
        "repo_full_name": "huggingface/transformers",
        "repo_url": "https://github.com/huggingface/transformers",
        "stars": 135200,
        "today_stars": 195,
        "forks": 26800,
        "primary_language": "Python",
        "license": "Apache 2.0",
        "description": "Transformers provides thousands of pretrained models to perform tasks on texts, vision, and audio for PyTorch, TensorFlow, and JAX.",
        "topics": ["ai", "deep-learning", "pytorch", "nlp", "llm"],
        "tech_score": 9.8,
        "is_bookmarked": 1,
        "demo_code": "from transformers import pipeline\nclassifier = pipeline('sentiment-analysis')\nprint(classifier('Lãi suất giảm mạnh'))",
        "readme_content": "# 🤗 Transformers: State-of-the-Art Machine Learning\nTransformers provides APIs to quickly download and train state-of-the-art pretrained models."
    },
    {
        "repo_full_name": "langchain-ai/langchain",
        "repo_url": "https://github.com/langchain-ai/langchain",
        "stars": 98600,
        "today_stars": 140,
        "forks": 15400,
        "primary_language": "Python",
        "license": "MIT",
        "description": "Building context-aware reasoning applications with LangChain's composable components and LCEL orchestrations.",
        "topics": ["ai", "llm", "rag", "agents", "langchain"],
        "tech_score": 9.2,
        "demo_code": "from langchain_core.prompts import PromptTemplate\nprompt = PromptTemplate.from_template('Tóm tắt vĩ mô: {topic}')",
        "readme_content": "# LangChain: Modular Framework for LLM Apps\nComposable abstractions and tools to connect LLMs to company data sources and tools."
    },
    {
        "repo_full_name": "ollama/ollama",
        "repo_url": "https://github.com/ollama/ollama",
        "stars": 97400,
        "today_stars": 345,
        "forks": 8900,
        "primary_language": "Go / C++",
        "license": "MIT",
        "description": "Get up and running with Llama 3, DeepSeek-R1, Mistral, and other large language models locally on macOS, Linux, and Windows.",
        "topics": ["ai", "systems", "llm", "inference", "local-ai"],
        "tech_score": 9.7,
        "is_bookmarked": 1,
        "demo_code": "ollama run deepseek-r1:7b 'Phân tích tác động tăng lãi suất Fed'",
        "readme_content": "# Ollama: Run LLMs Locally with Zero Config\nOllama bundles model weights, configuration, and GPU acceleration into a single binary."
    },
    {
        "repo_full_name": "pytorch/pytorch",
        "repo_url": "https://github.com/pytorch/pytorch",
        "stars": 88700,
        "today_stars": 90,
        "forks": 22400,
        "primary_language": "C++ / Python",
        "license": "BSD-3-Clause",
        "description": "Tensors and Dynamic neural networks in Python with strong GPU acceleration, autograd, and TorchScript.",
        "topics": ["ai", "systems", "gpu", "deep-learning", "cuda"],
        "tech_score": 9.9,
        "demo_code": "import torch\nx = torch.randn(3, 3, device='cuda')\nprint(x.matmul(x.t()))",
        "readme_content": "# PyTorch: Tensors & Dynamic Neural Networks\nOpen source machine learning framework that accelerates the path from research prototyping to production."
    },
    {
        "repo_full_name": "tauri-apps/tauri",
        "repo_url": "https://github.com/tauri-apps/tauri",
        "stars": 84200,
        "today_stars": 120,
        "forks": 2500,
        "primary_language": "Rust / TypeScript",
        "license": "Apache 2.0",
        "description": "Build smaller, faster, and more secure desktop and mobile applications with a web frontend and Rust backend core.",
        "topics": ["systems", "rust", "desktop", "tauri-v2"],
        "tech_score": 9.8,
        "is_bookmarked": 1,
        "demo_code": "#[tauri::command]\nfn trigger_spider_event(target_word: &str) -> String {\n    format!('Spider crawled to {}', target_word)\n}",
        "readme_content": "# Tauri v2: Next-Gen Desktop App Runtime\nTauri is an app construction toolkit that lets you build native binaries with web technologies and Rust."
    },
    {
        "repo_full_name": "tiangolo/fastapi",
        "repo_url": "https://github.com/tiangolo/fastapi",
        "stars": 78500,
        "today_stars": 85,
        "forks": 6500,
        "primary_language": "Python",
        "license": "MIT",
        "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production with Starlette and Pydantic.",
        "topics": ["systems", "web", "api", "asyncio"],
        "tech_score": 9.6,
        "demo_code": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/v1/status')\ndef status(): return {'status': 'ok'}",
        "readme_content": "# FastAPI: High Performance Async Python API\nModern web framework for building APIs with Python 3.8+ based on standard Python type hints."
    },
    {
        "repo_full_name": "openai/whisper",
        "repo_url": "https://github.com/openai/whisper",
        "stars": 74300,
        "today_stars": 130,
        "forks": 8400,
        "primary_language": "Python",
        "license": "MIT",
        "description": "Robust Speech Recognition via Large-Scale Weak Supervision with multilingual transcription and translation.",
        "topics": ["ai", "speech", "transcription", "audio"],
        "tech_score": 9.5,
        "demo_code": "import whisper\nmodel = whisper.load_model('base')\nres = model.transcribe('macro_audio.mp3')",
        "readme_content": "# OpenAI Whisper: General-Purpose Speech Recognition\nWhisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual data."
    },
    {
        "repo_full_name": "ggml-org/llama.cpp",
        "repo_url": "https://github.com/ggml-org/llama.cpp",
        "stars": 68500,
        "today_stars": 240,
        "forks": 10200,
        "primary_language": "C / C++",
        "license": "MIT",
        "description": "LLM inference in C/C++ with AVX, NEON, CUDA, and Metal acceleration without external dependencies.",
        "topics": ["systems", "ai", "inference", "c++", "llm"],
        "tech_score": 9.9,
        "is_bookmarked": 1,
        "demo_code": "./main -m models/7B/ggml-model-q4_0.bin -p 'Kinh tế vĩ mô năm 2026' -n 128",
        "readme_content": "# llama.cpp: Port of Facebook's LLaMA model in C/C++\nPure C/C++ implementation for running LLM inference with integer quantization (2-bit to 8-bit)."
    },
    {
        "repo_full_name": "deepseek-ai/DeepSeek-R1",
        "repo_url": "https://github.com/deepseek-ai/DeepSeek-R1",
        "stars": 62400,
        "today_stars": 1240,
        "forks": 7800,
        "primary_language": "Python",
        "license": "MIT",
        "description": "Incentivizing Reasoning Capability in LLMs via Reinforcement Learning with zero supervised fine-tuning cold-start.",
        "topics": ["ai", "reasoning", "rl", "llm", "deepseek"],
        "tech_score": 9.9,
        "is_bookmarked": 1,
        "demo_code": "from transformers import AutoModelForCausalLM\nmodel = AutoModelForCausalLM.from_pretrained('deepseek-ai/DeepSeek-R1-Distill-Qwen-14B')",
        "readme_content": "# DeepSeek-R1: Open Reasoning Model via Pure RL\nDeepSeek-R1 achieves reasoning performance comparable to OpenAI-o1 across math, code, and logic."
    },
    {
        "repo_full_name": "comfyanonymous/ComfyUI",
        "repo_url": "https://github.com/comfyanonymous/ComfyUI",
        "stars": 56800,
        "today_stars": 215,
        "forks": 5900,
        "primary_language": "Python",
        "license": "GPL-3.0",
        "description": "The most powerful and modular stable diffusion GUI and backend with a graph/nodes interface.",
        "topics": ["ai", "nodes", "diffusion", "workflow"],
        "tech_score": 9.5,
        "demo_code": "python main.py --port 8188 --force-fp16",
        "readme_content": "# ComfyUI: Node-Based Generative AI Workspace\nAllows you to design and execute advanced Stable Diffusion, SDXL, and Flux pipelines."
    },
    {
        "repo_full_name": "deepseek-ai/DeepSeek-V3",
        "repo_url": "https://github.com/deepseek-ai/DeepSeek-V3",
        "stars": 45900,
        "today_stars": 890,
        "forks": 5400,
        "primary_language": "Python / CUDA",
        "license": "MIT",
        "description": "DeepSeek-V3 is a strong Mixture-of-Experts (MoE) language model with 671B total parameters and 37B activated per token.",
        "topics": ["ai", "llm", "moe", "cuda", "deepseek"],
        "tech_score": 9.8,
        "is_bookmarked": 1,
        "demo_code": "# DeepSeek-V3 Multi-head Latent Attention (MLA)\nmla_kv_cache = allocate_compressed_latent(tokens=4096)",
        "readme_content": "# DeepSeek-V3: Scalable Open Mixture-of-Experts\nFeatures Multi-head Latent Attention (MLA) and DeepSeekMoE architecture with FP8 mixed precision training."
    },
    {
        "repo_full_name": "meta-llama/llama3",
        "repo_url": "https://github.com/meta-llama/llama3",
        "stars": 43200,
        "today_stars": 150,
        "forks": 5200,
        "primary_language": "Python",
        "license": "Llama 3 Community",
        "description": "The official Meta Llama 3 and 3.1 codebase with group query attention and native 128k context support.",
        "topics": ["ai", "llm", "meta", "llama3"],
        "tech_score": 9.7,
        "demo_code": "from llama import Llama\ngenerator = Llama.build(ckpt_dir='Meta-Llama-3-8B', tokenizer_path='tokenizer.model')",
        "readme_content": "# Meta Llama 3 Architecture\nState-of-the-art pretrained and instruction tuned language models designed for developers."
    },
    {
        "repo_full_name": "astral-sh/uv",
        "repo_url": "https://github.com/astral-sh/uv",
        "stars": 41300,
        "today_stars": 380,
        "forks": 1200,
        "primary_language": "Rust",
        "license": "Apache 2.0 / MIT",
        "description": "An extremely fast Python package and project manager, written in Rust. 10-100x faster than pip.",
        "topics": ["systems", "rust", "python", "tooling"],
        "tech_score": 9.9,
        "is_bookmarked": 1,
        "demo_code": "uv pip install -r requirements.txt\nuv venv create .venv",
        "readme_content": "# uv: Extremely Fast Python Package Manager in Rust\nA single tool to replace pip, pip-tools, pipx, poetry, pyenv, and virtualenv."
    },
    {
        "repo_full_name": "microsoft/autogen",
        "repo_url": "https://github.com/microsoft/autogen",
        "stars": 37600,
        "today_stars": 125,
        "forks": 5100,
        "primary_language": "Python",
        "license": "CC-BY-4.0",
        "description": "A programming framework for agentic AI that enables multiple conversational agents to cooperate.",
        "topics": ["ai", "agents", "microsoft", "llm"],
        "tech_score": 9.3,
        "demo_code": "from autogen import AssistantAgent, UserProxyAgent\nassistant = AssistantAgent('analyst')\nuser = UserProxyAgent('user')",
        "readme_content": "# AutoGen: Multi-Agent Conversation Framework\nEnables next-gen LLM applications with multi-agent conversation orchestrated workflows."
    },
    {
        "repo_full_name": "astral-sh/ruff",
        "repo_url": "https://github.com/astral-sh/ruff",
        "stars": 36400,
        "today_stars": 95,
        "forks": 1100,
        "primary_language": "Rust",
        "license": "MIT",
        "description": "An extremely fast Python linter and code formatter, written in Rust. Drop-in replacement for Flake8, Black, and isort.",
        "topics": ["systems", "rust", "linter", "formatter"],
        "tech_score": 9.8,
        "demo_code": "ruff check backend/\nruff format backend/",
        "readme_content": "# Ruff: Ultra-Fast Python Linter in Rust\n10-100x faster than traditional Python linters with near-instant pre-commit checks."
    },
    {
        "repo_full_name": "ggerganov/whisper.cpp",
        "repo_url": "https://github.com/ggerganov/whisper.cpp",
        "stars": 35100,
        "today_stars": 80,
        "forks": 3800,
        "primary_language": "C / C++",
        "license": "MIT",
        "description": "Port of OpenAI's Whisper model in C/C++ with zero dependencies and native WASM support.",
        "topics": ["systems", "wasm", "speech", "c++"],
        "tech_score": 9.6,
        "demo_code": "./main -m models/ggml-base.en.bin -f samples/audio.wav",
        "readme_content": "# whisper.cpp: High-Performance Whisper Inference\nLightweight C/C++ speech transcription with ARM NEON, AVX, Metal, and WebAssembly support."
    },
    {
        "repo_full_name": "vllm-project/vllm",
        "repo_url": "https://github.com/vllm-project/vllm",
        "stars": 32400,
        "today_stars": 280,
        "forks": 4900,
        "primary_language": "Python / C++",
        "license": "Apache 2.0",
        "description": "A high-throughput and memory-efficient inference and serving engine for LLMs with PagedAttention.",
        "topics": ["ai", "systems", "inference", "gpu", "vllm"],
        "tech_score": 9.8,
        "is_bookmarked": 1,
        "demo_code": "from vllm import LLM, SamplingParams\nllm = LLM(model='meta-llama/Llama-3-8b')\noutputs = llm.generate(['Dự báo lạm phát 2026:'])",
        "readme_content": "# vLLM: High-Throughput Serving Engine with PagedAttention\nvLLM delivers 24x higher throughput than HuggingFace Transformers by eliminating KV cache memory fragmentation."
    },
    {
        "repo_full_name": "milvus-io/milvus",
        "repo_url": "https://github.com/milvus-io/milvus",
        "stars": 31200,
        "today_stars": 75,
        "forks": 3100,
        "primary_language": "Go / C++",
        "license": "Apache 2.0",
        "description": "Milvus is an open-source vector database built to power embedding similarity search and AI applications.",
        "topics": ["vector", "systems", "database", "similarity-search"],
        "tech_score": 9.4,
        "demo_code": "from pymilvus import Collection\ncol = Collection('macro_embeddings')\ncol.search(vectors=[query_vector], anns_field='embedding', param={'metric_type': 'COSINE'})",
        "readme_content": "# Milvus: Distributed Vector Database for AI\nDesigned for massive-scale similarity search and multimodal retrieval."
    },
    {
        "repo_full_name": "facebookresearch/faiss",
        "repo_url": "https://github.com/facebookresearch/faiss",
        "stars": 30100,
        "today_stars": 65,
        "forks": 5800,
        "primary_language": "C++ / Python",
        "license": "MIT",
        "description": "A library for efficient similarity search and clustering of dense vectors, supporting GPU indexes.",
        "topics": ["vector", "systems", "c++", "gpu"],
        "tech_score": 9.7,
        "demo_code": "import faiss\nindex = faiss.IndexFlatL2(d)\nindex.add(xb)\nD, I = index.search(xq, k)",
        "readme_content": "# FAISS: Efficient Similarity Search of Dense Vectors\nGPU-accelerated vector indexing engine powering recommendation and RAG systems."
    },
    {
        "repo_full_name": "tinygrad/tinygrad",
        "repo_url": "https://github.com/tinygrad/tinygrad",
        "stars": 29400,
        "today_stars": 110,
        "forks": 2600,
        "primary_language": "Python",
        "license": "MIT",
        "description": "You like pytorch? You like micrograd? You want a simpler framework? tinygrad is a minimalist deep learning framework.",
        "topics": ["ai", "systems", "deep-learning", "compiler"],
        "tech_score": 9.5,
        "demo_code": "from tinygrad.tensor import Tensor\nx = Tensor.eye(3).requires_grad_()\ny = x * 2\ny.backward()",
        "readme_content": "# tinygrad: Minimalist Deep Learning Framework\nA small, understandable, and fast framework for neural networks."
    },
    {
        "repo_full_name": "QwenLM/Qwen2.5",
        "repo_url": "https://github.com/QwenLM/Qwen2.5",
        "stars": 26800,
        "today_stars": 165,
        "forks": 2100,
        "primary_language": "Python",
        "license": "Apache 2.0",
        "description": "Qwen2.5 is the large language model and large multimodal model series by Alibaba Cloud.",
        "topics": ["ai", "llm", "qwen", "multimodal"],
        "tech_score": 9.7,
        "demo_code": "from transformers import AutoModelForCausalLM\nmodel = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct')",
        "readme_content": "# Qwen2.5 Series\nHigh-performance open language models with strong multilingual and coding capabilities."
    },
    {
        "repo_full_name": "qdrant/qdrant",
        "repo_url": "https://github.com/qdrant/qdrant",
        "stars": 21400,
        "today_stars": 115,
        "forks": 1600,
        "primary_language": "Rust",
        "license": "Apache 2.0",
        "description": "High-performance, massive-scale Vector Database and Vector Search Engine written in Rust.",
        "topics": ["vector", "systems", "rust", "search"],
        "tech_score": 9.6,
        "is_bookmarked": 1,
        "demo_code": "from qdrant_client import QdrantClient\nclient = QdrantClient(':memory:')\nclient.search(collection_name='news', query_vector=vec, limit=5)",
        "readme_content": "# Qdrant Vector Database in Rust\nFast and reliable vector similarity search engine with JSON payload filtering."
    },
    {
        "repo_full_name": "chroma-core/chroma",
        "repo_url": "https://github.com/chroma-core/chroma",
        "stars": 16300,
        "today_stars": 60,
        "forks": 1400,
        "primary_language": "Python / Rust",
        "license": "Apache 2.0",
        "description": "Chroma is the AI-native open-source embedding database designed for developer ergonomics.",
        "topics": ["vector", "ai", "database", "rag"],
        "tech_score": 9.2,
        "demo_code": "import chromadb\nclient = chromadb.Client()\ncollection = client.create_collection('articles')\ncollection.add(documents=['Lãi suất VN'], ids=['doc1'])",
        "readme_content": "# Chroma: Open-Source AI Embedding Database\nSimple and powerful vector database for LLM retrieval-augmented generation."
    },
    {
        "repo_full_name": "huggingface/candle",
        "repo_url": "https://github.com/huggingface/candle",
        "stars": 15200,
        "today_stars": 95,
        "forks": 1100,
        "primary_language": "Rust",
        "license": "Apache 2.0 / MIT",
        "description": "Candle is a minimalist ML framework for Rust with a focus on performance (including GPU support) and ease of use.",
        "topics": ["systems", "rust", "ai", "inference", "wasm"],
        "tech_score": 9.5,
        "demo_code": "use candle_core::{Device, Tensor};\nlet a = Tensor::new(&[[1f32, 2.], [3., 4.]], &Device::Cpu)?;\nlet b = a.matmul(&a)?;\nprintln!(\"{:?}\", b);",
        "readme_content": "# Candle: Minimalist ML Framework for Rust\nServerless and edge inference with zero PyTorch/Python dependencies."
    },
    {
        "repo_full_name": "bytecodealliance/wasmtime",
        "repo_url": "https://github.com/bytecodealliance/wasmtime",
        "stars": 14900,
        "today_stars": 45,
        "forks": 1200,
        "primary_language": "Rust",
        "license": "Apache 2.0 with LLVM Exception",
        "description": "A fast and secure runtime for WebAssembly and WASI, developed by the Bytecode Alliance.",
        "topics": ["wasm", "systems", "rust", "edge", "runtime"],
        "tech_score": 9.7,
        "demo_code": "wasmtime run --env PORT=8000 spider_reflex.wasm",
        "readme_content": "# Wasmtime: Standalone WebAssembly Runtime in Rust\nFast and sandboxed WebAssembly execution engine compliant with modern WASI standards."
    },
    {
        "repo_full_name": "triton-lang/triton",
        "repo_url": "https://github.com/triton-lang/triton",
        "stars": 14200,
        "today_stars": 55,
        "forks": 1500,
        "primary_language": "C++ / Python",
        "license": "MIT",
        "description": "Development environment for parallel algorithms and compilers to write highly efficient GPU code with Python-like ease.",
        "topics": ["ai", "systems", "gpu", "cuda", "compiler"],
        "tech_score": 9.8,
        "demo_code": "import triton\nimport triton.language as tl\n@triton.jit\ndef add_kernel(x_ptr, y_ptr, output_ptr, n_elements, BLOCK_SIZE: tl.constexpr): pass",
        "readme_content": "# Triton: Language & Compiler for Parallel Algorithms\nProductive programming environment for custom GPU compute kernels."
    },
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
        "demo_code": "from decision_engine import SystemOneEngine\nengine = SystemOneEngine.load('checkpoints/decision3_core.safetensors')\nresult = engine.predict_binary(text='Lãi suất điều hành tăng nhẹ')\nprint(f'Decision: {result.decision}, Latency: {result.latency_ms}ms')",
        "readme_content": "# Decision 3 Lite: Sub-10ms Reflexive Reasoning Engine\nDecision 3 Lite handles intuitive System 1 passes with sub-10ms latency on CPU with 180MB RAM."
    },
    {
        "repo_full_name": "NandhaKishorM/laya",
        "repo_url": "https://github.com/NandhaKishorM/laya",
        "stars": 3450,
        "today_stars": 310,
        "forks": 240,
        "primary_language": "Python / CUDA",
        "license": "MIT",
        "description": "Laya: Latent Action Policy for Autonomous Web & System Navigation with RL and tensor-level feedback.",
        "topics": ["ai", "rl", "cuda", "laya"],
        "tech_score": 9.4,
        "is_bookmarked": 1,
        "demo_code": "from laya_agent import LayaPolicy\nagent = LayaPolicy(cuda_device=0)\naction = agent.step(observation={'word': 'Lãi suất', 'screen': 'SpiderArena'})\nprint(f'Dispatched spider web silk action: {action}')",
        "readme_content": "# Laya: Latent Action Reinforcement Learning Agent\nHigh-performance RL agent optimized for real-time web navigation and sub-50ms reactive triggers."
    }
]

# Insert or update
for r in repos_data:
    cur.execute("""
        INSERT INTO github_repos (
            repo_full_name, repo_url, stars, forks, primary_language,
            license, description, topics_json, tech_score, is_bookmarked,
            demo_code, readme_content, today_stars, crawled_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(repo_full_name) DO UPDATE SET
            stars=excluded.stars,
            today_stars=excluded.today_stars,
            forks=excluded.forks,
            primary_language=excluded.primary_language,
            license=excluded.license,
            description=excluded.description,
            topics_json=excluded.topics_json,
            tech_score=excluded.tech_score,
            is_bookmarked=CASE WHEN github_repos.is_bookmarked = 1 THEN 1 ELSE excluded.is_bookmarked END,
            demo_code=excluded.demo_code,
            readme_content=excluded.readme_content
    """, (
        r["repo_full_name"], r["repo_url"], r["stars"], r["forks"], r["primary_language"],
        r["license"], r["description"], json.dumps(r["topics"], ensure_ascii=False),
        r["tech_score"], r.get("is_bookmarked", 0), r["demo_code"], r["readme_content"],
        r["today_stars"]
    ))

con.commit()

# Record sync in system_settings
today_str = datetime.now().strftime("%Y-%m-%d")
now_iso = datetime.now().isoformat()
cur.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES ('github_last_sync_date', ?)", (today_str,))
cur.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES ('github_last_sync_time', ?)", (now_iso,))
con.commit()

cur.execute("SELECT count(*) FROM github_repos")
print(f"Total repos in DB: {cur.fetchone()[0]}")
cur.execute("SELECT repo_full_name, stars FROM github_repos ORDER BY stars DESC LIMIT 5")
print("Top 5 stars:", cur.fetchall())
cur.execute("SELECT repo_full_name, today_stars FROM github_repos ORDER BY today_stars DESC LIMIT 5")
print("Top 5 fastest growth:", cur.fetchall())
con.close()
