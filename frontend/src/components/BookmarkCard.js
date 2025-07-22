// src/components/BookmarkCard.js
import React from 'react';
import ReactMarkdown from 'react-markdown';

function BookmarkCard({ bookmark, onDelete }) {
  return (
    <div style={{ 
      border: '1px solid #ccc', 
      padding: '12px', 
      margin: '10px 0',
      borderRadius: '8px',
      backgroundColor: '#f9f9f9'
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        {bookmark.favicon && (
          <img src={bookmark.favicon} alt="Favicon" width="20" height="20" style={{ marginRight: '8px' }} />
        )}
        <h3 style={{ margin: 0 }}>{bookmark.title || 'No Title'}</h3>
      </div>

      <p style={{ margin: '6px 0' }}>
        <a href={bookmark.url} target="_blank" rel="noopener noreferrer">
          {bookmark.url}
        </a>
      </p>

      <ReactMarkdown children={bookmark.summary || 'No Summary Available'} />

      <button 
        onClick={() => onDelete(bookmark.id)} 
        style={{ marginTop: '8px', padding: '6px 10px', background: '#e74c3c', color: '#fff', border: 'none', borderRadius: '4px' }}
      >
        Delete
      </button>
    </div>
  );
}

export default BookmarkCard;
