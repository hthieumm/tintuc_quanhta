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

# Comprehensive, diverse GitHub repositories (from Canva/Design to Skills, UI, AI, Tools)
repos_data = [
    # --- SKILLS & EDUCATION ---
    {
        "repo_full_name": "freeCodeCamp/freeCodeCamp",
        "repo_url": "https://github.com/freeCodeCamp/freeCodeCamp",
        "stars": 410000,
        "today_stars": 230,
        "forks": 38500,
        "primary_language": "TypeScript / JavaScript",
        "license": "BSD-3-Clause",
        "description": "freeCodeCamp.org's open-source codebase and curriculum. Learn to code for free with millions of learners worldwide.",
        "topics": ["skills", "education", "curriculum", "javascript", "learning"],
        "tech_score": 9.9,
        "is_bookmarked": 1,
        "demo_code": "npm install\nnpm run develop # Chạy nền tảng học kỹ năng lập trình mã nguồn mở",
        "readme_content": "# freeCodeCamp: Toàn Cầu Học Kỹ Năng Lập Trình\nNền tảng đào tạo kỹ năng lập trình lớn nhất thế giới, cung cấp chứng chỉ miễn phí về Web Development, Data Science và AI."
    },
    {
        "repo_full_name": "sindresorhus/awesome",
        "repo_url": "https://github.com/sindresorhus/awesome",
        "stars": 350000,
        "today_stars": 180,
        "forks": 29400,
        "primary_language": "Markdown",
        "license": "CC0-1.0",
        "description": "Awesome lists about all kinds of interesting topics, software, design skills, frameworks, and tools across GitHub.",
        "topics": ["skills", "curated-list", "awesome", "resources"],
        "tech_score": 9.7,
        "demo_code": "# Khám phá hàng nghìn thư viện và kỹ năng tốt nhất\ngit clone https://github.com/sindresorhus/awesome.git",
        "readme_content": "# Awesome: Danh Mục Tổng Hợp Mọi Kỹ Năng & Thư Viện\nKho tài nguyên curated lớn nhất trên GitHub về mọi lĩnh vực từ Frontend, Backend, Thiết kế đến Machine Learning."
    },
    {
        "repo_full_name": "kamranahmedse/developer-roadmap",
        "repo_url": "https://github.com/kamranahmedse/developer-roadmap",
        "stars": 305000,
        "today_stars": 260,
        "forks": 39500,
        "primary_language": "TypeScript",
        "license": "CC-BY-NC-SA-4.0",
        "description": "Interactive roadmaps, guides, and other educational content to help developers grow in their careers and master new skills.",
        "topics": ["skills", "roadmap", "career", "developer-guide"],
        "tech_score": 9.8,
        "is_bookmarked": 1,
        "demo_code": "npm install && npm run dev # Khởi chạy bản đồ lộ trình kỹ năng tương tác",
        "readme_content": "# Developer Roadmaps: Lộ Trình Kỹ Năng Lập Trình Viên\nBản đồ định hướng kỹ năng toàn diện cho Frontend, Backend, DevOps, AI Engineer và System Architect."
    },
    {
        "repo_full_name": "public-apis/public-apis",
        "repo_url": "https://github.com/public-apis/public-apis",
        "stars": 325000,
        "today_stars": 170,
        "forks": 34800,
        "primary_language": "Python",
        "license": "MIT",
        "description": "A collective list of free APIs for use in software and web development across finance, news, weather, and tools.",
        "topics": ["skills", "api", "web", "public-data"],
        "tech_score": 9.5,
        "demo_code": "import requests\nres = requests.get('https://api.publicapis.org/entries')\nprint(res.json()['count'])",
        "readme_content": "# Public APIs: Kho API Mở Toàn Cầu\nTổng hợp các API công khai miễn phí để phát triển ứng dụng di động, web và hệ thống tự động hóa."
    },

    # --- DESIGN / CANVA / WHITEBOARD / CREATIVE TECH ---
    {
        "repo_full_name": "penpot/penpot",
        "repo_url": "https://github.com/penpot/penpot",
        "stars": 36000,
        "today_stars": 540,
        "forks": 2100,
        "primary_language": "Clojure / TypeScript",
        "license": "MPL-2.0",
        "description": "Penpot: The open-source design and prototyping platform for product teams. A free, self-hostable alternative to Canva & Figma based on SVG standards.",
        "topics": ["design", "canva", "figma", "svg", "prototyping", "ui-ux"],
        "tech_score": 9.8,
        "is_bookmarked": 1,
        "demo_code": "# Chạy nền tảng thiết kế Penpot tương tự Canva qua Docker\ndocker compose -f docker-compose.yaml up -d",
        "readme_content": "# Penpot: Nền Tảng Thiết Kế Mở (Giải Pháp Thay Thế Canva & Figma)\nPenpot là công cụ thiết kế đồ họa vector và tạo mẫu giao diện web/app đầu tiên chạy trực tiếp trên chuẩn SVG, cho phép tự host 100%."
    },
    {
        "repo_full_name": "excalidraw/excalidraw",
        "repo_url": "https://github.com/excalidraw/excalidraw",
        "stars": 86000,
        "today_stars": 280,
        "forks": 8400,
        "primary_language": "TypeScript",
        "license": "MIT",
        "description": "Virtual whiteboard for sketching hand-drawn like diagrams. Collaborative, lightweight infinite canvas for creative work and architecture design.",
        "topics": ["design", "canvas", "whiteboard", "canva", "diagrams"],
        "tech_score": 9.7,
        "is_bookmarked": 1,
        "demo_code": "import { Excalidraw } from '@excalidraw/excalidraw';\nexport default () => <div style={{ height: '500px' }}><Excalidraw /></div>;",
        "readme_content": "# Excalidraw: Bảng Vẽ Sáng Tạo Vô Tận\nCông cụ vẽ sơ đồ phác thảo tay và bảng trắng số hóa phong cách Canva, hỗ trợ cộng tác thời gian thực và xuất vector SVG/PNG."
    },
    {
        "repo_full_name": "tldraw/tldraw",
        "repo_url": "https://github.com/tldraw/tldraw",
        "stars": 44000,
        "today_stars": 310,
        "forks": 2700,
        "primary_language": "TypeScript",
        "license": "tldraw license",
        "description": "A collaborative digital canvas library for the web. SDK for building custom canvas, drawing, and Canva-like interactive editors.",
        "topics": ["design", "canvas", "sdk", "whiteboard", "canva"],
        "tech_score": 9.6,
        "demo_code": "import { Tldraw } from '@tldraw/tldraw';\nimport '@tldraw/tldraw/tldraw.css';\nexport default () => <Tldraw />;",
        "readme_content": "# tldraw: SDK Bảng Vẽ & Thiết Kế Đồ Họa Đa Năng\nBộ công cụ xây dựng ứng dụng canvas sáng tạo, chỉnh sửa hình ảnh, phác thảo ý tưởng tương tự Canva trên nền WebGL/SVG."
    },
    {
        "repo_full_name": "shadcn-ui/ui",
        "repo_url": "https://github.com/shadcn-ui/ui",
        "stars": 76000,
        "today_stars": 450,
        "forks": 6200,
        "primary_language": "TypeScript",
        "license": "MIT",
        "description": "Beautifully designed components that you can copy and paste into your apps. Accessible, customizable, and modern design system.",
        "topics": ["design", "ui", "tailwind", "components", "react"],
        "tech_score": 9.9,
        "is_bookmarked": 1,
        "demo_code": "npx shadcn@latest add button card dialog dropdown-menu",
        "readme_content": "# shadcn/ui: Hệ Thống Giao Diện Thiết Kế Đỉnh Cao\nBộ thư viện thành phần UI thẩm mỹ cao nhất hiện nay, dựa trên Radix UI và Tailwind CSS, không bị trói buộc npm package."
    },
    {
        "repo_full_name": "tailwindlabs/tailwindcss",
        "repo_url": "https://github.com/tailwindlabs/tailwindcss",
        "stars": 84000,
        "today_stars": 115,
        "forks": 4400,
        "primary_language": "Rust / JavaScript",
        "license": "MIT",
        "description": "A utility-first CSS framework for rapid UI development without leaving your HTML.",
        "topics": ["design", "css", "frontend", "ui"],
        "tech_score": 9.8,
        "demo_code": "<div class=\"p-6 max-w-sm mx-auto bg-white rounded-xl shadow-lg flex items-center space-x-4\">...</div>",
        "readme_content": "# Tailwind CSS: Thiết Kế Giao Diện Tốc Độ Cao\nFramework CSS utility-first phổ biến nhất thế giới cho thiết kế web responsive hiện đại."
    },
    {
        "repo_full_name": "ant-design/ant-design",
        "repo_url": "https://github.com/ant-design/ant-design",
        "stars": 93000,
        "today_stars": 95,
        "forks": 46000,
        "primary_language": "TypeScript",
        "license": "MIT",
        "description": "An enterprise-class UI design language and React UI library with a set of high-quality React components.",
        "topics": ["design", "ui", "enterprise", "react"],
        "tech_score": 9.6,
        "demo_code": "import { Button, DatePicker } from 'antd';\nconst App = () => <Button type='primary'>Spider Radar</Button>;",
        "readme_content": "# Ant Design: Ngôn Ngữ Thiết Kế Doanh Nghiệp\nHệ thống thiết kế giao diện hoàn chỉnh phục vụ các ứng dụng quản trị phức tạp."
    },
    {
        "repo_full_name": "storybookjs/storybook",
        "repo_url": "https://github.com/storybookjs/storybook",
        "stars": 84000,
        "today_stars": 105,
        "forks": 9300,
        "primary_language": "TypeScript",
        "license": "MIT",
        "description": "Storybook is a frontend workshop for building UI components and pages in isolation with design system documentation.",
        "topics": ["design", "ui", "workshop", "frontend", "testing"],
        "tech_score": 9.7,
        "demo_code": "npx storybook@latest init\nnpm run storybook",
        "readme_content": "# Storybook: Không Gian Sáng Tạo Thành Phần UI\nMôi trường phát triển và kiểm thử độc lập cho các component thiết kế giao diện."
    },

    # --- TOP AI, REASONING & SYSTEMS ---
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
        "readme_content": "# DeepSeek-R1: Mô Hình Suy Luận Đỉnh Cao Bằng RL Thuần Túy\nĐạt hiệu năng tương đương OpenAI-o1 trên các bài toán logic, toán học và lập trình."
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
        "demo_code": "# Multi-head Latent Attention (MLA)\nmla_kv = allocate_compressed_latent(tokens=4096)",
        "readme_content": "# DeepSeek-V3: Mô Hình MoE Mã Nguồn Mở Tối Tân\nTrang bị kiến trúc MLA nén bộ nhớ đệm và FP8 mixed precision training."
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
        "demo_code": "from decision_engine import SystemOneEngine\nengine = SystemOneEngine.load('checkpoints/decision3_core.safetensors')\nresult = engine.predict_binary(text='Lãi suất điều hành tăng nhẹ')",
        "readme_content": "# Decision 3 Lite: Động Cơ Phản Xạ Trực Giác Sub-10ms\nChạy trong Docker container trên CPU với 180MB RAM footprint, hỗ trợ Spider News Radar."
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
        "readme_content": "# uv: Trình Quản Lý Gói Python Bằng Rust Siêu Tốc\nThay thế hoàn hảo pip, poetry, pyenv với tốc độ vượt trội."
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
        "readme_content": "# Ollama: Chạy LLM Cục Bộ Với Một Câu Lệnh\nĐóng gói trọng số mô hình và tăng tốc phần cứng thành một tệp thực thi duy nhất."
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
        "demo_code": "from laya_agent import LayaPolicy\nagent = LayaPolicy(cuda_device=0)\naction = agent.step(observation={'word': 'Lãi suất', 'screen': 'SpiderArena'})",
        "readme_content": "# Laya: Latent Action Reinforcement Learning Agent\nTối ưu hóa phản xạ web thời gian thực dưới 50ms roundtrip."
    },
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
        "demo_code": "from autogpt.agent import Agent\nagent = Agent.create(goal='Analyze macroeconomic news')",
        "readme_content": "# AutoGPT: Nền Tảng AI Agent Tự Hành\nKết nối chuỗi suy nghĩ LLM để tự động thực hiện các mục tiêu phức tạp."
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
        "demo_code": "python launch.py --listen --port 7860",
        "readme_content": "# Stable Diffusion Web UI\nGiao diện trình duyệt chạy mô hình tạo ảnh AI khuếch tán cục bộ."
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
        "demo_code": "from transformers import pipeline\nclassifier = pipeline('sentiment-analysis')",
        "readme_content": "# 🤗 Transformers: Trụ Cột Học Sâu Hiện Đại\nCung cấp hàng nghìn mô hình AI pretrained chuẩn mực cho giới nghiên cứu và phát triển."
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
        "readme_content": "# LangChain: Khung Điều Phối Ứng Dụng LLM\nXây dựng RAG và các chuỗi phản hồi phức tạp với dữ liệu doanh nghiệp."
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
        "demo_code": "import torch\nx = torch.randn(3, 3, device='cuda')",
        "readme_content": "# PyTorch: Nền Tảng Học Máy Động Hàng Đầu\nTăng tốc tính toán tensor trên GPU với đồ thị động và autograd chuẩn xác."
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
        "demo_code": "#[tauri::command]\nfn trigger_spider_event() { ... }",
        "readme_content": "# Tauri v2: Runtime Ứng Dụng Desktop Nhẹ & Bảo Mật\nNền tảng desktop bản địa thay thế hoàn toàn Electron, dùng Webview hệ thống và lõi Rust."
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
        "demo_code": "from fastapi import FastAPI\napp = FastAPI()",
        "readme_content": "# FastAPI: Framework Web Bất Đồng Bộ Hiện Đại\nXây dựng API hiệu năng cao với type hint chuẩn của Python."
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
        "demo_code": "import whisper\nmodel = whisper.load_model('base')",
        "readme_content": "# OpenAI Whisper: Nhận Dạng Giọng Nói Đa Ngôn Ngữ\nMô hình ASR mã nguồn mở mạnh mẽ hỗ trợ chuyển đổi âm thanh sang văn bản."
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
        "demo_code": "./main -m models/7B/ggml-model-q4_0.bin -p 'Kinh tế vĩ mô'",
        "readme_content": "# llama.cpp: Suy Luận LLM Thuần C/C++\nChạy LLM trên phần cứng người dùng với cơ chế lượng tử hóa 4-bit, 8-bit cực kỳ tối ưu."
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
        "topics": ["ai", "nodes", "diffusion", "workflow", "design"],
        "tech_score": 9.5,
        "demo_code": "python main.py --port 8188",
        "readme_content": "# ComfyUI: Workspace Tạo Ảnh Bằng Nút Trực Quan\nThiết kế các pipeline sáng tạo phức tạp với Stable Diffusion và Flux."
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
        "demo_code": "from vllm import LLM\nllm = LLM(model='meta-llama/Llama-3-8b')",
        "readme_content": "# vLLM: Động Cơ Phục Vụ LLM Thông Lượng Cao\nĐột phá PagedAttention giúp tiết kiệm bộ nhớ KV cache và tăng tốc độ xử lý tới 24 lần."
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
        "demo_code": "from qdrant_client import QdrantClient\nclient = QdrantClient(':memory:')",
        "readme_content": "# Qdrant: Cơ Sở Dữ Liệu Vector Bằng Rust\nTìm kiếm độ tương đồng vector hiệu năng cao với bộ lọc payload JSON linh hoạt."
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
