import React, { useEffect, useState } from 'react';
import API from '../api/api';
import BookmarkCard from '../components/BookmarkCard';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [url, setUrl] = useState('');
  const [bookmarks, setBookmarks] = useState([]);
  const navigate = useNavigate();

  // Load all saved bookmarks
  const fetchBookmarks = async () => {
    try {
      const res = await API.get('/bookmarks');
      setBookmarks(res.data);
    } catch (err) {
      console.error('Error fetching bookmarks', err);
      if (err.response && err.response.status === 401) {
        localStorage.removeItem('token');
        navigate('/');
      }
    }
  };

  // Add new bookmark
  const addBookmark = async (e) => {
    e.preventDefault();
    if (!url.startsWith('http')) {
      alert('Please enter a valid URL (must start with http or https)');
      return;
    }

    try {
      await API.post('/bookmarks', { url });
      setUrl('');
      fetchBookmarks();
    } catch (err) {
      console.error('Failed to add bookmark:', err.response?.data || err.message);
      alert(err.response?.data?.readableMessage || 'Failed to add bookmark');
    }
  };

  // Delete bookmark by ID
  const deleteBookmark = async (id) => {
    try {
      await API.delete(`/bookmarks/${id}`);
      fetchBookmarks();
    } catch (err) {
      console.error('Failed to delete bookmark:', err);
      alert('Failed to delete bookmark');
    }
  };

  // Logout
  const logout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  // Load bookmarks on mount
  useEffect(() => {
    fetchBookmarks();
  }, []);

  return (
    <div style={{ padding: '20px', maxWidth: '700px', margin: '0 auto' }}>
      <h2>Your Bookmarks</h2>
      <form onSubmit={addBookmark} style={{ marginBottom: '20px' }}>
        <input
          type="url"
          placeholder="Enter valid URL like https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          style={{ padding: '8px', width: '70%' }}
        />
        <button type="submit" style={{ padding: '8px 12px', marginLeft: '10px' }}>Add</button>
        <button
          onClick={logout}
          type="button"
          style={{ padding: '8px 12px', marginLeft: '10px', backgroundColor: '#f44336', color: '#fff' }}
        >
          Logout
        </button>
      </form>

      <div>
        {bookmarks.length === 0 ? (
          <p>No bookmarks yet. Try adding one!</p>
        ) : (
          bookmarks.map((bm) =>
            bm.url?.startsWith('http') ? (
              <BookmarkCard key={bm.id} bookmark={bm} onDelete={deleteBookmark} />
            ) : null
          )
        )}
      </div>
    </div>
  );
}

export default Dashboard;
