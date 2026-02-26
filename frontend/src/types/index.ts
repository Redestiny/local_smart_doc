export interface Document {
  id: number;
  title: string;
  content: string;
  file_path?: string;
  is_processed: boolean;
  created_at: string;
  updated_at: string;
}

export interface DocumentChunk {
  id: number;
  chunk_index: number;
  content: string;
}

export interface DocumentWithChunks extends Document {
  chunks: DocumentChunk[];
}

export interface Conversation {
  id: number;
  title?: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationWithMessages extends Conversation {
  messages: Message[];
}

export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  sources?: string;
  created_at: string;
}

export interface QARequest {
  question: string;
  conversation_id?: number;
  top_k?: number;
}

export interface QAResponse {
  answer: string;
  sources: Source[];
  conversation_id: number;
  message_id: number;
}

export interface Source {
  content: string;
  metadata: Record<string, unknown>;
}
