# Local Smart Doc

一个本地化的智能文档问答系统，支持文档上传、向量存储和基于RAG的智能问答。

## 🎯 项目目标

构建一个完全本地化的文档智能助手，支持：
- 📄 文档上传与解析（PDF, Word, Excel, TXT等）
- 🗄️ 向量数据库存储（Chroma/Qdrant）
- 🤖 本地LLM集成（Ollama）
- 🔍 RAG（检索增强生成）问答
- 🌐 友好的Web界面

## 🏗️ 技术栈

### 后端 (Python)
- **Web框架**: FastAPI
- **向量数据库**: ChromaDB / Qdrant
- **文档解析**: Unstructured, PyPDF2, python-docx
- **RAG框架**: LangChain / LlamaIndex
- **LLM集成**: Ollama API
- **任务队列**: Celery (可选)

### 前端 (TypeScript)
- **框架**: Next.js 14 / React
- **UI库**: Shadcn/ui + Tailwind CSS
- **状态管理**: Zustand
- **HTTP客户端**: Axios / TanStack Query
- **构建工具**: Vite (可选)

### 开发工具
- **代码质量**: Black, isort, flake8 (Python), ESLint, Prettier (TS)
- **测试**: pytest, Jest, React Testing Library
- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## 📁 项目结构

```
local_smart_doc/
├── backend/                 # Python后端
│   ├── app/                # FastAPI应用
│   ├── core/               # 核心逻辑
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   ├── utils/              # 工具函数
│   ├── tests/              # 测试
│   ├── requirements.txt    # Python依赖
│   └── main.py            # 入口文件
├── frontend/               # TypeScript前端
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # React组件
│   │   ├── lib/          # 工具库
│   │   ├── types/        # TypeScript类型
│   │   └── styles/       # 样式文件
│   ├── public/            # 静态资源
│   ├── package.json       # 依赖配置
│   └── next.config.js    # Next.js配置
├── docs/                  # 项目文档
├── scripts/              # 部署/工具脚本
├── docker/               # Docker配置
├── .github/workflows/    # CI/CD配置
├── docker-compose.yml    # 开发环境编排
├── .env.example         # 环境变量示例
└── README.md            # 项目说明
```

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (可选)
- Ollama (本地LLM)

### 开发环境设置
```bash
# 1. 克隆项目
git clone https://github.com/Redestiny/local_smart_doc.git
cd local_smart_doc

# 2. 后端设置
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 前端设置
cd ../frontend
npm install

# 4. 启动服务
# 后端 (端口 8000)
cd backend && uvicorn main:app --reload

# 前端 (端口 3000)
cd frontend && npm run dev
```

## 🔧 配置说明

### 环境变量
复制 `.env.example` 为 `.env` 并配置：
```env
# 后端配置
DATABASE_URL=sqlite:///./local_smart_doc.db
VECTOR_DB_PATH=./data/vector_db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# 前端配置
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Ollama 设置
```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下载模型
ollama pull llama3.2
ollama pull nomic-embed-text
```

## 📖 功能规划

### Phase 1: MVP (基础功能)
- [ ] 文档上传接口
- [ ] 文本提取与分块
- [ ] 向量嵌入与存储
- [ ] 基础问答接口
- [ ] 简单Web界面

### Phase 2: 增强功能
- [ ] 多格式文档支持
- [ ] 对话历史管理
- [ ] 文档管理界面
- [ ] 搜索优化
- [ ] 用户认证

### Phase 3: 高级功能
- [ ] 批量处理
- [ ] API密钥管理
- [ ] 插件系统
- [ ] 移动端适配
- [ ] 离线模式

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Ollama](https://ollama.com/) - 本地LLM运行
- [LangChain](https://www.langchain.com/) - RAG框架
- [Chroma](https://www.trychroma.com/) - 向量数据库
- [FastAPI](https://fastapi.tiangolo.com/) - Python Web框架
- [Next.js](https://nextjs.org/) - React框架

## 📞 联系

如有问题或建议，请通过GitHub Issues提交。

---

**注意**: 本项目处于早期开发阶段，API和功能可能会有较大变化。
