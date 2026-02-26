'use client';

import { useState, useEffect } from 'react';
import Chat from '@/components/Chat';
import DocumentUpload from '@/components/DocumentUpload';
import DocumentList from '@/components/DocumentList';
import { documentsApi, conversationsApi, qaApi } from '@/lib/api';
import type { Document, Conversation, Message } from '@/types';

export default function Home() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'chat' | 'documents'>('chat');

  useEffect(() => {
    loadDocuments();
    loadConversations();
  }, []);

  const loadDocuments = async () => {
    try {
      const res = await documentsApi.list();
      setDocuments(res.data);
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  };

  const loadConversations = async () => {
    try {
      const res = await conversationsApi.list();
      setConversations(res.data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const handleUpload = async (file: File) => {
    await documentsApi.upload(file);
    loadDocuments();
  };

  const handleCreate = async (title: string, content: string) => {
    await documentsApi.create({ title, content });
    loadDocuments();
  };

  const handleDelete = async (id: number) => {
    await documentsApi.delete(id);
    loadDocuments();
  };

  const handleSendMessage = async (content: string) => {
    setIsLoading(true);
    try {
      const res = await qaApi.ask({
        question: content,
        conversation_id: currentConversation?.id,
      });

      if (!currentConversation) {
        const convRes = await conversationsApi.create({ title: content.slice(0, 50) });
        setCurrentConversation(convRes.data);
        setConversations([convRes.data, ...conversations]);
        setMessages([
          { id: res.data.message_id - 1, conversation_id: convRes.data.id, role: 'user', content, created_at: new Date().toISOString() },
          { id: res.data.message_id, conversation_id: convRes.data.id, role: 'assistant', content: res.data.answer, created_at: new Date().toISOString() },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { id: res.data.message_id - 1, conversation_id: currentConversation.id, role: 'user', content, created_at: new Date().toISOString() },
          { id: res.data.message_id, conversation_id: currentConversation.id, role: 'assistant', content: res.data.answer, created_at: new Date().toISOString() },
        ]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectConversation = async (conv: Conversation) => {
    const res = await conversationsApi.get(conv.id);
    setCurrentConversation(res.data);
    setMessages(res.data.messages);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Local Smart Doc</h1>
          <div className="flex gap-2">
            <button onClick={() => setActiveTab('chat')} className={`px-4 py-2 rounded-lg ${activeTab === 'chat' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Chat</button>
            <button onClick={() => setActiveTab('documents')} className={`px-4 py-2 rounded-lg ${activeTab === 'documents' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Documents</button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'documents' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Add Document</h2>
              <DocumentUpload onUpload={handleUpload} onCreate={handleCreate} />
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Documents</h2>
              <DocumentList documents={documents} onDelete={handleDelete} />
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold mb-4">History</h2>
              {conversations.length === 0 ? <p className="text-gray-500 text-sm">No conversations.</p> : (
                <ul className="space-y-2">
                  {conversations.map((conv) => (
                    <li key={conv.id} onClick={() => handleSelectConversation(conv)} className={`p-2 rounded cursor-pointer ${currentConversation?.id === conv.id ? 'bg-blue-100' : 'hover:bg-gray-100'}`}>
                      <p className="text-sm font-medium truncate">{conv.title || 'Untitled'}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div className="md:col-span-3 bg-white rounded-lg shadow h-[600px]">
              <Chat messages={messages} onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
