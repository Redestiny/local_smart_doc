import { useState, useRef } from 'react';

interface DocumentUploadProps {
  onUpload: (file: File) => Promise<void>;
  onCreate: (title: string, content: string) => Promise<void>;
}

export default function DocumentUpload({ onUpload, onCreate }: DocumentUploadProps) {
  const [mode, setMode] = useState<'upload' | 'create'>('upload');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIsLoading(true);
    try {
      await onUpload(file);
    } finally {
      setIsLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleCreate = async () => {
    if (!title.trim() || !content.trim()) return;
    setIsLoading(true);
    try {
      await onCreate(title.trim(), content.trim());
      setTitle('');
      setContent('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <button
          type="button"
          onClick={() => setMode('upload')}
          className={`px-3 py-1 text-sm rounded ${mode === 'upload' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}
        >
          Upload
        </button>
        <button
          type="button"
          onClick={() => setMode('create')}
          className={`px-3 py-1 text-sm rounded ${mode === 'create' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}
        >
          Create
        </button>
      </div>

      {mode === 'upload' ? (
        <div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".txt,.md,.json"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700"
            disabled={isLoading}
          />
        </div>
      ) : (
        <div className="space-y-4">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Title"
            className="w-full border rounded-lg px-3 py-2"
          />
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Content"
            rows={4}
            className="w-full border rounded-lg px-3 py-2"
          />
          <button
            onClick={handleCreate}
            disabled={!title.trim() || !content.trim() || isLoading}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading ? 'Creating...' : 'Create'}
          </button>
        </div>
      )}
    </div>
  );
}
