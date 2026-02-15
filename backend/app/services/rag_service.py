"""
电动汽车知识问答系统 - RAG服务
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from app.core.config import settings

class EVRAGService:
    """电动汽车领域RAG服务"""
    
    def __init__(self):
        self.vector_store = None
        self.qa_chain = None
        self.initialized = False
        self.ev_keywords = settings.DOMAIN_KEYWORDS
        
    def initialize(self):
        """初始化RAG系统"""
        try:
            logger.info("🚀 初始化电动汽车RAG系统...")
            
            # 1. 初始化嵌入模型
            embeddings = OllamaEmbeddings(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_EMBEDDING_MODEL
            )
            
            # 2. 初始化向量存储
            vector_store_path = settings.VECTOR_DB_DIR / "ev_knowledge"
            self.vector_store = Chroma(
                persist_directory=str(vector_store_path),
                embedding_function=embeddings,
                collection_name="ev_knowledge_base"
            )
            
            # 3. 初始化LLM
            llm = Ollama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=0.1,  # 降低温度以获得更准确的回答
                num_predict=512  # 限制生成长度
            )
            
            # 4. 创建电动汽车领域特定的提示模板
            prompt_template = PromptTemplate(
                template="""你是一个电动汽车领域的专家助手。请基于以下上下文信息回答问题。

上下文信息:
{context}

问题: {question}

请按照以下要求回答:
1. 如果上下文信息中包含答案，请基于上下文准确回答
2. 如果上下文信息不足，请基于你的电动汽车领域知识回答
3. 回答要专业、准确、简洁
4. 如果涉及技术参数，请提供具体数值
5. 对于不确定的信息，请说明"根据现有信息无法确定"

电动汽车领域关键词: {keywords}

请用中文回答:""",
                input_variables=["context", "question", "keywords"]
            )
            
            # 5. 创建检索QA链
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": settings.SIMILARITY_TOP_K}
                ),
                chain_type_kwargs={
                    "prompt": prompt_template,
                    "verbose": True
                },
                return_source_documents=True
            )
            
            # 6. 初始化对话记忆
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            self.initialized = True
            logger.info("✅ 电动汽车RAG系统初始化完成")
            
        except Exception as e:
            logger.error(f"❌ RAG系统初始化失败: {e}")
            raise
    
    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self.initialized
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """添加文档到知识库"""
        if not self.initialized:
            self.initialize()
        
        try:
            # 文本分割
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                separators=["\n\n", "\n", "。", "！", "？", "；", "，", "、", " "]
            )
            
            chunks = text_splitter.create_documents(documents, metadata)
            
            # 添加到向量存储
            self.vector_store.add_documents(chunks)
            self.vector_store.persist()
            
            logger.info(f"✅ 已添加 {len(chunks)} 个文档块到知识库")
            return True
            
        except Exception as e:
            logger.error(f"❌ 添加文档失败: {e}")
            return False
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """提问问题"""
        if not self.initialized:
            self.initialize()
        
        try:
            # 增强问题（添加电动汽车领域上下文）
            enhanced_question = self._enhance_question(question)
            
            # 执行问答
            result = self.qa_chain({
                "query": enhanced_question,
                "keywords": ", ".join(self.ev_keywords)
            })
            
            # 提取源文档信息
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_info = {
                        "content": doc.page_content[:200] + "...",
                        "metadata": doc.metadata
                    }
                    sources.append(source_info)
            
            # 更新对话记忆
            self.memory.save_context(
                {"input": question},
                {"output": result["result"]}
            )
            
            return {
                "answer": result["result"],
                "sources": sources,
                "question": question,
                "enhanced_question": enhanced_question,
                "domain": "electric_vehicles"
            }
            
        except Exception as e:
            logger.error(f"❌ 问答失败: {e}")
            return {
                "answer": f"抱歉，处理问题时出现错误: {str(e)}",
                "sources": [],
                "question": question,
                "error": str(e)
            }
    
    def _enhance_question(self, question: str) -> str:
        """增强问题 - 添加电动汽车领域上下文"""
        enhanced = question
        
        # 检查是否包含电动汽车关键词
        has_ev_keyword = any(keyword in question for keyword in self.ev_keywords)
        
        if not has_ev_keyword:
            # 如果不是明显的电动汽车问题，添加领域提示
            enhanced = f"关于电动汽车领域的: {question}"
        
        return enhanced
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        """搜索相似内容"""
        if not self.initialized:
            self.initialize()
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ 搜索失败: {e}")
            return []
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        if not self.initialized:
            self.initialize()
        
        try:
            # 获取集合信息
            collection = self.vector_store._collection
            count = collection.count() if collection else 0
            
            return {
                "document_count": count,
                "domain": settings.DOMAIN,
                "keywords": self.ev_keywords,
                "model": settings.OLLAMA_MODEL,
                "vector_db": "Chroma",
                "status": "active" if count > 0 else "empty"
            }
            
        except Exception as e:
            logger.error(f"❌ 获取统计信息失败: {e}")
            return {
                "document_count": 0,
                "domain": settings.DOMAIN,
                "status": "error",
                "error": str(e)
            }
    
    def clear_knowledge_base(self) -> bool:
        """清空知识库"""
        try:
            if self.vector_store:
                self.vector_store.delete_collection()
                self.vector_store = None
            
            # 重新初始化
            self.initialized = False
            self.initialize()
            
            logger.info("✅ 知识库已清空")
            return True
            
        except Exception as e:
            logger.error(f"❌ 清空知识库失败: {e}")
            return False

# 全局RAG服务实例
rag_service = EVRAGService()