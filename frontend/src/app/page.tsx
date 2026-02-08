import { Upload, MessageSquare, Database, Cpu } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* 导航栏 */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex items-center space-x-2">
                <Cpu className="h-8 w-8 text-blue-600" />
                <span className="text-xl font-bold text-gray-900">Local Smart Doc</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900">
                GitHub
              </button>
              <button className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* 英雄区域 */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl mb-6">
            本地智能文档助手
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-10">
            完全本地化的文档问答系统，支持文档上传、向量存储和基于RAG的智能问答。
            保护您的数据隐私，无需连接互联网。
          </p>
          <div className="flex justify-center space-x-4">
            <button className="px-8 py-3 text-lg font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">
              开始使用
            </button>
            <button className="px-8 py-3 text-lg font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
              查看文档
            </button>
          </div>
        </div>

        {/* 功能展示 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <Upload className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">文档上传</h3>
            <p className="text-gray-600">
              支持PDF、Word、Excel、TXT等多种格式，智能解析文档内容。
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <Database className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">向量存储</h3>
            <p className="text-gray-600">
              使用Chroma向量数据库，高效存储和检索文档语义信息。
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <Cpu className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">本地LLM</h3>
            <p className="text-gray-600">
              集成Ollama，支持多种本地大语言模型，完全离线运行。
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
              <MessageSquare className="h-6 w-6 text-orange-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">智能问答</h3>
            <p className="text-gray-600">
              基于RAG技术，提供准确、上下文相关的文档问答服务。
            </p>
          </div>
        </div>

        {/* 技术栈 */}
        <div className="bg-white rounded-xl shadow-sm border p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">技术栈</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { name: 'FastAPI', color: 'bg-green-100 text-green-800' },
              { name: 'Next.js', color: 'bg-gray-100 text-gray-800' },
              { name: 'TypeScript', color: 'bg-blue-100 text-blue-800' },
              { name: 'ChromaDB', color: 'bg-purple-100 text-purple-800' },
              { name: 'Ollama', color: 'bg-yellow-100 text-yellow-800' },
              { name: 'LangChain', color: 'bg-red-100 text-red-800' },
              { name: 'Tailwind', color: 'bg-teal-100 text-teal-800' },
              { name: 'Docker', color: 'bg-indigo-100 text-indigo-800' },
            ].map((tech) => (
              <div
                key={tech.name}
                className={`px-4 py-3 rounded-lg text-center font-medium ${tech.color}`}
              >
                {tech.name}
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">准备好开始了吗？</h2>
          <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
            只需几分钟即可在本地部署，完全掌控您的数据，享受智能文档助手的便利。
          </p>
          <button className="px-8 py-3 text-lg font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">
            查看部署指南
          </button>
        </div>
      </main>

      {/* 页脚 */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>© 2024 Local Smart Doc. 一个完全本地化的智能文档问答系统。</p>
            <p className="mt-2 text-sm">
              开源项目 · MIT许可证 · 由社区驱动
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
