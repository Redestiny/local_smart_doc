import type { Document } from '@/types';

interface DocumentListProps {
  documents: Document[];
  onDelete: (id: number) => void;
}

export default function DocumentList({ documents, onDelete }: DocumentListProps) {
  if (documents.length === 0) {
    return <div className="p-4 text-center text-gray-500">No documents yet.</div>;
  }

  return (
    <ul className="divide-y divide-gray-200">
      {documents.map((doc) => (
        <li key={doc.id} className="flex items-center justify-between p-4">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{doc.title}</p>
            <p className="text-xs text-gray-500">
              {doc.is_processed ? '✓ Processed' : '⏳ Pending'} • {new Date(doc.created_at).toLocaleDateString()}
            </p>
          </div>
          <button
            onClick={() => onDelete(doc.id)}
            className="ml-4 text-red-600 hover:text-red-800 text-sm"
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
