from typing import List, Dict, Any, Optional
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from app.core.config import get_settings

settings = get_settings()


class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self._vectorstore: Optional[Chroma] = None
    
    @property
    def vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            os.makedirs(settings.chroma_persist_directory, exist_ok=True)
            self._vectorstore = Chroma(
                persist_directory=settings.chroma_persist_directory,
                embedding_function=self.embeddings,
                collection_name="ev-knowledge"
            )
        return self._vectorstore
    
    def process_document(self, content: str, doc_id: int) -> List[str]:
        """Split document into chunks and add to vector store."""
        chunks = self.text_splitter.split_text(content)
        metadatas = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]
        
        self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)
        self.vectorstore.persist()
        
        return chunks
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant document chunks."""
        docs = self.vectorstore.similarity_search(query, k=top_k)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
    
    def answer_question(self, question: str, top_k: int = 5) -> tuple[str, List[Dict]]:
        """Answer a question using RAG."""
        docs = self.vectorstore.similarity_search(question, k=top_k)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=settings.openai_api_key,
            temperature=0.7
        )
        
        prompt = f"""You are an expert on Expected Value (EV) knowledge and DeFi.
Based on the following context, answer the user's question thoroughly and accurately.

Context:
{context}

Question: {question}

Answer:"""

        answer = llm.invoke(prompt)
        
        sources = [
            {
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
        
        return answer.content, sources
    
    def clear_all(self) -> None:
        """Clear all documents from the vector store."""
        self.vectorstore.delete_collection()
        self._vectorstore = None


rag_service = RAGService()
